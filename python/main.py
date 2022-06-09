from src.parser import Parser
from src.models.aircon import Aircon
from src.repository.repository import Repository

slaapkamer = Parser.translateBytes(Repository.getAirconStats(ip='192.168.178.206'))
woonkamer = Parser.translateBytes(Repository.getAirconStats(ip='192.168.178.207'))

print(slaapkamer.IndoorTemp)
print(woonkamer.IndoorTemp)