package src.refactor;

import java.util.Arrays;
import java.util.Base64;
import java.util.Locale;

import src.AirconStat;

public class SmallDecoder {
    public static AirconStat fromBase64(AirconStat airconStat, String str) {
        return translateBytesToAirconStat(Base64.getDecoder().decode(str.replace("\n", "")));
    }

    private static final double ELECTRIC_ENERGY_COFFICIENT = 0.25d;

    private static AirconStat translateBytesToAirconStat(byte[] contentByteArray) {
        AirconStat airconStat = new AirconStat();
        int startLength = contentByteArray[18] * 4 + 21;
        byte[] content = Arrays.copyOfRange(contentByteArray, startLength, startLength + 18);

        // setters \\
        airconStat.setOperation(1 == (3 & content[2]) ? 1 : 0);
        airconStat.setPresetTemp(content[4] / 2.0d);
        airconStat.setOperationMode(Utils.findMatch(60 & content[2], 8, 16, 12, 4) + 1);
        airconStat.setAirFlow(Utils.findMatch(15 & content[3], 7, 0, 1, 2, 6));
        airconStat.setWindDirectionUD((Utils.findMatch(240 & content[3], 0, 16, 31, 48) + 1));
        airconStat.setWindDirectionLR(Utils.findMatch(31 & content[11], 0, 1, 2, 3, 4, 5, 6) + 1);
        airconStat.setEntrust(4 == (12 & content[12]) ? 1 : 0);
        airconStat.setCoolHotJudge((content[8] & 8) <= 0 ? 1 : 0);

        // Error code \\
        int code = content[6] & 127;
        airconStat.setErrorCode(code == 0 ? "00"
                : (content[6] & -128) <= 0 ? "M" + String.format(Locale.US, "%02d", code) : "E" + code);

        // Get IndoorTemp, OutdoorTemp and electric \\
        byte[] valueSegment = Arrays.copyOfRange(contentByteArray, startLength + 19,
                contentByteArray.length - 2);

        System.out.println(valueSegment[6]);
        airconStat.setIndoorTemp(Constants.indoorTemp[256 + valueSegment[2]]);
        airconStat.setOutdoorTemp(Constants.outdoorTemp[256 + valueSegment[6]]);
        airconStat.setElectric(((valueSegment[11] << 8) + valueSegment[10]) * ELECTRIC_ENERGY_COFFICIENT);

        return airconStat;
    }

}
