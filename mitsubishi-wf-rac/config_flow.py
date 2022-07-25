"""Config flow WF-RAC"""
from __future__ import annotations
from datetime import timedelta

import logging
from typing import Any
from aiohttp import ClientConnectionError

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
)
from homeassistant.data_entry_flow import FlowResult
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.typing import ConfigType
from homeassistant.util import Throttle

from .src.models.aircon import Aircon
from .src.models.device import Device
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=60)


# async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
#     """Establish connection"""
#     if DOMAIN not in config:
#         return True

#     username = config[DOMAIN][CONF_USERNAME]
#     token = config[DOMAIN][CONF_TOKEN]
#     hass.async_create_task(
#         hass.config_entries.flow.async_init(
#             DOMAIN,
#             context={"source": SOURCE_IMPORT},
#             data={CONF_USERNAME: username, CONF_TOKEN: token},
#         )
#     )
#     return True


# async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
#     """Establish connection with MELClooud."""
#     conf = entry.data
#     mel_devices = await mel_devices_setup(hass, conf[CONF_TOKEN])
#     hass.data.setdefault(DOMAIN, {}).update({entry.entry_id: mel_devices})
#     hass.config_entries.async_setup_platforms(entry, PLATFORMS)
#     return True


# async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
#     """Unload a config entry."""
#     unload_ok = await hass.config_entries.async_unload_platforms(
#         config_entry, PLATFORMS
#     )
#     hass.data[DOMAIN].pop(config_entry.entry_id)
#     if not hass.data[DOMAIN]:
#         hass.data.pop(DOMAIN)
#     return unload_ok


class WfRacConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    def __init__(self) -> None:
        """Init the lookin flow."""
        self._host: str | None = None
        self._port: str | None = None

    async def _show_setup_form(
        self, errors: dict[str, str] | None = None
    ) -> FlowResult:
        """Show the setup form to the user."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_PORT, default=3000): vol.Coerce(int),
                }
            ),
            errors=errors or {},
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initiated by the user."""
        if user_input is None:
            return await self._show_setup_form(user_input)

        self._async_abort_entries_match(
            {CONF_HOST: user_input[CONF_HOST], CONF_PORT: user_input[CONF_PORT]}
        )

        errors = {}

        session = async_get_clientsession(self.hass, False)

        airconDevice: Aircon = ()
