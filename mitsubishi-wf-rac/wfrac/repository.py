"""Local API for sending and receiving to and from WF-RAC module"""

import time
from requests import post


class DetailResponse:
    """Model to store the airco details in"""

    airco_id: str
    operator_id: str

    def __init__(self, airco_id: str, operator_id: str) -> None:
        self.airco_id = airco_id
        self.operator_id = operator_id


class Repository:
    """Simple Api class to send and get Aircon information"""

    api_version = "1.0"

    def __init__(self, hostname: str, port: int) -> None:
        self._hostname = hostname
        self._port = port

    def get_details(self) -> DetailResponse:
        """Simple command to get aircon details"""
        url = f"http://{self._hostname}:{self._port}/beaver/command/getAirconStat"
        myobj = {
            "apiVer": self.api_version,
            "command": "getAirconStat",
            "deviceId": "1",  # can be random, till aws api is added
            "operatorId": "1",  # not known at the moment
            "timestamp": round(time.time()),
        }

        response = post(url, json=myobj).json()["contents"]

        return DetailResponse(response["airconId"], response["remoteList"][0])

    def update_account_info(self, operator_id: str, airco_id: str) -> str:
        """Update the account info on the airco (sets to operator id of the device)"""
        url = f"http://{self._hostname}:{self._port}/beaver/command/updateAccountInfo"
        myobj = {
            "apiVer": self.api_version,
            "command": "updateAccountInfo",
            "deviceId": "1",  # can be random, till aws api is added
            "operatorId": operator_id,
            "contents": {
                "accountId": operator_id,
                "airconId": airco_id,
                "remote": 0,  # TODO: test what difference it will make to set it to 1 (True, add it to remoteList?)
                "timezone": "Europe/Amsterdam",  # TODO: change to auto generate
            },
            "timestamp": round(time.time()),
        }

        return post(url, json=myobj).json()["contents"]["airconStat"]

    def get_aircon_stats(
        self,
        operator_id: str,
    ) -> str:
        """Get the Aricon Stats from the Airco"""
        url = f"http://{self._hostname}:{self._port}/beaver/command/getAirconStat"
        myobj = {
            "apiVer": self.api_version,
            "command": "getAirconStat",
            "deviceId": "1",  # can be random, till aws api is added
            "operatorId": operator_id,
            "timestamp": round(time.time()),
        }

        return post(url, json=myobj).json()["contents"]["airconStat"]

    def send_airco_command(self, operator_id: str, airco_id: str, command: str) -> str:
        """send command to the Airco"""
        url = f"http://{self._hostname}:{self._port}/beaver/command/setAirconStat"
        myobj = {
            "apiVer": self.api_version,
            "command": "setAirconStat",
            "contents": {"airconId": airco_id, "airconStat": command},
            "deviceId": "1",  # can be random, till aws api is added
            "operatorId": operator_id,
            "timestamp": round(time.time()),
        }

        return post(url, json=myobj).json()["contents"]["airconStat"]
