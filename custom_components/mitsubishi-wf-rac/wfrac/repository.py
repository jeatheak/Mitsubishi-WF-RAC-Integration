"""Local API for sending and receiving to and from WF-RAC module"""
from __future__ import annotations

import time
import logging
import threading

from typing import Any
from datetime import datetime, timedelta

import requests

_LOGGER = logging.getLogger(__name__)
# log http requests/responses to separate logger, to allow easily turning on/off from
# configuration.yaml
_HTTP_LOG = _LOGGER.getChild("http")

# ensure that we don't overwhelm the aircon unit by waiting at least
# this long between successive requests
_MIN_TIME_BETWEEN_REQUESTS = timedelta(seconds=1)

class Repository:
    """Simple Api class to send and get Aircon information"""

    api_version = "1.0"

    def __init__(
        self, hostname: str, port: int, operator_id: str, device_id: str
    ) -> None:
        self._hostname = hostname
        self._port = port
        self._operator_id = operator_id
        self._device_id = device_id
        self._mutex = threading.Lock()
        self._next_request_after = datetime.now()

    def _post(self,
              command: str,
              contents: dict[str, Any] | None = None) -> dict:
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
        with self._mutex:
            wait_for = (self._next_request_after - datetime.now()).total_seconds()
            if wait_for > 0:
                _LOGGER.debug("Waiting for %r until we can send a request", wait_for)
                # TODO: make this whole thing async so we don't
                # actually tie up a thread while we wait
                time.sleep(wait_for)
            _HTTP_LOG.debug("POSTing to %s: %r",
                            url,
                            data)
            response = requests.post(url, json=data)
            _HTTP_LOG.debug("Got response (%r) from %r: %r",
                            response.status_code,
                            self._hostname,
                            response.text)
            self._next_request_after = datetime.now() + _MIN_TIME_BETWEEN_REQUESTS

        # raise an exception if the airco returned an error
        response.raise_for_status()

        return response.json()

    def get_info(self) -> str:
        """Simple command to get aircon details"""
        return self._post("getDeviceInfo")["contents"]

    def get_airco_id(self) -> str:
        """Simple command to get aircon ID"""
        return self.get_info()["airconId"]

    def update_account_info(self, airco_id: str, time_zone: str) -> str:
        """Update the account info on the airco (sets to operator id of the device)"""
        contents = {
            "accountId": self._operator_id,
            "airconId": airco_id,
            "remote": 0,
            "timezone": time_zone,
        }
        return self._post("updateAccountInfo", contents)

    def del_account_info(self, airco_id: str) -> str:
        """delete the account info on the airco"""
        contents = {
            "accountId": self._operator_id,
            "airconId": airco_id
        }
        return self._post("deleteAccountInfo", contents)

    def get_aircon_stats(self, raw=False) -> str:
        """Get the Aricon Stats from the Airco"""
        result = self._post("getAirconStat")
        return result if raw else result["contents"]

    def send_airco_command(self, airco_id: str, command: str) -> str:
        """send command to the Airco"""
        contents = {
            "airconId": airco_id,
            "airconStat": command
        }
        result = self._post("setAirconStat", contents)
        return result["contents"]["airconStat"]
