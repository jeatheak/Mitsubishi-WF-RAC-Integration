""" for sensor integration."""
from __future__ import annotations
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import CONF_ICON, CONF_NAME, TEMP_CELSIUS, CONF_TYPE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .wfrac.device import Device
from . import WF_RAC_DEVICES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    for device in hass.data[WF_RAC_DEVICES]:
        entities = [TemperatureSensor(device, "Indoor")]
        async_add_entities(entities)


class TemperatureSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_native_unit_of_measurement = TEMP_CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, api: Device, name: str) -> None:
        """Initialize the sensor."""
        self._api = api
        self._attr_name = name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._api.airco.IndoorTemp

    async def async_update(self):
        """Retrieve latest state."""
        await self._api.update()
