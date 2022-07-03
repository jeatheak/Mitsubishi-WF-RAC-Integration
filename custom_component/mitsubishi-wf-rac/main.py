import json
from src.parser import Parser
from src.models.aircon import Aircon
from src.repository.repository import Repository
from src.utils import Utils
from base64 import b64decode

woonkamer = Parser.translateBytes(Repository.getAirconStats(ip='192.168.178.207'))
print(woonkamer.IndoorTemp)

# outputJson = Parser.toBase64(airconStat=Utils.convertAirconToAirconStat(woonkamer))
# response = Parser.translateBytes(Repository.sendAircoCommand(command=outputJson, ip='192.168.178.207'))

# convertedAircon = json.dumps(response.__dict__, sort_keys=False, indent=4)
# print(convertedAircon)