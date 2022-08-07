""" for Climate integration."""
from __future__ import annotations
from datetime import timedelta
import logging


from homeassistant.components.climate import (
    ClimateEntity,
    ConfigEntry,
)
from homeassistant.components.climate.const import HVACMode, FAN_AUTO
from homeassistant.const import TEMP_CELSIUS, ATTR_TEMPERATURE
from homeassistant.util import Throttle
from homeassistant.const import CONF_HOST

from .wfrac.device import MIN_TIME_BETWEEN_UPDATES, Device
from .wfrac.models.aircon import AirconCommands
from .const import (
    DOMAIN,
    FAN_MODE_TRANSLATION,
    HVAC_TRANSLATION,
    SUPPORT_FLAGS,
    SUPPORT_SWING_MODES,
    SUPPORTED_FAN_MODES,
    SUPPORTED_HVAC_MODES,
    SWING_3D_AUTO,
    SWING_MODE_TRANSLATION,
    SWING_OFF,
)

_LOGGER = logging.getLogger(__name__)
MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=10)


async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities):
    """Setup climate entities"""
    for device in hass.data[DOMAIN]:
        if device.host == entry.data[CONF_HOST]:
            _LOGGER.info("Setup switch for: %s, %s", device.name, device.airco_id)
            async_add_entities([AircoClimate(device)])


class AircoClimate(ClimateEntity):
    """Representation of a climate entity"""

    _attr_supported_features: int = SUPPORT_FLAGS
    _attr_temperature_unit: str = TEMP_CELSIUS
    _attr_hvac_modes: list[HVACMode] = SUPPORTED_HVAC_MODES
    _attr_fan_modes: list[str] = SUPPORTED_FAN_MODES
    _attr_hvac_mode: HVACMode = HVACMode.OFF
    _attr_fan_mode: str = FAN_AUTO
    _attr_swing_mode: str | None = SWING_OFF
    _attr_swing_modes: list[str] | None = SUPPORT_SWING_MODES
    _attr_min_temp: float = 16
    _attr_max_temp: float = 30

    def __init__(self, device: Device) -> None:
        self._device = device
        self._attr_name = device.name
        self._attr_device_info = device.device_info
        self._attr_unique_id = f"{DOMAIN}-{self._device.airco_id}-climate"
        self._update_state()

    async def async_set_temperature(self, **kwargs) -> None:
        """Set new target temperature."""
        await self._device.set_airco(
            {AirconCommands.PresetTemp: kwargs.get(ATTR_TEMPERATURE)}
        )
        self._update_state()

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        """Set new target fan mode."""
        await self._device.set_airco(
            {AirconCommands.AirFlow: FAN_MODE_TRANSLATION[fan_mode]}
        )
        self._update_state()

    async def async_turn_on(self) -> None:
        """Turn the entity on."""
        await self._device.set_airco({AirconCommands.Operation: True})
        self._update_state()

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target hvac mode."""
        await self._device.set_airco(
            {
                AirconCommands.OperationMode: self._device.airco.OperationMode
                if hvac_mode == HVACMode.OFF
                else HVAC_TRANSLATION[hvac_mode],
                AirconCommands.Operation: hvac_mode != HVACMode.OFF,
            }
        )
        self._update_state()

    async def async_set_swing_mode(self, swing_mode: str) -> None:
        """Set new target swing operation."""
        _airco = self._device.airco
        _swing_auto = swing_mode == SWING_3D_AUTO
        _swing_ud = _airco.WindDirectionUD

        if swing_mode != SWING_3D_AUTO:
            _swing_ud = SWING_MODE_TRANSLATION[swing_mode]

        await self._device.set_airco(
            {
                AirconCommands.WindDirectionUD: _swing_ud,
                AirconCommands.Entrust: _swing_auto,
            }
        )
        self._update_state()

    async def async_turn_off(self) -> None:
        """Turn the entity off."""
        await self._device.set_airco({AirconCommands.Operation: False})
        self._update_state()

    def _update_state(self) -> None:
        """Private update attributes"""
        airco = self._device.airco

        self._attr_target_temperature = airco.PresetTemp
        self._attr_current_temperature = airco.IndoorTemp
        self._attr_fan_mode = list(FAN_MODE_TRANSLATION.keys())[airco.AirFlow]
        self._attr_swing_mode = (
            SWING_3D_AUTO
            if airco.Entrust
            else list(SWING_MODE_TRANSLATION.keys())[airco.WindDirectionUD]
        )
        self._attr_hvac_mode = list(HVAC_TRANSLATION.keys())[airco.OperationMode]

        if airco.Operation is False:
            self._attr_hvac_mode = HVACMode.OFF
        else:
            _new_mode: HVACMode = None
            _mode = airco.OperationMode
            if _mode == 0:
                _new_mode = HVACMode.AUTO
            elif _mode == 1:
                _new_mode = HVACMode.COOL
            elif _mode == 2:
                _new_mode = HVACMode.HEAT
            elif _mode == 3:
                _new_mode = HVACMode.FAN_ONLY
            elif _mode == 4:
                _new_mode = HVACMode.DRY
            self._attr_hvac_mode = _new_mode

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Retrieve latest state."""
        await self._device.update()
        self._update_state()
