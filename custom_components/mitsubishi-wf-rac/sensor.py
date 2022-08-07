""" for sensor integration."""
from __future__ import annotations
from datetime import timedelta
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import TEMP_CELSIUS
from homeassistant.util import Throttle

from .wfrac.device import Device
from .const import DOMAIN, ATTR_INSIDE_TEMPERATURE, ATTR_OUTSIDE_TEMPERATURE

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=30)


async def async_setup_entry(hass, entry, async_add_entities):
    """Setup sensor entries"""

    for device in hass.data[DOMAIN]:
        if device.host == entry.data["host"]:
            _LOGGER.info("Setup: %s, %s", device.name, device.airco_id)
            entities = [TemperatureSensor(device, "Indoor", ATTR_INSIDE_TEMPERATURE)]
            entities.append(
                TemperatureSensor(device, "Outdoor", ATTR_OUTSIDE_TEMPERATURE)
            )
            async_add_entities(entities)


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
        await self._device.update()
        self._update_state()
