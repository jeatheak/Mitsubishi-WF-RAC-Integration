from .models.aircon import Aircon
from .models.airconStat import AirconStat

class Utils:
    def convertAirconToAirconStat(aircon: Aircon) -> AirconStat:
        airconStat: AirconStat = AirconStat()

        airconStat.Operation = aircon.Operation
        airconStat.OperationMode = aircon.OperationMode
        airconStat.CoolHotJudge = aircon.CoolHotJudge
        airconStat.AirFlow = aircon.AirFlow
        airconStat.WindDirectionUD = aircon.WindDirectionUD
        airconStat.WindDirectionLR = aircon.WindDirectionLR
        airconStat.PresetTemp = aircon.PresetTemp
        airconStat.Entrust = aircon.Entrust
        airconStat.ModelNr = aircon.ModelNr
        airconStat.Vacant = aircon.Vacant

        airconStat.IsSelfCleanOperation = 0
        airconStat.IsSelfCleanReset = 0

        return airconStat

    def findMatch(content, *inputMatrix):
        i = 0
        for value in inputMatrix:
            if (value == content):
                return i
            i += 1

        return -1