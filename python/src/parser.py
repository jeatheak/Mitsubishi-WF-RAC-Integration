from base64 import b64decode
from .utils import Utils
from .constants import Constants
from .models.aircon import Aircon


class Parser:
    def translateBytes(inputString: str) -> Aircon:
        ac: Aircon = Aircon()

        # convert to byte array
        contentByteArray = b64decode(bytearray(inputString, encoding='UTF'))
        # Convert to signed integers instead of bytes
        contentByteArray = [(256-a) * (-1) if a >
                            127 else a for a in contentByteArray]

        # get te start of the first bytearray segment we use
        startLength = contentByteArray[18] * 4 + 21
        # copy the bytearray segment to variable
        content = contentByteArray[startLength:startLength+18]

        # get the current ac operation (3th value and with byte 3)
        ac.Operation = 1 == (3 & content[2])
        # get preset temp: 5th byte divided by 2
        ac.PresetTemp = content[4] / 2
        # get operation mode: check if 3th byte and byte 60 matches 8,16,12 or 4 (add 1)
        ac.OperationMode = (Utils.findMatch(60 & content[2], 8, 16, 12, 4) + 1)
        ac.AirFlow = (Utils.findMatch(15 & content[3], 7, 0, 1, 2, 6))
        ac.WindDirectionUD = (
            (Utils.findMatch(240 & content[3], 0, 16, 31, 48) + 1))
        ac.WindDirectionLR = (Utils.findMatch(
            31 & content[11], 0, 1, 2, 3, 4, 5, 6) + 1)
        ac.Entrust = (4 == (12 & content[12]))
        ac.CoolHotJudge = ((content[8] & 8) <= 0)

        code = content[6] & 127
        ac.ErrorCode = ('00' if code == 0 else 'M{code:02d}'.format(
            code) if (content[6] & -128) <= 0 else "E" + code)

        valueSegment = contentByteArray[startLength +
                                        19:len(contentByteArray) - 2]

        ac.IndoorTemp = (Constants.indoorTemp[256 + valueSegment[2]])
        ac.OutdoorTemp = (Constants.outdoorTemp[256 + valueSegment[6]])
        # ac.Electric = (((valueSegment[11] << 8) + valueSegment[10]) * 0.25)

        return ac
