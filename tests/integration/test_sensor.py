"""Tests for sensor.py: the parts that only exist at the entity boundary.

The accumulator arithmetic itself is covered in tests/unit/test_energy_total.py
against a bare instance; what is left here needs Home Assistant around it -
the entity service, the restore path, and the one diagnostic sensor that
reports nothing rather than guessing.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.core import HomeAssistant, ServiceCall, State
from homeassistant.exceptions import ServiceValidationError
from pytest_homeassistant_custom_component.common import (
    MockEntityPlatform,
    mock_restore_cache_with_extra_data,
)

from custom_components.mitsubishi_wf_rac.const import ATTR_COOL_HOT_JUDGE
from custom_components.mitsubishi_wf_rac.sensor import (
    DiagnosticsSensor,
    EnergyTotalExtraStoredData,
    EnergyTotalSensor,
    async_set_energy_total,
)


async def test_setting_the_total_on_the_wrong_sensor_says_which(
    hass: HomeAssistant, platform_device
):
    """An entity service reaches every sensor of the integration.

    The handler is registered as a callable rather than a method name for
    exactly this: targeting any other sensor has to name the entity instead
    of failing with an AttributeError.
    """
    wrong = DiagnosticsSensor(platform_device, "error")
    wrong.entity_id = "sensor.living_room_error"

    with pytest.raises(ServiceValidationError, match="sensor.living_room_error"):
        await async_set_energy_total(
            wrong, MagicMock(spec=ServiceCall, data={"value": 12.0})
        )


async def test_setting_the_total_reanchors_the_meter(
    hass: HomeAssistant, platform_device
):
    """Carrying a figure over from a previous meter is the whole point."""
    sensor = EnergyTotalSensor(platform_device)
    sensor.async_write_ha_state = lambda: None

    await async_set_energy_total(
        sensor, MagicMock(spec=ServiceCall, data={"value": 412.5})
    )

    assert sensor.native_value == 412.5


@pytest.mark.parametrize(
    ("operation", "operation_mode"),
    [
        pytest.param(False, 1, id="unit_off"),
        pytest.param(True, 3, id="fan_only"),
    ],
)
async def test_the_judge_reports_nothing_when_it_means_nothing(
    hass: HomeAssistant, platform_device, operation: bool, operation_mode: int
):
    """CoolHotJudge keeps its last value while the unit is not regulating.

    Reporting it then would claim a direction the unit is not working in.
    """
    platform_device.airco.Operation = operation
    platform_device.airco.OperationMode = operation_mode
    sensor = DiagnosticsSensor(platform_device, ATTR_COOL_HOT_JUDGE)

    sensor._update_state()

    assert sensor.native_value is None


def test_a_stored_state_that_cannot_be_read_restores_nothing():
    """from_dict has to answer for anything the state store hands it."""
    assert EnergyTotalExtraStoredData.from_dict({"native_value": 3.0}) is None


async def test_the_total_survives_a_restart(hass: HomeAssistant, platform_device):
    """The lifetime figure is the sensor's whole reason to exist.

    The anchor is restored with it: the unit's counter keeps running across
    our restart, so without last_raw the first reading afterwards would be
    counted as consumption from zero all over again.
    """
    entity_id = "sensor.living_room_energy_usage_total"
    mock_restore_cache_with_extra_data(
        hass,
        ((State(entity_id, "123.5"), EnergyTotalExtraStoredData(123.5, "kWh", 0.75).as_dict()),),
    )
    platform_device.airco.Electric = 1.0
    sensor = EnergyTotalSensor(platform_device)
    sensor.entity_id = entity_id
    sensor.platform = MockEntityPlatform(hass)
    sensor.hass = hass

    await sensor.async_added_to_hass()

    # 123.5 carried over, plus the 0.25 the unit ran up while we were away.
    assert sensor.native_value == 123.75

    # Registering with the coordinator started its refresh timer.
    await platform_device.async_shutdown()
