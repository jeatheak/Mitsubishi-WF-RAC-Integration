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

from homeassistant.const import CONF_HOST, CONF_PORT, CONF_NAME

from .const import DOMAIN
from .wfrac.device import Device

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Establish connection with mitsubishi-wf-rac."""

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = []

    device = entry.data[CONF_HOST]
    name = entry.data[CONF_NAME]
    port: int = entry.data[CONF_PORT]

    try:
        api = Device(hass, name, device, port)
        await api.update()
        hass.data[DOMAIN].append(api)
    except Exception as ex:
        _LOGGER.warning("Something whent wrong setting up device [%s] %s", device, ex)

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    return True


async def async_unload_entry(hass, config_entry):
    """Unload a config entry."""
    await asyncio.wait(
        [hass.config_entries.async_forward_entry_unload(config_entry, "sensor")]
    )
    if DOMAIN in hass.data:
        hass.data.pop(DOMAIN)

    return True
