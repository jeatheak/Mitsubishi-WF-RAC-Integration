"""Device module"""
from datetime import timedelta
from typing import Any
import logging

from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.util import Throttle

from .rac_parser import RacParser
from .repository import Repository
from .models.aircon import Aircon, AirconStat, AirconCommands

from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)
MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=60)


class Device:  # pylint: disable=too-many-instance-attributes
    """Device Class"""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        hass: HomeAssistantType,
        name: str,
        hostname: str,
        port: int,
        device_id: str,
        operator_id: str,
        airco_id: str,
    ) -> None:
        self._api = Repository(hostname, port, operator_id, device_id)
        self._parser = RacParser()
        self._hass = hass

        self._airco = None
        self._operator_id = operator_id
        self._device_id = device_id
        self._host = hostname
        self._port = port
        self._airco_id = airco_id
        self._available = True
        self._name = name
        self._firmware = ""
        self._connected_accounts = -1

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def update(self):
        """Update the device information from API"""

        try:
            _raw_response = await self._hass.async_add_executor_job(
                self._api.get_aircon_stats
            )

            if _raw_response is None:
                self._available = False
                _LOGGER.warning("Received no data for device %s", self._airco_id)
                return
        except Exception as ex:  # pylint: disable=broad-except
            _LOGGER.error(
                "Error: something whent wrong updating the airco [%s] valus - error: %s",
                self.name,
                ex,
            )
            return

        self._connected_accounts = _raw_response["numOfAccount"]
        self._firmware = f'{_raw_response["firmType"]}, mcu: {_raw_response["mcu"]["firmVer"]}, wireless: {_raw_response["wireless"]["firmVer"]}'
        self._airco = self._parser.translate_bytes(_raw_response["airconStat"])

    async def delete_account(self):
        """Delete account (operator id) from the airco"""

        try:
            _raw_response = await self._hass.async_add_executor_job(
                self._api.del_account_info,
                self._airco_id,
            )
        except Exception as ex:  # pylint: disable=broad-except
            _LOGGER.debug("Could not delete account from airco %s", ex)
            return

        return _raw_response

    async def add_account(self):
        """Add account (operator id) from the airco"""

        try:
            _raw_response = await self._hass.async_add_executor_job(
                self._api.update_account_info,
                self._airco_id,
                self._hass.config.time_zone,
            )
        except Exception as ex:  # pylint: disable=broad-except
            _LOGGER.debug("Could not add account from airco %s", ex)
            return

        return _raw_response

    async def set_airco(self, params: dict[AirconCommands, Any]) -> None:
        """Private method to send airco command"""

        if self.airco is None:
            await self._hass.async_add_executor_job(self.update)

        _airco_stat = AirconStat(self._airco)

        try:
            for command in params:
                setattr(_airco_stat, command, params[command])
        except Exception:  # pylint: disable=broad-except
            _LOGGER.warning("Could not find command [%s] in Airco Object!")
            return

        _command = self._parser.to_base64(_airco_stat)
        try:
            _raw_response = await self._hass.async_add_executor_job(
                self._api.send_airco_command,
                self._airco_id,
                _command,
            )
        except Exception as ex:  # pylint: disable=broad-except
            _LOGGER.debug("Could not send airco data %s", ex)

        self._airco = self._parser.translate_bytes(_raw_response)

    @property
    def device_info(self) -> DeviceInfo:
        """Return a device description for device registry."""
        return {
            "sw_version": self._firmware,
            "identifiers": {(DOMAIN, self.airco_id)},
            "manufacturer": "Mitsubishi (WF-RAC)",
            # "model": self.airco.ModelNr,
            "name": self.name,
        }

    @property
    def operator_id(self) -> str:
        """Return Airco Operator ID"""
        return self._operator_id

    @property
    def num_accounts(self) -> str:
        """Return Accounts connected"""
        return self._connected_accounts

    @property
    def device_id(self) -> str:
        """Return Airco device ID"""
        return self._device_id

    @property
    def host(self) -> str:
        """Get Host (IP)"""
        return self._host

    @property
    def port(self) -> int:
        """Get Port"""
        return self._port

    @property
    def name(self) -> str:
        """Get given Airco name"""
        return self._name

    @property
    def airco_id(self) -> str:
        """Return Airco ID"""
        return self._airco_id

    @property
    def airco(self) -> Aircon:
        """Return parsed Aircon object if set otherwise None"""
        return self._airco
