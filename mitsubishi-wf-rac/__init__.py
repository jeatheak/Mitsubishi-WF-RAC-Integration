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

from .const import CONF_AIRCO_ID, DOMAIN, CONF_OPERATOR_ID
from .wfrac.device import Device

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Establish connection with mitsubishi-wf-rac."""

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = []

    device: str = entry.data[CONF_HOST]
    name: str = entry.data[CONF_NAME]
    device_id: str = entry.data[CONF_DEVICE_ID]
    operator_id: str = entry.data[CONF_OPERATOR_ID]
    port: int = entry.data[CONF_PORT]
    airco_id: str = entry.data[CONF_AIRCO_ID]

    try:
        api = Device(hass, name, device, port, device_id, operator_id, airco_id)
        await api.update()  # initial update to get fresh values
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
            try:
                await temp_device.delete_account()
                _LOGGER.info(
                    "Deleted operator ID [%s] from airco [%s]",
                    temp_device.operator_id,
                    temp_device.airco_id,
                )
                hass.data[DOMAIN].remove(temp_device)
            except Exception as ex:
                _LOGGER.warning(
                    "Something whent wrong deleting account from airco [%s] %s",
                    temp_device.name,
                    ex,
                )

    if DOMAIN in hass.data:
        if len(hass.data[DOMAIN]) <= 0:
            hass.data.pop(DOMAIN)

    return True
