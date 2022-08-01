"""The WF-RAC sensor integration."""
import logging

import asyncio
from typing import Dict

import voluptuous as vol

from homeassistant.components.zeroconf import async_get_instance
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import HomeAssistantType

from homeassistant.const import CONF_HOST, CONF_PORT, CONF_NAME, CONF_DEVICE_ID

from .const import DOMAIN, CONF_OPERATOR_ID
from .wfrac.device import Device

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Establish connection with mitsubishi-wf-rac."""

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = []

    device = entry.data[CONF_HOST]
    name = entry.data[CONF_NAME]
    device_id = entry.data[CONF_DEVICE_ID]
    operator_id = entry.data[CONF_OPERATOR_ID]
    port: int = entry.data[CONF_PORT]

    try:
        api = Device(hass, name, device, port, device_id, operator_id)
        await api.update()
        hass.data[DOMAIN].append(api)
    except Exception as ex:
        _LOGGER.warning("Something whent wrong setting up device [%s] %s", device, ex)

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    return True


async def async_unload_entry(hass, entry: ConfigEntry):
    """Unload a config entry."""
    await asyncio.wait(
        [hass.config_entries.async_forward_entry_unload(entry, "sensor")]
    )

    for device in hass.data[DOMAIN]:
        temp_device: Device = device
        if temp_device.host == entry.data[CONF_HOST]:
            _LOGGER.warning("Delete %s, %s", temp_device.host, temp_device.name)
            try:
                await temp_device.delete_account()
            except Exception as ex:
                _LOGGER.warning(
                    "Something whent wrong deleting account from airco [%s] %s",
                    temp_device.name,
                    ex,
                )

    return True
