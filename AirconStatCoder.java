
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Base64;
import java.util.List;
import java.util.stream.Collectors;

/* renamed from: jp.co.mhi_mth.smartmair.util.AirconStatCoder */
public class AirconStatCoder {
    private static final int[] COMMAND_OPERATION_MODE2_OFF = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 0, 0, 0, 0, 0 };
    private static final int[] COMMAND_OPERATION_MODE2_ON = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 144, 0, 0, 0, 0, 0 };
    private static final int[] COMMAND_SELF_CLEAN_RESET_ON = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] COMMAND_SELF_CLEAN_RESET_OFF = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] COMMAND_VACANT_PROPERTY_OFF = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] COMMAND_VACANT_PROPERTY_ON = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] STATUS_MODEL_NO_TYPE_GLOBAL_2022 = { 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0 };
    private static final int[] STATUS_MODEL_NO_TYPE_HIGH_END_FOR_JAPANESE_2023 = { 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0 };
    private static final int[] STATUS_MODEL_NO_TYPE_SEPARATE_2021;

    private static final int[] STATUS_OPERATION_MODE2_OFF;
    private static final int[] STATUS_OPERATION_MODE2_ON = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0 };
    private static final int[] STATUS_VACANT_PROPERTY_MAX_BIT;
    private static final int[] STATUS_VACANT_PROPERTY_OFF;
    private static final int[] STATUS_VACANT_PROPERTY_ON;
    private static final String TAG = "AirconStatCoder";
    private static final int[] af_n_00 = { 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] af_n_01 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] af_n_02 = { 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] af_n_03 = { 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] af_n_04 = { 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] af_p_00 = { 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] af_p_01 = { 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] af_p_02 = { 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] af_p_03 = { 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] af_p_04 = { 0, 0, 0, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] as_n_of = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] as_n_on = { 0, 0, 64, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] as_p_of = { 0, 0, 128, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] as_p_on = { 0, 0, 192, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] av_n_of = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] av_n_on = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0 };
    private static final int[] av_p_of = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0 };
    private static final int[] av_p_on = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0 };
    private static final int[] receive_init = { 0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] command_init = { 0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] en_n_of = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] en_n_on = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0 };
    private static final int[] en_p_of = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0 };
    private static final int[] en_p_on = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 0, 0, 0, 0 };
    private static final int[] lh_n_01 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] lh_n_02 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0 };
    private static final int[] lh_n_03 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0 };
    private static final int[] lh_n_04 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0 };
    private static final int[] lh_n_05 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0 };
    private static final int[] lh_n_06 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0 };
    private static final int[] lh_n_07 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0 };
    private static final int[] lh_p_01 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 0, 0, 0, 0, 0, 0 };
    private static final int[] lh_p_02 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 17, 0, 0, 0, 0, 0, 0 };
    private static final int[] lh_p_03 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 18, 0, 0, 0, 0, 0, 0 };
    private static final int[] lh_p_04 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 19, 0, 0, 0, 0, 0, 0 };
    private static final int[] lh_p_05 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 0, 0, 0, 0, 0, 0 };
    private static final int[] lh_p_06 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 21, 0, 0, 0, 0, 0, 0 };
    private static final int[] lh_p_07 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 0, 0, 0, 0, 0, 0 };
    private static final int[] lv_n_01 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] lv_n_02 = { 0, 0, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] lv_n_03 = { 0, 0, 0, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] lv_n_04 = { 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] lv_p_01 = { 0, 0, 0, 128, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] lv_p_02 = { 0, 0, 0, 144, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] lv_p_03 = { 0, 0, 0, 160, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] lv_p_04 = { 0, 0, 0, 176, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] om_n_au = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] om_n_dn = { 0, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] om_n_jo = { 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] om_n_re = { 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] om_n_so = { 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] om_p_au = { 0, 0, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] om_p_dn = { 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] om_p_jo = { 0, 0, 36, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] om_p_re = { 0, 0, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] om_p_so = { 0, 0, 44, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] op_n_of = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] op_n_on = { 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] op_p_of = { 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] op_p_on = { 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] tm_p_au = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] tm_p_no = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] zeros;

    static {
        int[] iArr = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
        zeros = iArr;
        STATUS_MODEL_NO_TYPE_SEPARATE_2021 = iArr;
        STATUS_VACANT_PROPERTY_OFF = iArr;
        int[] iArr2 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0 };
        STATUS_VACANT_PROPERTY_ON = iArr2;
        STATUS_VACANT_PROPERTY_MAX_BIT = iArr2;
        STATUS_OPERATION_MODE2_OFF = iArr;
    }

    public static String toBase64(AirconStat airconStat) {
        return Base64
                .getEncoder().encodeToString(
                        concat(
                                addCrc16(addCommandVariableData(commandToByte(airconStat))).array(),
                                addCrc16(addReceiveVariableData(receiveToByte(airconStat))).array()));
    }

    private static ByteBuffer commandToByte(AirconStat airconStat) {
        ByteBuffer byteBuffer;
        ByteBuffer byteBuffer2;
        ByteBuffer bytes = toBytes(command_init);
        if (airconStat.getOperation() == 1) {
            byteBuffer = orBytes(bytes, toBytes(op_p_on));
        } else {
            byteBuffer = orBytes(bytes, toBytes(op_p_of));
        }
        int operationMode = airconStat.getOperationMode();
        if (operationMode == 0) {
            byteBuffer = orBytes(byteBuffer, toBytes(om_p_au));
        } else if (operationMode == 1) {
            byteBuffer = orBytes(byteBuffer, toBytes(om_p_re));
        } else if (operationMode == 2) {
            byteBuffer = orBytes(byteBuffer, toBytes(om_p_dn));
        } else if (operationMode == 3) {
            byteBuffer = orBytes(byteBuffer, toBytes(om_p_so));
        } else if (operationMode == 4) {
            byteBuffer = orBytes(byteBuffer, toBytes(om_p_jo));
        }
        int airFlow = airconStat.getAirFlow();
        if (airFlow == 0) {
            byteBuffer = orBytes(byteBuffer, toBytes(af_p_00));
        } else if (airFlow == 1) {
            byteBuffer = orBytes(byteBuffer, toBytes(af_p_01));
        } else if (airFlow == 2) {
            byteBuffer = orBytes(byteBuffer, toBytes(af_p_02));
        } else if (airFlow == 3) {
            byteBuffer = orBytes(byteBuffer, toBytes(af_p_03));
        } else if (airFlow == 4) {
            byteBuffer = orBytes(byteBuffer, toBytes(af_p_04));
        }
        int windDirectionUD = airconStat.getWindDirectionUD();
        if (windDirectionUD == 0) {
            byteBuffer = orBytes(orBytes(byteBuffer, toBytes(as_p_on)), toBytes(lv_p_01));
        } else if (windDirectionUD == 1) {
            byteBuffer = orBytes(orBytes(byteBuffer, toBytes(as_p_of)), toBytes(lv_p_01));
        } else if (windDirectionUD == 2) {
            byteBuffer = orBytes(orBytes(byteBuffer, toBytes(as_p_of)), toBytes(lv_p_02));
        } else if (windDirectionUD == 3) {
            byteBuffer = orBytes(orBytes(byteBuffer, toBytes(as_p_of)), toBytes(lv_p_03));
        } else if (windDirectionUD == 4) {
            byteBuffer = orBytes(orBytes(byteBuffer, toBytes(as_p_of)), toBytes(lv_p_04));
        }
        int windDirectionLR = airconStat.getWindDirectionLR();
        if (windDirectionLR == 0) {
            byteBuffer = orBytes(orBytes(byteBuffer, toBytes(av_p_on)), toBytes(lh_p_01));
        } else if (windDirectionLR == 1) {
            byteBuffer = orBytes(orBytes(byteBuffer, toBytes(av_p_of)), toBytes(lh_p_01));
        } else if (windDirectionLR == 2) {
            byteBuffer = orBytes(orBytes(byteBuffer, toBytes(av_p_of)), toBytes(lh_p_02));
        } else if (windDirectionLR == 3) {
            byteBuffer = orBytes(orBytes(byteBuffer, toBytes(av_p_of)), toBytes(lh_p_03));
        } else if (windDirectionLR == 4) {
            byteBuffer = orBytes(orBytes(byteBuffer, toBytes(av_p_of)), toBytes(lh_p_04));
        } else if (windDirectionLR == 5) {
            byteBuffer = orBytes(orBytes(byteBuffer, toBytes(av_p_of)), toBytes(lh_p_05));
        } else if (windDirectionLR == 6) {
            byteBuffer = orBytes(orBytes(byteBuffer, toBytes(av_p_of)), toBytes(lh_p_06));
        } else if (windDirectionLR == 7) {
            byteBuffer = orBytes(orBytes(byteBuffer, toBytes(av_p_of)), toBytes(lh_p_07));
        }
        double presetTemp = airconStat.getOperationMode() == 3 ? 25.0d : airconStat.getPresetTemp();
        int[] iArr = zeros;
        iArr[4] = ((int) (presetTemp / 0.5d)) + 128;
        ByteBuffer orBytes = orBytes(byteBuffer, toBytes(iArr));
        if (airconStat.getEntrust() == 0) {
            byteBuffer2 = orBytes(orBytes, toBytes(en_p_of));
        } else {
            byteBuffer2 = orBytes(orBytes, toBytes(en_p_on));
        }
        if (airconStat.getModelNo() == 1) {
            byteBuffer2 = orBytes(byteBuffer2,
                    toBytes(airconStat.isVacantProperty() ? COMMAND_VACANT_PROPERTY_ON : COMMAND_VACANT_PROPERTY_OFF));
        }
        int modelNo = airconStat.getModelNo();
        if (modelNo != 1 && modelNo != 2) {
            return byteBuffer2;
        }
        return orBytes(
                orBytes(byteBuffer2,
                        toBytes(airconStat.isSelfCleanReset() ? COMMAND_SELF_CLEAN_RESET_ON
                                : COMMAND_SELF_CLEAN_RESET_OFF)),
                toBytes(airconStat.isSelfCleanOperation() ? COMMAND_OPERATION_MODE2_ON : COMMAND_OPERATION_MODE2_OFF));
    }

    private static ByteBuffer receiveToByte(AirconStat airconStat) {
        ByteBuffer byteBuffer;
        ByteBuffer byteBuffer2;
        ByteBuffer bytes = toBytes(receive_init);
        if (airconStat.getOperation() == 1) {
            byteBuffer = orBytes(bytes, toBytes(op_n_on));
        } else {
            byteBuffer = orBytes(bytes, toBytes(op_n_of));
        }
        int operationMode = airconStat.getOperationMode();
        if (operationMode == 0) {
            byteBuffer = orBytes(byteBuffer, toBytes(om_n_au));
        } else if (operationMode == 1) {
            byteBuffer = orBytes(byteBuffer, toBytes(om_n_re));
        } else if (operationMode == 2) {
            byteBuffer = orBytes(byteBuffer, toBytes(om_n_dn));
        } else if (operationMode == 3) {
            byteBuffer = orBytes(byteBuffer, toBytes(om_n_so));
        } else if (operationMode == 4) {
            byteBuffer = orBytes(byteBuffer, toBytes(om_n_jo));
        }
        int airFlow = airconStat.getAirFlow();
        if (airFlow == 0) {
            byteBuffer = orBytes(byteBuffer, toBytes(af_n_00));
        } else if (airFlow == 1) {
            byteBuffer = orBytes(byteBuffer, toBytes(af_n_01));
        } else if (airFlow == 2) {
            byteBuffer = orBytes(byteBuffer, toBytes(af_n_02));
        } else if (airFlow == 3) {
            byteBuffer = orBytes(byteBuffer, toBytes(af_n_03));
        } else if (airFlow == 4) {
            byteBuffer = orBytes(byteBuffer, toBytes(af_n_04));
        }
        int windDirectionUD = airconStat.getWindDirectionUD();
        if (windDirectionUD == 0) {
            byteBuffer = orBytes(orBytes(byteBuffer, toBytes(as_n_on)), toBytes(lv_n_01));
        } else if (windDirectionUD == 1) {
            byteBuffer = orBytes(orBytes(byteBuffer, toBytes(as_n_of)), toBytes(lv_n_01));
        } else if (windDirectionUD == 2) {
            byteBuffer = orBytes(orBytes(byteBuffer, toBytes(as_n_of)), toBytes(lv_n_02));
        } else if (windDirectionUD == 3) {
            byteBuffer = orBytes(orBytes(byteBuffer, toBytes(as_n_of)), toBytes(lv_n_03));
        } else if (windDirectionUD == 4) {
            byteBuffer = orBytes(orBytes(byteBuffer, toBytes(as_n_of)), toBytes(lv_n_04));
        }
        int windDirectionLR = airconStat.getWindDirectionLR();
        if (windDirectionLR == 0) {
            byteBuffer = orBytes(orBytes(byteBuffer, toBytes(av_n_on)), toBytes(lh_n_01));
        } else if (windDirectionLR == 1) {
            byteBuffer = orBytes(orBytes(byteBuffer, toBytes(av_n_of)), toBytes(lh_n_01));
        } else if (windDirectionLR == 2) {
            byteBuffer = orBytes(orBytes(byteBuffer, toBytes(av_n_of)), toBytes(lh_n_02));
        } else if (windDirectionLR == 3) {
            byteBuffer = orBytes(orBytes(byteBuffer, toBytes(av_n_of)), toBytes(lh_n_03));
        } else if (windDirectionLR == 4) {
            byteBuffer = orBytes(orBytes(byteBuffer, toBytes(av_n_of)), toBytes(lh_n_04));
        } else if (windDirectionLR == 5) {
            byteBuffer = orBytes(orBytes(byteBuffer, toBytes(av_n_of)), toBytes(lh_n_05));
        } else if (windDirectionLR == 6) {
            byteBuffer = orBytes(orBytes(byteBuffer, toBytes(av_n_of)), toBytes(lh_n_06));
        } else if (windDirectionLR == 7) {
            byteBuffer = orBytes(orBytes(byteBuffer, toBytes(av_n_of)), toBytes(lh_n_07));
        }
        double presetTemp = airconStat.getOperationMode() == 3 ? 25.0d : airconStat.getPresetTemp();
        int[] iArr = zeros;
        iArr[4] = (int) (presetTemp / 0.5d);
        ByteBuffer orBytes = orBytes(byteBuffer, toBytes(iArr));
        if (airconStat.getEntrust() == 0) {
            byteBuffer2 = orBytes(orBytes, toBytes(en_n_of));
        } else {
            byteBuffer2 = orBytes(orBytes, toBytes(en_n_on));
        }
        int[] iArr2 = STATUS_MODEL_NO_TYPE_SEPARATE_2021;
        int modelNo = airconStat.getModelNo();
        if (modelNo == 1) {
            iArr2 = STATUS_MODEL_NO_TYPE_GLOBAL_2022;
        } else if (modelNo == 2) {
            iArr2 = STATUS_MODEL_NO_TYPE_HIGH_END_FOR_JAPANESE_2023;
        }

        ByteBuffer orBytes2 = orBytes(byteBuffer2, toBytes(iArr2));
        if (airconStat.getModelNo() == 1) {
            orBytes2 = orBytes(orBytes2,
                    toBytes(airconStat.isVacantProperty() ? STATUS_VACANT_PROPERTY_ON : STATUS_VACANT_PROPERTY_OFF));
        }
        int modelNo2 = airconStat.getModelNo();
        if (modelNo2 != 1 && modelNo2 != 2) {
            return orBytes2;
        }
        return orBytes(orBytes2,
                toBytes(airconStat.isSelfCleanOperation() ? STATUS_OPERATION_MODE2_ON : STATUS_OPERATION_MODE2_OFF));
    }

    private static ByteBuffer addCommandVariableData(ByteBuffer byteBuffer) {
        return ByteBuffer.wrap(concat(byteBuffer.array(), toBytes(new int[] { 1, 255, 255, 255, 255 }).array()));
    }

    private static ByteBuffer addReceiveVariableData(ByteBuffer byteBuffer) {
        return ByteBuffer.wrap(concat(byteBuffer.array(), toBytes(new int[] { 1, 255, 255, 255, 255 }).array()));
    }

    private static ByteBuffer addCrc16(ByteBuffer byteBuffer) {
        int crc16ccitt = crc16ccitt(byteBuffer.array());
        return ByteBuffer.wrap(
                concat(byteBuffer.array(), new byte[] { toByte(crc16ccitt & 255), toByte((crc16ccitt >> 8) & 255) }));
    }

    private static byte[] concat(byte[] bArr, byte[] bArr2) {
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        try {
            byteArrayOutputStream.write(bArr);
            byteArrayOutputStream.write(bArr2);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        return byteArrayOutputStream.toByteArray();
    }

    private static ByteBuffer toBytes(int[] iArr) {
        ByteBuffer allocate = ByteBuffer.allocate(iArr.length);
        for (int i : iArr) {
            allocate.put(toByte(i));
        }
        return allocate;
    }

    private static byte toByte(int i) {
        return Arrays.copyOfRange(ByteBuffer.allocate(4).putInt(i).array(), 3, 4)[0];
    }

    private static ByteBuffer orBytes(ByteBuffer byteBuffer, ByteBuffer byteBuffer2) {
        int length = byteBuffer.array().length;
        byteBuffer.rewind();
        byteBuffer2.rewind();
        ByteBuffer allocate = ByteBuffer.allocate(length);
        for (int i = 0; i < length; i++) {
            allocate.put((byte) (byteBuffer.get() | byteBuffer2.get()));
        }
        return allocate;
    }

    private static int crc16ccitt(byte[] bArr) {
        int i = 65535;
        for (byte b : bArr) {
            for (int i2 = 0; i2 < 8; i2++) {
                boolean z = true;
                boolean z2 = ((b >> (7 - i2)) & 1) == 1;
                if (((i >> 15) & 1) != 1) {
                    z = false;
                }
                i <<= 1;
                if (z2 ^ z) {
                    i ^= 4129;
                }
            }
        }
        return i & 65535;
    }

    private static void putArrayToList(List<Integer> list, int[] iArr) {
        list.addAll((List) Arrays.stream(iArr).boxed().collect(Collectors.toList()));
    }
}
