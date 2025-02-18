"""Local API for sending and receiving to and from WF-RAC module"""

from __future__ import annotations

import time
import logging
import asyncio
import functools
from threading import RLock

from typing import Any
from datetime import datetime, timedelta
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

import requests
from requests.exceptions import RequestException

_LOGGER = logging.getLogger(__name__)
# log http requests/responses to separate logger, to allow easily turning on/off from
# configuration.yaml
_HTTP_LOG = _LOGGER.getChild("http")

# ensure that we don't overwhelm the aircon unit by waiting at least
# this long between successive requests
_MIN_TIME_BETWEEN_REQUESTS = timedelta(seconds=1)

class AirconApiError(HomeAssistantError):
    """Raised when the aircon API returns an error"""
    pass

class Repository:
    """Simple Api class to send and get Aircon information"""

    api_version = "1.0"

    def __init__(  # pylint: disable=too-many-arguments
        self,
        hass: HomeAssistant,
        hostname: str,
        port: int,
        operator_id: str,
        device_id: str,
    ) -> None:
        self._hass = hass
        self._hostname = hostname
        self._port = port
        self._operator_id = operator_id
        self._device_id = device_id
        # Use both asyncio.Lock for async operations and RLock for sync operations
        self._mutex = asyncio.Lock()
        self._sync_lock = RLock()
        self._next_request_after = datetime.now()
        self._session = requests.Session()

    async def _post(
        self, command: str, contents: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        url = f"http://{self._hostname}:{self._port}/beaver/command/{command}"
        data = {
            "apiVer": self.api_version,
            "command": command,
            "deviceId": self._device_id,  # is unique device ID (on android it is called android_id)
            "operatorId": self._operator_id,  # is generated UUID
            "timestamp": round(time.time()),
        }
        if contents is not None:
            data["contents"] = contents

        # ensure only one thread is talking to the device at a time
        async with self._mutex:
            wait_for = (self._next_request_after - datetime.now()).total_seconds()
            if wait_for > 0:
                _LOGGER.debug("Waiting for %rs until we can send a request", wait_for)
                await asyncio.sleep(wait_for)

            # _HTTP_LOG.debug("POSTing to %s: %r", url, data)
            try:
                with self._sync_lock:
                    response = await self._hass.async_add_executor_job(
                        functools.partial(
                            self._session.post,
                            url,
                            json=data,
                            timeout=30
                        )
                    )
            except RequestException as ex:
                _HTTP_LOG.warning("Error POSTing to %s: %s", url, ex)
                raise AirconApiError(f"Failed to communicate with aircon: {ex}") from ex

            # _HTTP_LOG.debug(
            #     "Got response (%r) from %r: %r",
            #     response.status_code,
            #     self._hostname,
            #     response.text,
            # )

            # Update next request time under lock protection
            self._next_request_after = datetime.now() + _MIN_TIME_BETWEEN_REQUESTS

        try:
            response.raise_for_status()
        except RequestException as ex:
            raise AirconApiError(f"Aircon returned error: {ex}") from ex

        try:
            return response.json()
        except ValueError as ex:
            raise AirconApiError(f"Invalid JSON response from aircon: {ex}") from ex

    async def get_info(self) -> dict:
        """Simple command to get aircon details"""
        return (await self._post("getDeviceInfo"))["contents"]

    async def get_airco_id(self) -> str:
        """Simple command to get aircon ID"""
        return (await self.get_info())["airconId"]

    async def update_account_info(
        self, airco_id: str, time_zone: str
    ) -> dict[str, Any]:
        """Update the account info on the airco (sets to operator id of the device)"""
        contents = {
            "accountId": self._operator_id,
            "airconId": airco_id,
            "remote": 0,
            "timezone": time_zone,
        }
        return await self._post("updateAccountInfo", contents)

    async def del_account_info(self, airco_id: str) -> dict:
        """delete the account info on the airco"""
        contents = {"accountId": self._operator_id, "airconId": airco_id}
        return await self._post("deleteAccountInfo", contents)

    async def get_aircon_stats(self, raw=False) -> dict:
        """Get the Aricon Stats from the Airco"""
        result = await self._post("getAirconStat")
        return result if raw else result["contents"]

    async def send_airco_command(self, airco_id: str, command: str) -> str:
        """send command to the Airco"""
        contents = {"airconId": airco_id, "airconStat": command}
        result = await self._post("setAirconStat", contents)
        return result["contents"]["airconStat"]

    def __del__(self):
        """Cleanup resources"""
        if hasattr(self, '_session'):
            with self._sync_lock:
                self._session.close()
