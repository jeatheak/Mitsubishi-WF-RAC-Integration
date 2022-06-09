from src.parser import Parser
from src.models.aircon import Aircon
from src.repository.repository import Repository

# slaapkamer = Parser.translateBytes(Repository.getAirconStats(ip='192.168.178.206'))
# woonkamer = Parser.translateBytes(Repository.getAirconStats(ip='192.168.178.207'))

slaapkamer = Parser.translateBytes('AACriKr/AAAAAAAQCgAAAAAAAf////+1WQAACQAq/wAAAAAAAAAAAAAAAAH/////yak=')

print('Operation:\t' + str(slaapkamer.Operation))
print('OperationMode:\t' + str(slaapkamer.OperationMode))
print('AirFlow:\t' + str(slaapkamer.AirFlow))
print('WindDirectionUD:' + str(slaapkamer.WindDirectionUD))
print('WindDirectionLR:' + str(slaapkamer.WindDirectionLR))
print('PresetTemp:\t' + str(slaapkamer.PresetTemp))
print('Entrust:\t' + str(slaapkamer.Entrust))
print('ModelNr:\t' + str(slaapkamer.ModelNr))
print('Vacant:\t\t' + str(slaapkamer.Vacant))