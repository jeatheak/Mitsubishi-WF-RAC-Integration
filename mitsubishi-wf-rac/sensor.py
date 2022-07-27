""" for sensor integration."""
from __future__ import annotations
from datetime import timedelta
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import CONF_ICON, CONF_NAME, TEMP_CELSIUS, CONF_TYPE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.util import Throttle

from .wfrac.device import Device
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=60)

# def setup_platform(hass, config, add_entities, discovery_info=None):
#     """Set up platform."""
#     for device in hass.data[DEVICES]:
#         entities = [TemperatureSensor(device, "Indoor")]
#         add_entities(entities)


async def async_setup_entry(hass, entry, async_add_entities):
    for device in hass.data[DOMAIN]:
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
    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def state(self):
        """Return the state of the sensor."""
        _LOGGER.info("Update: %s", self._api.airco_id)
        return self._api.airco.IndoorTemp

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Retrieve latest state."""
        await self._api.update()
