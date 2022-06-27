import json
from src.parser import Parser
from src.models.aircon import Aircon
from src.repository.repository import Repository
from src.utils import Utils
from base64 import b64decode

# slaapkamer = Parser.translateBytes(Repository.getAirconStats(ip='192.168.178.206'))
# raw = Repository.getAirconStats(ip='192.168.178.207')
raw = 'AACqn6z/AAAAAAAUCgAAAAAAAf/////dhgAACBcs/wAAAAAABAAAAAAAAAH/////oXY='
# raw = 'AACqn6z/AAAAAAAUCgAAAAAAAf////8CzwAACBcs/wAAAAAABAAAAAAAAAH/////GdA='

# print([x for x in b64decode(bytearray(raw1, encoding='UTF'))])
# print([x for x in b64decode(bytearray(raw, encoding='UTF'))])

woonkamer = Parser.translateBytes(raw)
slaapkamer = woonkamer
# slaapkamer = Parser.translateBytes('AACqn6z/AAAAAAAUCgAAAAAAAf/////dhgAACBcs/wAAAAAABAAAAAAAAAH/////oXY=')
# slaapkamer = Parser.translateBytes('AACrn6z/AAAAAAAUCgAAAAAAAf////8rU4AECRcsmAAAiAIABAAAAAAAAAKAIJj/gBC4//tX')

# slaapkamer = Parser.translateBytes('AACqn6z/AAAAAAAQDgAAAAAAAf////97xwAACBcs/wAAAAAAAAQAAAAAAAH/////YNg=')
# slaapkamer = Parser.translateBytes(Repository.sendAircoCommand(command='AACqn6z/AAAAAAAUCgAAAAAAAf/////dhgAACBcs/wAAAAAABAAAAAAAAAH/////oXY=', ip='192.168.178.207'))

# print(slaapkamer)

#convert to JSON string
jsonStr = json.dumps(slaapkamer.__dict__, sort_keys=False, indent=4)

#print json string
print(jsonStr)

outputJson = (Parser.toBase64(airconStat=Utils.convertAirconToAirconStat(slaapkamer)))
# print(outputJson)
print(json.dumps(Parser.translateBytes(outputJson).__dict__, sort_keys=False, indent=4))