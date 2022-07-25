"""The WF-RAC sensor integration."""
import logging

import asyncio
from async_timeout import timeout
from typing import Any, Dict

import voluptuous as vol

from homeassistant.components.zeroconf import async_get_instance
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import HomeAssistantType

from homeassistant.const import CONF_HOSTS, CONF_PORT

from .const import DOMAIN
from .wfrac.device import Device

_LOGGER = logging.getLogger(__name__)

WF_RAC_DEVICES = "wf-rac-devices"


def setup(hass, config):
    pass


async def async_setup(hass: HomeAssistant, config: Dict) -> bool:
    """Set up the Garo Wallbox component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Establish connection with mitsubishi-wf-rac."""

    if WF_RAC_DEVICES not in hass.data:
        hass.data[WF_RAC_DEVICES] = ["192.168.178.206"]

    devices = CONF_HOSTS
    port = CONF_PORT

    for device in devices:
        try:
            api = Device(hass, device, port)
            await api.update()
            hass.data[WF_RAC_DEVICES].append(api)
        except Exception as ex:
            _LOGGER.warning(
                "Something whent wrong setting up device [%s] %s", device, ex
            )

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    return True


async def async_unload_entry(hass, config_entry):
    """Unload a config entry."""
    await asyncio.wait(
        [hass.config_entries.async_forward_entry_unload(config_entry, "sensor")]
    )
    hass.data.pop(WF_RAC_DEVICES)

    return True
