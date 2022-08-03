"""Device module"""
from datetime import timedelta
import logging

from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.util import Throttle

from .rac_parser import RacParser
from .repository import Repository
from .models.aircon import Aircon, AirconStat

_LOGGER = logging.getLogger(__name__)
MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=60)


class Device:
    """Device Class"""

    def __init__(
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

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def update(self):
        """Update the device information from API"""

        _raw_response = await self._hass.async_add_executor_job(
            self._api.get_aircon_stats
        )

        if _raw_response is None:
            self._available = False
            _LOGGER.debug("Received no data for device %s", self._airco_id)
            return

        self._airco = self._parser.translate_bytes(_raw_response)

    async def delete_account(self):
        """Delete account (operator id) from the airco"""

        try:
            await self._hass.async_add_executor_job(
                self._api.del_account_info,
                self._airco_id,
            )
        except Exception as ex:
            _LOGGER.debug("Could not delete account from airco %s", ex)

    async def set_airco(self, operation: bool):
        """Private method to send airco command"""

        if self.airco is None:
            await self._hass.async_add_executor_job(self.update)
            return  # return because there is nothing to send

        _airco_stat = AirconStat(self._airco)
        _airco_stat.Operation = operation
        _command = self._parser.to_base64(_airco_stat)
        try:
            _raw_response = await self._hass.async_add_executor_job(
                self._api.send_airco_command,
                self._airco_id,
                _command,
            )
        except Exception as ex:
            _LOGGER.debug("Could not send airco data %s", ex)

        self._airco = self._parser.translate_bytes(_raw_response)

    @property
    def operator_id(self) -> str:
        """Return Airco Operator ID"""
        return self._operator_id

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
