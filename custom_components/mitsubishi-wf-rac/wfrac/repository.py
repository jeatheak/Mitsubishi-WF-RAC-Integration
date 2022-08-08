"""Local API for sending and receiving to and from WF-RAC module"""

import time
from requests import post


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

    def get_details(self) -> str:
        """Simple command to get aircon details"""
        url = f"http://{self._hostname}:{self._port}/beaver/command/getDeviceInfo"
        myobj = {
            "apiVer": self.api_version,
            "command": "getDeviceInfo",
            "deviceId": self._device_id,  # is unique device ID (on android it is called android_id)
            "operatorId": self._operator_id,  # is generated UUID
            "timestamp": round(time.time()),
        }

        return post(url, json=myobj).json()["contents"]["airconId"]

    def update_account_info(self, airco_id: str, time_zone: str) -> str:
        """Update the account info on the airco (sets to operator id of the device)"""
        url = f"http://{self._hostname}:{self._port}/beaver/command/updateAccountInfo"
        myobj = {
            "apiVer": self.api_version,
            "command": "updateAccountInfo",
            "deviceId": self._device_id,  # is unique device ID (on android it is called android_id)
            "operatorId": self._operator_id,  # is generated UUID
            "contents": {
                "accountId": self._operator_id,
                "airconId": airco_id,
                "remote": 0,
                "timezone": time_zone,
            },
            "timestamp": round(time.time()),
        }

        return post(url, json=myobj).json()

    def del_account_info(self, airco_id: str) -> str:
        """delete the account info on the airco"""
        url = f"http://{self._hostname}:{self._port}/beaver/command/deleteAccountInfo"
        myobj = {
            "apiVer": self.api_version,
            "command": "deleteAccountInfo",
            "deviceId": self._device_id,  # is unique device ID (on android it is called android_id)
            "operatorId": self._operator_id,  # is generated UUID
            "contents": {"accountId": self._operator_id, "airconId": airco_id},
            "timestamp": round(time.time()),
        }

        return post(url, json=myobj).json()

    def get_aircon_stats(self, raw=False) -> str:
        """Get the Aricon Stats from the Airco"""
        url = f"http://{self._hostname}:{self._port}/beaver/command/getAirconStat"
        myobj = {
            "apiVer": self.api_version,
            "command": "getAirconStat",
            "deviceId": self._device_id,  # is unique device ID (on android it is called android_id)
            "operatorId": self._operator_id,  # is generated UUID
            "timestamp": round(time.time()),
        }

        if raw is True:
            return post(url, json=myobj).json()

        return post(url, json=myobj).json()["contents"]

    def send_airco_command(self, airco_id: str, command: str) -> str:
        """send command to the Airco"""
        url = f"http://{self._hostname}:{self._port}/beaver/command/setAirconStat"
        myobj = {
            "apiVer": self.api_version,
            "command": "setAirconStat",
            "contents": {"airconId": airco_id, "airconStat": command},
            "deviceId": self._device_id,  # is unique device ID (on android it is called android_id)
            "operatorId": self._operator_id,  # is generated UUID
            "timestamp": round(time.time()),
        }

        # return post(url, json=myobj).json()
        return post(url, json=myobj).json()["contents"]["airconStat"]
