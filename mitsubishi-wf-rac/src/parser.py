from base64 import b64decode, b64encode
from .utils import Utils
from .constants import Constants
from .models.aircon import Aircon
from .models.airconStat import AirconStat


class Parser:

    def toBase64(airconStat: AirconStat):
        command = Parser.addCrc16(Parser.addVariable(Parser.CommandtoByte(airconStat)))
        receive = Parser.addCrc16(Parser.addVariable(Parser.RecievetoByte(airconStat)))
        
        return str(b64encode(bytes(command+receive)))[2:-1]


    def addVariable(ByteBuffer: bytearray):
        byteBuffer = ByteBuffer + [1, 255, 255, 255, 255]
        return byteBuffer

    def CommandtoByte(airconStat: AirconStat):
        airconStat: AirconStat = airconStat
        StatByte: bytearray = [0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        # On/Off
        if airconStat.Operation:
            StatByte[2] |= 3
        else:
            StatByte[2] |= 2
        
        #Operating Mode
        if airconStat.OperationMode == 0:
            StatByte[2] |= 32
        elif airconStat.OperationMode == 1:
            StatByte[2] |= 40
        elif airconStat.OperationMode == 2:
            StatByte[2] |= 48
        elif airconStat.OperationMode == 3:
            StatByte[2] |= 44
        elif airconStat.OperationMode == 4:
            StatByte[2] |= 36
            
        #airflow
        if airconStat.AirFlow == 0:
            StatByte[3] |= 15
        elif airconStat.AirFlow == 1:
            StatByte[3] |= 8
        elif airconStat.AirFlow == 2:
            StatByte[3] |= 9
        elif airconStat.AirFlow == 3:
            StatByte[3] |= 10
        elif airconStat.AirFlow == 4:
            StatByte[3] |= 14      
            
        # Vertical wind direction
        if airconStat.WindDirectionUD == 0:
            StatByte[2] |= 192
            StatByte[3] |= 128
        elif airconStat.WindDirectionUD == 1:
            StatByte[2] |= 128
            StatByte[3] |= 128
        elif airconStat.WindDirectionUD == 2:
            StatByte[2] |= 128
            StatByte[3] |= 144
        elif airconStat.WindDirectionUD == 3:
            StatByte[2] |= 128
            StatByte[3] |= 160
        elif airconStat.WindDirectionUD == 4:
            StatByte[2] |= 128
            StatByte[3] |= 176
            
        # Horizontal wind direction
        if airconStat.WindDirectionLR == 0:
            StatByte[12] |= 3
            StatByte[11] |= 16
        elif airconStat.WindDirectionLR == 1:
            StatByte[12] |= 2
            StatByte[11] |= 16
        elif airconStat.WindDirectionLR == 2:
            StatByte[12] |= 2
            StatByte[11] |= 17
        elif airconStat.WindDirectionLR == 3:
            StatByte[12] |= 2
            StatByte[11] |= 18
        elif airconStat.WindDirectionLR == 4:
            StatByte[12] |= 2
            StatByte[11] |= 19
        elif airconStat.WindDirectionLR == 5:
            StatByte[12] |= 2
            StatByte[11] |= 20
        elif airconStat.WindDirectionLR == 6:
            StatByte[12] |= 2
            StatByte[11] |= 21
        elif airconStat.WindDirectionLR == 7:
            StatByte[12] |= 2
            StatByte[11] |= 22
        
        #preset temp
        presetTemp = 25.0 if airconStat.OperationMode == 3 else airconStat.PresetTemp
        StatByte[4] |= (int(presetTemp/0.5) + 128)
        
        #entrust
        if not airconStat.Entrust:
            StatByte[12] |= 8
        else:
            StatByte[12] |= 12

        if not airconStat.CoolHotJudge:
            StatByte[8] |= 8
        
        if airconStat.ModelNr == 1:
            StatByte[10] |= 1 if airconStat.Vacant else 0
            
        if airconStat.ModelNr != 1 and airconStat.ModelNr != 2:
            return StatByte
    
        StatByte[10] |= (4 if airconStat.IsSelfCleanReset else 0)
        StatByte[10] |= (144 if airconStat.IsSelfCleanOperation else 128)

        return StatByte

    def RecievetoByte(airconStat: AirconStat):
        airconStat: AirconStat = airconStat
        StatByte: bytearray = [0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        # On/Off
        if airconStat.Operation:
            StatByte[2] |= 1
        
        #Operating Mode
        if airconStat.OperationMode == 1:
            StatByte[2] |= 8
        elif airconStat.OperationMode == 2:
            StatByte[2] |= 16
        elif airconStat.OperationMode == 3:
            StatByte[2] |= 12
        elif airconStat.OperationMode == 4:
            StatByte[2] |= 4
            
        #airflow
        if airconStat.AirFlow == 0:
            StatByte[3] |= 7
        elif airconStat.AirFlow == 2:
            StatByte[3] |= 1
        elif airconStat.AirFlow == 3:
            StatByte[3] |= 2
        elif airconStat.AirFlow == 4:
            StatByte[3] |= 6
            
        # Vertical wind direction
        if airconStat.WindDirectionUD == 0:
            StatByte[2] |= 64
        elif airconStat.WindDirectionUD == 2:
            StatByte[3] |= 16
        elif airconStat.WindDirectionUD == 3:
            StatByte[3] |= 32
        elif airconStat.WindDirectionUD == 4:
            StatByte[3] |= 48
            
        # Horizontal wind direction
        if airconStat.WindDirectionLR == 0:
            StatByte[12] |= 1
        elif airconStat.WindDirectionLR == 1:
            StatByte[11] |= 0
        elif airconStat.WindDirectionLR == 2:
            StatByte[11] |= 1
        elif airconStat.WindDirectionLR == 3:
            StatByte[11] |= 2
        elif airconStat.WindDirectionLR == 4:
            StatByte[11] |= 3
        elif airconStat.WindDirectionLR == 5:
            StatByte[11] |= 4
        elif airconStat.WindDirectionLR == 6:
            StatByte[11] |= 5
        elif airconStat.WindDirectionLR == 7:
            StatByte[11] |= 6
        
        #preset temp
        presetTemp = 25.0 if airconStat.OperationMode == 3 else airconStat.PresetTemp
        StatByte[4] |= int(presetTemp/0.5)
        
        #entrust
        if airconStat.Entrust:
            StatByte[12] |= 4

        if not airconStat.CoolHotJudge:
            StatByte[8] |= 8
            
        
        if airconStat.ModelNr == 1:
            StatByte[0] |= 1
        elif airconStat.ModelNr == 2:
            StatByte[0] |= 2

        if airconStat.ModelNr == 1:
            StatByte[10] |= 1 if airconStat.Vacant else 0
            
        if airconStat.ModelNr != 1 and airconStat.ModelNr != 2:
            return StatByte
    
        StatByte[15] |= (1 if airconStat.IsSelfCleanOperation else 0)


        return StatByte

    def translateBytes(inputString: str) -> Aircon:
        ac: Aircon = Aircon()
        # print(inputString)

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
        ac.ModelNr = Utils.findMatch(content[0] & 127, 0,1,2)
        ac.Vacant = content[10] & 1
        code = content[6] & 127
        ac.ErrorCode = ('00' if code == 0 else 'M{code:02d}'.format(
            code) if (content[6] & -128) <= 0 else "E" + code)

        valueSegment = contentByteArray[startLength + 19:len(contentByteArray) - 2]

        if(len(valueSegment) >= 8):
            ac.IndoorTemp = (Constants.indoorTemp[256 + valueSegment[2]])
            ac.OutdoorTemp = (Constants.outdoorTemp[256 + valueSegment[6]])
        if(len(valueSegment) >= 11):
            ac.Electric = (((valueSegment[11] << 8) + valueSegment[10]) * 0.25)

        return ac

    def crc16ccitt(data):
        # Convert to signed integers instead of bytes
        data = [(256-a) * (-1) if a > 127 else a for a in data]

        i = 65535
        for b in data:
            for i2 in range(8):
                z = True
                z2 = ((b>> (7-i2)) & 1) == 1
                if ((( i >> 15) & 1) != 1):
                    z = False
                i = i << 1
                if (z2 ^z):
                    i ^= 4129
        return i & 65535

    
    def addCrc16(ByteBuffer: bytearray):
        crc =  Parser.crc16ccitt(ByteBuffer)
        
        return ByteBuffer + [crc & 255, (crc >> 8) & 255]
        # return ByteBuffer + (crc.to_bytes(2, 'big'))