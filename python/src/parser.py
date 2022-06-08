from base64 import b64decode
from utils import Utils
from constants import Constants

class Parser:
    def translateBytes(inputString: str):
        contentByteArray = b64decode(bytearray(inputString, encoding='UTF'))
        startLength = contentByteArray[18] * 4 + 21
        content = contentByteArray[startLength:startLength+18]

        Operation = 1 == (3 & content[2])
        PresetTemp = content[4] / 2.0
        OperationMode = (Utils.findMatch(60 & content[2], 8, 16, 12, 4) + 1)
        AirFlow = (Utils.findMatch(15 & content[3], 7, 0, 1, 2, 6));
        WindDirectionUD = ((Utils.findMatch(240 & content[3], 0, 16, 31, 48) + 1))
        WindDirectionLR = (Utils.findMatch(31 & content[11], 0, 1, 2, 3, 4, 5, 6) + 1)
        Entrust = (4 == (12 & content[12]))
        CoolHotJudge = ((content[8] & 8) <= 0)

        code = content[6] & 127
        ErrorCode = ('00' if code == 0 else 'M{code:02d}'.format(code) if (content[6] & -128) <= 0 else "E" + code)

        valueSegment = contentByteArray[startLength + 19:len(contentByteArray) - 2]

        print(valueSegment[6])
        IndoorTemp = (Constants.indoorTemp[256 - valueSegment[2]])
        OutdoorTemp = (Constants.outdoorTemp[256 - valueSegment[6]])
        Electric = (((valueSegment[11] << 8) + valueSegment[10]) * 0.25)

        print('Indoor Temp:\t\t' + str(IndoorTemp) + ' C')
        print('Outdoor Temp:\t\t' + str(OutdoorTemp) + ' C')
        print('Preset Temp:\t\t' + str(PresetTemp))
        print('Operation:\t\t' + str(Operation))
        print('Operation Mode:\t\t' + str(OperationMode))
        print('Air Flow:\t\t' + str(AirFlow))
        print('Direction UP/DOWN:\t' + str(WindDirectionUD))
        print('Direction LEFT/RIGHT:\t' + str(WindDirectionLR))
        print('3D Auto:\t\t' + str(Entrust))
        print('Error Code:\t\t' + ErrorCode)
        print('Electric:\t\t' + str(Electric))
 
Parser.translateBytes('AACqj6j/AAAAAAAQCgAAAAAAAf////9FqIAECAcojgAAiAAAAAAAAAAAAAOAII7/gBCW/5QQAADrgg==')