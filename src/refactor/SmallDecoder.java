package src.refactor;

import java.nio.ByteBuffer;
import java.nio.charset.Charset;
import java.util.Arrays;
import java.util.Base64;
import java.util.Locale;

import src.AirconStat;
import src.ByteCompanionObject;

public class SmallDecoder {
    public static AirconStat fromBase64(AirconStat airconStat, String str) {
        return translateBytesToAirconStat(Base64.getDecoder().decode(str.replace("\n", "")));
        // return byteToStat(airconStat, Base64.getDecoder().decode(str.replace("\n",
        // "")));
    }

    private static final double ELECTRIC_ENERGY_COFFICIENT = 0.25d;

    private static final int[] om_n_au = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] om_n_op = { 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] om_n_dn = { 0, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] om_n_jo = { 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] om_n_re = { 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] om_n_so = { 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] op_n_on = { 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] op_p_on = { 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };

    private static final int[] av_n_on = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0 };
    private static final int[] av_p_of = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0 };
    private static final int[] av_p_on = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0 };

    private static final int[] as_n_on = { 0, 0, 64, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] as_p_of = { 0, 0, 128, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] as_p_on = { 0, 0, 192, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };

    private static final int[] en_n_of = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] en_n_on = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0 };
    private static final int[] en_p_of = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0 };
    private static final int[] en_p_on = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 0, 0, 0, 0 };

    private static final int[] af_n_00 = { 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] af_n_01 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] af_n_02 = { 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] af_n_03 = { 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] af_n_04 = { 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] af_p_00 = { 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] af_p_on = { 0, 0, 0, 240, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };

    private static final int[] lv_n_01 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] lv_n_02 = { 0, 0, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] lv_n_03 = { 0, 0, 0, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] lv_n_04 = { 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };

    private static final int[] lh_n_01 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] lh_n_02 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0 };
    private static final int[] lh_n_03 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0 };
    private static final int[] lh_n_04 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0 };
    private static final int[] lh_n_05 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0 };
    private static final int[] lh_n_06 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0 };
    private static final int[] lh_n_07 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0 };
    private static final int[] lh_n_on = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 31, 0, 0, 0, 0, 0, 0 };

    private static AirconStat translateBytesToAirconStat(byte[] contentByteArray) {
        AirconStat airconStat = new AirconStat();
        int startLength = contentByteArray[18] * 4 + 21; // ((ByteBuffer.wrap(contentByteArray).position(18).get() & -1)
                                                         // * 4) + 21;
        ByteBuffer contentWrapper = ByteBuffer
                .wrap(Arrays.copyOfRange(contentByteArray, startLength, startLength + 18));

        // setOperation \\
        airconStat.setOperation(Utils.compare(op_n_on, Utils.and(op_p_on, contentWrapper)) ? 1 : 0);

        // setPresetTemp \\
        airconStat.setPresetTemp((contentWrapper.position(4).get() & -1) / 2.0d);

        // setOperationMode \\
        airconStat.setOperationMode(
                Utils.getMatch(Utils.and(om_n_op, contentWrapper), om_n_re, om_n_dn, om_n_so, om_n_jo) + 1);

        // setAirFlow \\
        airconStat.setAirFlow(
                Utils.getMatch(Utils.and(af_p_00, contentWrapper), af_n_00, af_n_01, af_n_02, af_n_03, af_n_04));

        // setWindDirectionUD \\
        airconStat.setWindDirectionUD(
                (Utils.getMatch(Utils.and(af_p_on, contentWrapper), lv_n_01, lv_n_02, lv_n_03, lv_n_04) + 1));

        // setWindDirectionLR \\
        airconStat.setWindDirectionLR(
                Utils.getMatch(Utils.and(lh_n_on, contentWrapper), lh_n_01, lh_n_02, lh_n_03, lh_n_04, lh_n_05, lh_n_06,
                        lh_n_07) + 1);

        // setEntrust \\
        ByteBuffer entrustWrapper = Utils.and(en_p_on, contentWrapper);
        airconStat.setEntrust(Utils.equal(en_n_on, entrustWrapper) ? 1 : 0);

        // Error code \\
        byte errorByte = contentWrapper.position(6).get();
        int code = errorByte & ByteCompanionObject.MAX_VALUE;
        if ((errorByte & ByteCompanionObject.MIN_VALUE) <= 0) {
            airconStat.setErrorCode("M".concat(String.format(Locale.US, "%02d", Integer.valueOf(code))));
        } else {
            airconStat.setErrorCode("E".concat(String.valueOf(code)));
        }
        if (code == 0) {
            airconStat.setErrorCode("00");
        }

        // setCoolHutJudge \\
        airconStat.setCoolHotJudge((contentWrapper.position(8).get() & 8) <= 0 ? 1 : 0);

        // TODO: MODELNUMBER \\

        // Get IndoorTemp, OutdoorTemp and electric \\
        byte[] copyOfRange = Arrays.copyOfRange(contentByteArray, startLength + 19,
                contentByteArray.length - 2);
        ByteBuffer tempWrapper = ByteBuffer.wrap(copyOfRange);

        for (int segment = 0; segment < copyOfRange.length / 4; segment++) {
            int startPos = segment * 4;
            byte b = tempWrapper.position(startPos).get();
            byte b2 = tempWrapper.position(startPos + 1).get();
            byte b3 = tempWrapper.position(startPos + 2).get();
            byte b4 = tempWrapper.position(startPos + 3).get();
            if (b == Utils.toByte(128) && b2 == Utils.toByte(16)) {
                airconStat.setOutdoorTemp(Double.valueOf(Constants.outdoorTemp[255 - ~b3]).doubleValue());
            } else {
                if (b == Utils.toByte(128) && b2 == Utils.toByte(32)) {
                    airconStat.setIndoorTemp(Constants.indoorTemp[255 - ~b3]);
                } else if (b == Utils.toByte(148) && b2 == Utils.toByte(16)) {
                    airconStat.setElectric((((b4 & -1) << 8) + (b3 & -1)) * ELECTRIC_ENERGY_COFFICIENT);
                }
            }
        }

        return airconStat;
    }

}
