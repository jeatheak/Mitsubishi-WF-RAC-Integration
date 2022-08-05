"""Config flow WF-RAC"""
from __future__ import annotations

import logging
from typing import Any
from uuid import uuid4

import voluptuous as vol

from homeassistant.components import zeroconf
from homeassistant import config_entries, exceptions
from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
    CONF_NAME,
    CONF_BASE,
    CONF_DEVICE_ID,
)
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import CONF_OPERATOR_ID, CONF_AIRCO_ID, DOMAIN
from .wfrac.repository import Repository

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME, description={"suggested_value": "Airco unknown"}): str,
        vol.Required(CONF_HOST): str,
        vol.Optional(CONF_PORT, default=51443): int,
    }
)


class WfRacConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL
    _discovery_info = {}
    DOMAIN = DOMAIN

    async def _async_validate_input(
        self, hass: HomeAssistant, data: dict
    ) -> dict[str, Any]:
        """Validate the user input allows us to connect."""
        if len(data[CONF_HOST]) < 3:
            raise InvalidHost

        if len(data[CONF_NAME]) < 3:
            raise InvalidName

        for entry in self._async_current_entries():
            already_configured = False

            if CONF_HOST in entry.data and entry.data[CONF_HOST] in (data[CONF_HOST]):
                # Is this address or IP address already configured?
                already_configured = True

            if already_configured:
                raise HostAlreadyConfigured

        repository = Repository(
            data[CONF_HOST],
            data[CONF_PORT],
            data[CONF_OPERATOR_ID],
            data[CONF_DEVICE_ID],
        )

        airco_id = await hass.async_add_executor_job(repository.get_details)
        data[CONF_AIRCO_ID] = airco_id
        if not airco_id:
            raise CannotConnect

        _LOGGER.info(
            "Trying to register OperatorId[%s] on Airco[%s]",
            data[CONF_OPERATOR_ID],
            data[CONF_AIRCO_ID],
        )
        result = await hass.async_add_executor_job(
            repository.update_account_info, airco_id
        )
        if not result:
            raise CannotConnect

        return {"title": data[CONF_NAME]}

    async def _async_fetch_operator_id(self):
        """Fetch UUID operator id if exists otherwise create it"""
        for entry in self._async_current_entries():
            if CONF_OPERATOR_ID in entry.data:
                return entry.data[CONF_OPERATOR_ID]

        return f"hassio-{str(uuid4())[7:]}"

    async def _async_fetch_device_id(self):
        """Fetch unique device id if exists otherwise create it"""
        for entry in self._async_current_entries():
            if CONF_DEVICE_ID in entry.data:
                return entry.data[CONF_DEVICE_ID]

        return f"homeassistant-device-{uuid4().hex[21:]}"

    async def async_step_discovery_confirm(self, user_input=None):
        """Handle the initial step."""

        errors = {}
        if user_input is not None:
            try:
                user_input[CONF_HOST] = self._discovery_info[CONF_HOST]
                user_input[CONF_PORT] = self._discovery_info[CONF_PORT]

                user_input[CONF_OPERATOR_ID] = await self._async_fetch_operator_id()
                user_input[CONF_DEVICE_ID] = await self._async_fetch_device_id()

                info = await self._async_validate_input(self.hass, user_input)

                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect:
                errors[CONF_BASE] = "cannot_connect"
            except InvalidHost:
                errors[CONF_HOST] = "cannot_connect"
            except HostAlreadyConfigured:
                errors[CONF_HOST] = "host_already_configured"
            except InvalidName:
                errors[CONF_NAME] = "name_invalid"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors[CONF_BASE] = "unknown"

        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form(
            step_id="discovery_confirm",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_NAME, default=f"Airco {self._discovery_info[CONF_NAME]}"
                    ): str,
                }
            ),
            errors=errors,
            description_placeholders={
                "id": self._discovery_info[CONF_NAME],
                "host": self._discovery_info[CONF_HOST],
                "port": self._discovery_info[CONF_PORT],
            },
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

                user_input[CONF_OPERATOR_ID] = await self._async_fetch_operator_id()
                user_input[CONF_DEVICE_ID] = await self._async_fetch_device_id()

                info = await self._async_validate_input(self.hass, user_input)

                _LOGGER.warning(
                    f"Got {user_input[CONF_OPERATOR_ID]} and {user_input[CONF_DEVICE_ID]}"
                )

                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect:
                errors[CONF_BASE] = "cannot_connect"
            except InvalidHost:
                errors[CONF_HOST] = "cannot_connect"
            except HostAlreadyConfigured:
                errors[CONF_HOST] = "host_already_configured"
            except InvalidName:
                errors[CONF_NAME] = "name_invalid"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors[CONF_BASE] = "unknown"

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


class HostAlreadyConfigured(exceptions.HomeAssistantError):
    """Error to indicate there is an duplicate hostname."""


class InvalidName(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid hostname."""
