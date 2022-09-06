""" for sensor integration."""
# pylint: disable = too-few-public-methods

from __future__ import annotations
from datetime import timedelta
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    TEMP_CELSIUS,
    ENERGY_KILO_WATT_HOUR,
    CONF_HOST,
    CONF_ERROR,
)
from homeassistant.util import Throttle
from homeassistant.helpers.entity import EntityCategory

from .wfrac.device import Device
from .const import (
    DOMAIN,
    ATTR_INSIDE_TEMPERATURE,
    ATTR_OUTSIDE_TEMPERATURE,
    CONF_OPERATOR_ID,
    CONF_AIRCO_ID,
    ATTR_DEVICE_ID,
    ATTR_CONNECTED_ACCOUNTS,
)

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=30)

async def async_setup_entry(hass, entry, async_add_entities):
    """Setup sensor entries"""

    for device in hass.data[DOMAIN]:
        if device.host == entry.data[CONF_HOST]:
            _LOGGER.info("Setup: %s, %s", device.name, device.airco_id)
            entities = [
                TemperatureSensor(device, "Indoor", ATTR_INSIDE_TEMPERATURE),
                TemperatureSensor(device, "Outdoor", ATTR_OUTSIDE_TEMPERATURE),
                DiagnosticsSensor(device, "Airco ID", CONF_AIRCO_ID),
                DiagnosticsSensor(device, "Operator ID", CONF_OPERATOR_ID, True),
                DiagnosticsSensor(device, "Device ID", ATTR_DEVICE_ID, True),
                DiagnosticsSensor(device, "IP", CONF_HOST, True),
                DiagnosticsSensor(device, "Accounts", ATTR_CONNECTED_ACCOUNTS, True),
                DiagnosticsSensor(device, "Error", CONF_ERROR),
            ]
            if device.airco.Electric is not None:
                entities.append(EnergySensor(device))

            async_add_entities(entities)

class DiagnosticsSensor(SensorEntity):
    # pylint: disable = too-many-instance-attributes
    """Representation of a Sensor."""

    _attr_entity_category: EntityCategory | None = EntityCategory.DIAGNOSTIC

    def __init__(
        self, device: Device, name: str, custom_type: str, enable=False
    ) -> None:
        """Initialize the sensor."""
        self._device = device
        self._attr_name = f"{device.name} {name}"
        self._attr_entity_registry_enabled_default = enable
        self._custom_type = custom_type
        self._attr_device_info = device.device_info
        self._attr_native_unit_of_measurement = (
            "Accounts" if custom_type == ATTR_CONNECTED_ACCOUNTS else None
        )
        self._attr_icon = (
            "mdi:account-group" if custom_type == ATTR_CONNECTED_ACCOUNTS else None
        )
        self._attr_unique_id = (
            f"{DOMAIN}-{self._device.airco_id}-{self._custom_type}-sensor"
        )
        self._update_state()

    def _update_state(self) -> None:
        if self._custom_type == CONF_OPERATOR_ID:
            self._attr_native_value = self._device.operator_id
        elif self._custom_type == CONF_AIRCO_ID:
            self._attr_native_value = self._device.airco_id
        elif self._custom_type == CONF_HOST:
            self._attr_native_value = self._device.host
        elif self._custom_type == ATTR_DEVICE_ID:
            self._attr_native_value = self._device.device_id
        elif self._custom_type == ATTR_CONNECTED_ACCOUNTS:
            self._attr_native_value = self._device.num_accounts
        elif self._custom_type == CONF_ERROR:
            self._attr_native_value = self._device.airco.ErrorCode

    async def async_update(self):
        """Retrieve latest state."""
        self._update_state()


class TemperatureSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_native_unit_of_measurement = TEMP_CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, device: Device, name: str, custom_type: str) -> None:
        """Initialize the sensor."""
        self._device = device
        self._custom_type = custom_type
        self._attr_name = f"{device.name} {name}"
        self._attr_device_info = device.device_info
        self._attr_unique_id = (
            f"{DOMAIN}-{self._device.airco_id}-{self._custom_type}-sensor"
        )
        self._update_state()

    def _update_state(self) -> None:
        if self._custom_type == ATTR_INSIDE_TEMPERATURE:
            self._attr_native_value = self._device.airco.IndoorTemp
        elif self._custom_type == ATTR_OUTSIDE_TEMPERATURE:
            self._attr_native_value = self._device.airco.OutdoorTemp

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Retrieve latest state."""
        self._update_state()


class EnergySensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_native_unit_of_measurement: str | None = ENERGY_KILO_WATT_HOUR
    _attr_device_class: SensorDeviceClass | str | None = SensorDeviceClass.ENERGY
    _attr_state_class: SensorStateClass | str | None = SensorStateClass.TOTAL_INCREASING

    def __init__(self, device: Device) -> None:
        """Initialize the sensor."""
        self._device = device
        self._attr_name = f"{device.name} energy usage cycle"
        self._attr_device_info = device.device_info
        self._attr_unique_id = f"{DOMAIN}-{self._device.airco_id}-energy-sensor"
        self._update_state()

    def _update_state(self) -> None:
        self._attr_native_value = self._device.airco.Electric

    async def async_update(self):
        """Retrieve latest state."""
        self._update_state()
