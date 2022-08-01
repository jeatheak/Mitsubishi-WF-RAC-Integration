"""Config flow WF-RAC"""
from __future__ import annotations

import logging
from uuid import uuid4
from typing import Any

import voluptuous as vol

from homeassistant.components import zeroconf, onboarding
from homeassistant import config_entries, exceptions
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN  # pylint:disable=unused-import
from .wfrac.repository import Repository

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME, description={"suggested_value": "Airco unknown"}): str,
        vol.Required(CONF_HOST): str,
        vol.Optional(CONF_PORT, default=51443): int,
    }
)


async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    if len(data["host"]) < 3:
        raise InvalidHost

    if len(data["name"]) < 3:
        raise InvalidName

    repository = Repository(data["host"], data["port"])
    result = await hass.async_add_executor_job(repository.get_details)
    if not result:
        raise CannotConnect

    return {"title": data["name"]}


class WfRacConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL
    _discovery_info = {}
    DOMAIN = DOMAIN

    async def async_step_discovery_confirm(self, user_input=None):
        """Handle the initial step."""

        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)

                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidHost:
                errors["host"] = "cannot_connect"
            except InvalidName:
                errors["name"] = "name_invalid"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form(
            step_id="discovery_confirm",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_NAME, default=f"Airco {self._discovery_info[CONF_NAME]}"
                    ): str,
                    vol.Required(
                        CONF_HOST, default=self._discovery_info[CONF_HOST]
                    ): str,
                    vol.Required(
                        CONF_PORT, default=self._discovery_info[CONF_PORT]
                    ): vol.Coerce(int),
                }
            ),
            errors=errors,
            description_placeholders={"name": self._name},
        )

    async def async_step_zeroconf(
        self, discovery_info: zeroconf.ZeroconfServiceInfo
    ) -> FlowResult:
        """Handle zeroconf discovery."""

        local_name = discovery_info.hostname[:-1]
        node_name = local_name[: -len(".local")]
        host = discovery_info.host
        port = discovery_info.port

        await self.async_set_unique_id(node_name)
        self._abort_if_unique_id_configured(updates={CONF_HOST: discovery_info.host})

        for entry in self._async_current_entries():
            already_configured = False

            if CONF_HOST in entry.data and entry.data[CONF_HOST] in (
                host,
                discovery_info.host,
            ):
                # Is this address or IP address already configured?
                already_configured = True

            if already_configured:
                return self.async_abort(reason="already_configured")

        self._discovery_info = {CONF_HOST: host, CONF_NAME: node_name, CONF_PORT: port}

        return await self.async_step_discovery_confirm()

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""

        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)

                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidHost:
                errors["host"] = "cannot_connect"
            except InvalidName:
                errors["name"] = "name_invalid"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )

    @property
    def _name(self) -> str | None:
        return self.context.get(CONF_NAME)


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidHost(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid hostname."""


class InvalidName(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid hostname."""
