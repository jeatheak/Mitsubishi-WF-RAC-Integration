""" for switch integration."""
from __future__ import annotations
from datetime import timedelta
from typing import Any
import logging

from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity, ConfigEntry
from homeassistant.util import Throttle
from homeassistant.const import CONF_HOST

from .wfrac.device import MIN_TIME_BETWEEN_UPDATES, Device
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=30)


async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities):
    """Setup switch entities"""
    for device in hass.data[DOMAIN]:
        if device.host == entry.data[CONF_HOST]:
            _LOGGER.info("Setup switch for: %s, %s", device.name, device.airco_id)
            async_add_entities([AircoSwitch(device)])


class AircoSwitch(SwitchEntity):
    """Representation of a Switch."""

    _attr_device_class: SwitchDeviceClass | str | None = SwitchDeviceClass.SWITCH

    def __init__(self, api: Device) -> None:
        """Initialize the sensor."""
        self._device = api
        self._attr_name = f"{api.name} Switch"
        self._attr_unique_id = f"{DOMAIN}-{self._device.airco_id}-switch"
        self._attr_is_on = self._device.airco.Operation

    async def async_turn_on(self, **kwargs):
        """Turn on nanoe."""
        await self._device.set_airco(True)
        self._attr_is_on = self._device.airco.Operation

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        await self._device.set_airco(False)
        self._attr_is_on = self._device.airco.Operation

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Retrieve latest state."""
        await self._device.update()
        self._attr_is_on = self._device.airco.Operation
