package src;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Base64;
import java.util.List;
import java.util.Locale;
import java.util.stream.Collectors;

public class AirconStatCoder {
    private static final double[] outdoorTemp = { -50.0, -50.0, -50.0, -50.0, -50.0, -48.9, -46.0, -44.0, -42.0, -41.0,
            -39.0, -38.0,
            -37.0, -36.0, -35.0, -34.0, -33.0, -32.0, -31.0, -30.0, -29.0, -28.5, -28.0, -27.0, -26.0, -25.5,
            -25.0, -24.0, -23.5, -23.0, -22.5, -22.0, -21.5, -21.0, -20.5, -20.0, -19.5, -19.0, -18.5, -18.0,
            -17.5, -17.0, -16.5, -16.0, -15.5, -15.0, -14.6, -14.3, -14.0, -13.5, -13.0, -12.6, -12.3, -12.0,
            -11.5, -11.0, -10.6, -10.3, -10.0, -9.6, -9.3, -9.0, -8.6, -8.3, -8.0, -7.6, -7.3, -7.0, -6.6, -6.3,
            -6.0, -5.6, -5.3, -5.0, -4.6, -4.3, -4.0, -3.7, -3.5, -3.2, -3.0, -2.6, -2.3, -2.0, -1.7, -1.5,
            -1.2, -1.0, -0.6, -0.3, 0.0, 0.2, 0.5, 0.7, 1.0, 1.3, 1.6, 2.0, 2.2, 2.5, 2.7, 3.0, 3.2, 3.5, 3.7,
            4.0, 4.2, 4.5, 4.7, 5.0, 5.2, 5.5, 5.7, 6.0, 6.2, 6.5, 6.7, 7.0, 7.2, 7.5, 7.7, 8.0, 8.2, 8.5, 8.7,
            9.0, 9.2, 9.5, 9.7, 10.0, 10.2, 10.5, 10.7, 11.0, 11.2, 11.5, 11.7, 12.0, 12.2, 12.5, 12.7, 13.0,
            13.2, 13.5, 13.7, 14.0, 14.2, 14.4, 14.6, 14.8, 15.0, 15.2, 15.5, 15.7, 16.0, 16.2, 16.5, 16.7,
            17.0, 17.2, 17.5, 17.7, 18.0, 18.2, 18.5, 18.7, 19.0, 19.2, 19.4, 19.6, 19.8, 20.0, 20.2, 20.5,
            20.7, 21.0, 21.2, 21.5, 21.7, 22.0, 22.2, 22.5, 22.7, 23.0, 23.2, 23.5, 23.7, 24.0, 24.2, 24.5,
            24.7, 25.0, 25.2, 25.5, 25.7, 26.0, 26.2, 26.5, 26.7, 27.0, 27.2, 27.5, 27.7, 28.0, 28.2, 28.5,
            28.7, 29.0, 29.2, 29.5, 29.7, 30.0, 30.2, 30.5, 30.7, 31.0, 31.3, 31.6, 32.0, 32.2, 32.5, 32.7,
            33.0, 33.2, 33.5, 33.7, 34.0, 34.3, 34.6, 35.0, 35.2, 35.5, 35.7, 36.0, 36.3, 36.6, 37.0, 37.2,
            37.5, 37.7, 38.0, 38.3, 38.6, 39.0, 39.3, 39.6, 40.0, 40.3, 40.6, 41.0, 41.3, 41.6, 42.0, 42.3,
            42.6, 43.0 };
    private static final double[] indoorTemp = { -30.0, -30.0, -30.0, -30.0, -30.0, -30.0, -30.0, -30.0, -30.0, -30.0,
            -30.0, -30.0, -30.0,
            -30.0, -30.0, -30.0, -29.0, -28.0, -27.0, -26.0, -25.0, -24.0, -23.0, -22.5, -22.0, -21.0, -20.0, -19.5,
            -19.0, -18.0, -17.5, -17.0, -16.5, -16.0, -15.0, -14.5, -14.0, -13.5, -13.0, -12.5, -12.0, -11.5, -11.0,
            -10.5, -10.0, -9.5, -9.0, -8.6, -8.3, -8.0, -7.5, -7.0, -6.5, -6.0, -5.6, -5.3, -5.0, -4.5, -4.0, -3.6,
            -3.3, -3.0, -2.6, -2.3, -2.0, -1.6, -1.3, -1.0, -0.5, 0.0, 0.3, 0.6, 1.0, 1.3, 1.6, 2.0, 2.3, 2.6, 3.0, 3.2,
            3.5, 3.7, 4.0, 4.3, 4.6, 5.0, 5.3, 5.6, 6.0, 6.3, 6.6, 7.0, 7.2, 7.5, 7.7, 8.0, 8.3, 8.6, 9.0, 9.2, 9.5,
            9.7, 10.0, 10.3, 10.6, 11.0, 11.2, 11.5, 11.7, 12.0, 12.3, 12.6, 13.0, 13.2, 13.5, 13.7, 14.0, 14.2, 14.5,
            14.7, 15.0, 15.3, 15.6, 16.0, 16.2, 16.5, 16.7, 17.0, 17.2, 17.5, 17.7, 18.0, 18.2, 18.5, 18.7, 19.0, 19.2,
            19.5, 19.7, 20.0, 20.2, 20.5, 20.7, 21.0, 21.2, 21.5, 21.7, 22.0, 22.2, 22.5, 22.7, 23.0, 23.2, 23.5, 23.7,
            24.0, 24.2, 24.5, 24.7, 25.0, 25.2, 25.5, 25.7, 26.0, 26.2, 26.5, 26.7, 27.0, 27.2, 27.5, 27.7, 28.0, 28.2,
            28.5, 28.7, 29.0, 29.2, 29.5, 29.7, 30.0, 30.2, 30.5, 30.7, 31.0, 31.3, 31.6, 32.0, 32.2, 32.5, 32.7, 33.0,
            33.2, 33.5, 33.7, 34.0, 34.2, 34.5, 34.7, 35.0, 35.3, 35.6, 36.0, 36.2, 36.5, 36.7, 37.0, 37.2, 37.5, 37.7,
            38.0, 38.3, 38.6, 39.0, 39.2, 39.5, 39.7, 40.0, 40.3, 40.6, 41.0, 41.2, 41.5, 41.7, 42.0, 42.3, 42.6, 43.0,
            43.2, 43.5, 43.7, 44.0, 44.3, 44.6, 45.0, 45.3, 45.6, 46.0, 46.2, 46.5, 46.7, 47.0, 47.3, 47.6, 48.0, 48.3,
            48.6, 49.0, 49.3, 49.6, 50.0, 50.3, 50.6, 51.0, 51.3, 51.6, 52.0 };
    private static final int COMMAND_EXTENSION_HOME_LEAVE_MODE_FAN_SPEED_AUTO = 0;
    private static final int COMMAND_EXTENSION_HOME_LEAVE_MODE_FAN_SPEED_VOLUME1 = 3;
    private static final int COMMAND_EXTENSION_HOME_LEAVE_MODE_FAN_SPEED_VOLUME2 = 5;
    private static final int COMMAND_EXTENSION_HOME_LEAVE_MODE_FAN_SPEED_VOLUME3 = 7;
    private static final int COMMAND_EXTENSION_HOME_LEAVE_MODE_FAN_SPEED_VOLUME4 = 14;
    private static final int[] COMMAND_OPERATION_MODE2_OFF = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 0, 0, 0, 0, 0 };
    private static final int[] COMMAND_OPERATION_MODE2_ON = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 144, 0, 0, 0, 0, 0 };
    private static final int[] COMMAND_SELF_CLEAN_RESET_ON = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] COMMAND_VACANT_PROPERTY_OFF = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] COMMAND_VACANT_PROPERTY_ON = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0 };
    private static final double ELECTRIC_ENERGY_COFFICIENT = 0.25d;
    private static final int STATUS_EXTENSION_CODE_HOME_LEAVE_MODE = 248;
    private static final int STATUS_EXTENSION_HOME_LEAVE_MODE_FAN_SPEED_AUTO = 0;
    private static final int STATUS_EXTENSION_HOME_LEAVE_MODE_FAN_SPEED_VOLUME1 = 3;
    private static final int STATUS_EXTENSION_HOME_LEAVE_MODE_FAN_SPEED_VOLUME2 = 5;
    private static final int STATUS_EXTENSION_HOME_LEAVE_MODE_FAN_SPEED_VOLUME3 = 7;
    private static final int STATUS_EXTENSION_HOME_LEAVE_MODE_FAN_SPEED_VOLUME4 = 14;
    private static final int STATUS_EXTENSION_OP1_HOME_LEAVE_MODE_COMMAND = 0;
    private static final int STATUS_EXTENSION_OP1_HOME_LEAVE_MODE_REQUEST = 255;
    private static final int STATUS_EXTENSION_OP1_HOME_LEAVE_MODE_STATUS = 16;
    private static final int STATUS_EXTENSION_OP2_HOME_LEAVE_MODE_FAN_SPEED_FOR_COOLING = 31;
    private static final int STATUS_EXTENSION_OP2_HOME_LEAVE_MODE_FAN_SPEED_FOR_HEATING = 32;
    private static final int STATUS_EXTENSION_OP2_HOME_LEAVE_MODE_TEMP_RULE_FOR_COOLING = 27;
    private static final int STATUS_EXTENSION_OP2_HOME_LEAVE_MODE_TEMP_RULE_FOR_HEATING = 28;
    private static final int STATUS_EXTENSION_OP2_HOME_LEAVE_MODE_TEMP_SETTING_FOR_COOLING = 29;
    private static final int STATUS_EXTENSION_OP2_HOME_LEAVE_MODE_TEMP_SETTING_FOR_HEATING = 30;
    private static final int[] STATUS_MODEL_NO_TYPE_GLOBAL_2022 = { 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0 };
    private static final int[] STATUS_MODEL_NO_TYPE_HIGH_END_FOR_JAPANESE_2023 = { 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0 };
    private static final int[] STATUS_MODEL_NO_TYPE_MAX_BIT = { 127, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0 };
    private static final int[] STATUS_MODEL_NO_TYPE_SEPARATE_2021;
    private static final int[] STATUS_OPERATION_MODE2_MAX_BIT = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0,
            0 };
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
    private static final int[] receive_init = { 0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] tm_p_au = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] tm_p_no = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
    private static final int[] zeros;

    private static int getHomeLeaveModeAirFlowByte(int i) {
        if (i == 1) {
            return 3;
        }
        if (i == 2) {
            return 5;
        }
        if (i != 3) {
            return i != 4 ? 0 : 14;
        }
        return 7;
    }

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

    public static AirconStat fromBase64(AirconStat airconStat, String str) {
        return byteToStat(airconStat, Base64.getDecoder().decode(str.replace("\n", "")));
    }

    private static boolean equalBytes(ByteBuffer byteBuffer, ByteBuffer byteBuffer2) {
        return Arrays.equals(byteBuffer.array(), byteBuffer2.array());
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

    private static ByteBuffer andBytes(ByteBuffer byteBuffer, ByteBuffer byteBuffer2) {
        int length = byteBuffer.array().length;
        byteBuffer.rewind();
        byteBuffer2.rewind();
        ByteBuffer allocate = ByteBuffer.allocate(length);
        for (int i = 0; i < length; i++) {
            allocate.put((byte) (byteBuffer.get() & byteBuffer2.get()));
        }
        return allocate;
    }

    private static AirconStat byteToStat(AirconStat airconStat, byte[] bArr) {
        int i = 999;
        ByteBuffer andBytes;
        ByteBuffer andBytes2;
        int i2;
        ByteBuffer andBytes3;
        ByteBuffer andBytes4;
        ByteBuffer andBytes5;
        int length;
        int i3;
        Double d;
        Double d2;
        Integer num;
        Double d3;
        Double d4;
        Integer num2;
        int i4;
        long j;
        boolean z;
        ByteBuffer wrap = ByteBuffer.wrap(bArr);
        wrap.position(18);
        int i5 = ((wrap.get() & -1) * 4) + 21;
        ByteBuffer wrap2 = ByteBuffer.wrap(Arrays.copyOfRange(bArr, i5, i5 + 18));
        byte[] copyOfRange = Arrays.copyOfRange(bArr, i5 + 19, bArr.length - 2);
        int i6 = 1;
        if (equalBytes(toBytes(op_n_on),
                andBytes(toBytes(new int[] { 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }), wrap2))) {
            airconStat.setOperation(1);
        } else {
            airconStat.setOperation(0);
        }
        ByteBuffer wrap3 = ByteBuffer.wrap(wrap2.array());
        wrap3.position(4);
        airconStat.setPresetTemp((wrap3.get() & -1) / 2.0d);
        ByteBuffer andBytes6 = andBytes(toBytes(new int[] { 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }),
                wrap2);
        int i7 = 3;
        if (!equalBytes(toBytes(om_n_au), andBytes6)) {
            if (equalBytes(toBytes(om_n_re), andBytes6)) {
                i = 1;
            } else if (equalBytes(toBytes(om_n_dn), andBytes6)) {
                i = 2;
            } else if (equalBytes(toBytes(om_n_so), andBytes6)) {
                i = 3;
            } else if (equalBytes(toBytes(om_n_jo), andBytes6)) {
                i = 4;
            }
            airconStat.setOperationMode(i);
            andBytes = andBytes(toBytes(new int[] { 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }), wrap2);
            if (!equalBytes(toBytes(af_n_00), andBytes)) {
                airconStat.setAirFlow(0);
            } else if (equalBytes(toBytes(af_n_01), andBytes)) {
                airconStat.setAirFlow(1);
            } else if (equalBytes(toBytes(af_n_02), andBytes)) {
                airconStat.setAirFlow(2);
            } else if (equalBytes(toBytes(af_n_03), andBytes)) {
                airconStat.setAirFlow(3);
            } else if (equalBytes(toBytes(af_n_04), andBytes)) {
                airconStat.setAirFlow(4);
            }
            if (!equalBytes(toBytes(as_n_on),
                    andBytes(toBytes(new int[] { 0, 0, 192, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }), wrap2))) {
                airconStat.setWindDirectionUD(0);
            } else {
                ByteBuffer andBytes7 = andBytes(
                        toBytes(new int[] { 0, 0, 0, 240, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }), wrap2);
                if (equalBytes(toBytes(lv_n_01), andBytes7)) {
                    airconStat.setWindDirectionUD(1);
                } else if (equalBytes(toBytes(lv_n_02), andBytes7)) {
                    airconStat.setWindDirectionUD(2);
                } else if (equalBytes(toBytes(lv_n_03), andBytes7)) {
                    airconStat.setWindDirectionUD(3);
                } else if (equalBytes(toBytes(lv_n_04), andBytes7)) {
                    airconStat.setWindDirectionUD(4);
                }
            }
            if (!equalBytes(toBytes(av_n_on),
                    andBytes(toBytes(new int[] { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0 }), wrap2))) {
                airconStat.setWindDirectionLR(0);
            } else {
                ByteBuffer andBytes8 = andBytes(
                        toBytes(new int[] { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 31, 0, 0, 0, 0, 0, 0 }), wrap2);
                if (equalBytes(toBytes(lh_n_01), andBytes8)) {
                    airconStat.setWindDirectionLR(1);
                } else if (equalBytes(toBytes(lh_n_02), andBytes8)) {
                    airconStat.setWindDirectionLR(2);
                } else if (equalBytes(toBytes(lh_n_03), andBytes8)) {
                    airconStat.setWindDirectionLR(3);
                } else if (equalBytes(toBytes(lh_n_04), andBytes8)) {
                    airconStat.setWindDirectionLR(4);
                } else if (equalBytes(toBytes(lh_n_05), andBytes8)) {
                    airconStat.setWindDirectionLR(5);
                } else if (equalBytes(toBytes(lh_n_06), andBytes8)) {
                    airconStat.setWindDirectionLR(6);
                } else if (equalBytes(toBytes(lh_n_07), andBytes8)) {
                    airconStat.setWindDirectionLR(7);
                }
            }
            andBytes2 = andBytes(toBytes(new int[] { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 0, 0, 0, 0 }), wrap2);
            if (!equalBytes(toBytes(en_n_of), andBytes2)) {
                airconStat.setEntrust(0);
            } else if (equalBytes(toBytes(en_n_on), andBytes2)) {
                airconStat.setEntrust(1);
            }
            wrap3.position(6);
            i2 = wrap3.get() & ByteCompanionObject.MAX_VALUE;
            int i8 = 128;
            if ((wrap3.get() & ByteCompanionObject.MIN_VALUE) <= 0) {
                airconStat.setErrorCode("M".concat(String.format(Locale.US, "%02d", Integer.valueOf(i2))));
            } else {
                airconStat.setErrorCode("E".concat(String.valueOf(i2)));
            }
            if (i2 == 0) {
                airconStat.setErrorCode("00");
            }
            wrap3.position(8);
            if ((wrap3.get() & 8) <= 0) {
                airconStat.setCoolHotJudge(1);
            } else {
                airconStat.setCoolHotJudge(0);
            }
            andBytes3 = andBytes(toBytes(STATUS_MODEL_NO_TYPE_MAX_BIT), wrap2);
            if (!equalBytes(toBytes(STATUS_MODEL_NO_TYPE_SEPARATE_2021), andBytes3)) {
                airconStat.setModelNo(0);
            } else if (equalBytes(toBytes(STATUS_MODEL_NO_TYPE_GLOBAL_2022), andBytes3)) {
                airconStat.setModelNo(1);
            } else if (equalBytes(toBytes(STATUS_MODEL_NO_TYPE_HIGH_END_FOR_JAPANESE_2023), andBytes3)) {
                airconStat.setModelNo(2);
            }
            andBytes4 = andBytes(toBytes(STATUS_VACANT_PROPERTY_MAX_BIT), wrap2);
            if (!equalBytes(toBytes(STATUS_VACANT_PROPERTY_OFF), andBytes4)) {
                airconStat.setVacantProperty(false);
            } else if (equalBytes(toBytes(STATUS_VACANT_PROPERTY_ON), andBytes4)) {
                airconStat.setVacantProperty(true);
            }
            andBytes5 = andBytes(toBytes(STATUS_OPERATION_MODE2_MAX_BIT), wrap2);
            if (!equalBytes(toBytes(STATUS_OPERATION_MODE2_OFF), andBytes5)) {
                airconStat.setSelfCleanOperation(false);
            } else if (equalBytes(toBytes(STATUS_OPERATION_MODE2_ON), andBytes5)) {
                airconStat.setSelfCleanOperation(true);
            }
            length = copyOfRange.length / 4;
            ByteBuffer wrap4 = ByteBuffer.wrap(copyOfRange);
            i3 = 0;
            d = null;
            d2 = null;
            num = null;
            d3 = null;
            d4 = null;
            num2 = null;

            while (i3 < length) {
                int i9 = i3 * 4;
                wrap4.position(i9);
                byte b = wrap4.get();
                wrap4.position(i9 + 1);
                byte b2 = wrap4.get();
                wrap4.position(i9 + 2);
                byte b3 = wrap4.get();
                wrap4.position(i9 + i7);
                byte b4 = wrap4.get();
                if (b == toByte(i8) && b2 == toByte(16)) {
                    byte[] bArr2 = new byte[i6];
                    z = false;
                    bArr2[0] = b3;
                    airconStat.setOutdoorTemp(Double.valueOf(outdoorTemp[256 - ~b3]).doubleValue());
                    j = 4611686018427387904L;
                    i4 = 128;
                } else {
                    z = false;
                    i4 = 128;
                    if (b == toByte(128) && b2 == toByte(32)) {
                        airconStat.setIndoorTemp(indoorTemp[256 - ~b3]);
                    } else if (b == toByte(148) && b2 == toByte(16)) {
                        airconStat.setElectric(
                                (((b4 & -1) << 8) + (b3 & -1)) * ELECTRIC_ENERGY_COFFICIENT);
                    } else {
                        if (Byte.toUnsignedInt(b) == STATUS_EXTENSION_CODE_HOME_LEAVE_MODE
                                && Byte.toUnsignedInt(b2) == 16) {
                            switch (Byte.toUnsignedInt(b3)) {
                                case 27:
                                    j = 4611686018427387904L;
                                    d = Double.valueOf(Byte.toUnsignedInt(b4) / 2.0d);
                                    break;
                                case 28:
                                    j = 4611686018427387904L;
                                    d3 = Double.valueOf(Byte.toUnsignedInt(b4) / 2.0d);
                                    break;
                                case 29:
                                    j = 4611686018427387904L;
                                    d2 = Double.valueOf(Byte.toUnsignedInt(b4) / 2.0d);
                                    break;
                                case 30:
                                    j = 4611686018427387904L;
                                    d4 = Double.valueOf(Byte.toUnsignedInt(b4) / 2.0d);
                                    break;
                            }
                        }
                        j = 4611686018427387904L;
                    }
                    j = 4611686018427387904L;
                }
                i3++;
                i8 = i4;
                i6 = 1;
                i7 = 3;
            }
            return airconStat;
        }
        i = 0;
        airconStat.setOperationMode(i);
        andBytes = andBytes(toBytes(new int[] { 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }), wrap2);
        if (!equalBytes(toBytes(af_n_00), andBytes)) {
        }
        if (!equalBytes(toBytes(as_n_on),
                andBytes(toBytes(new int[] { 0, 0, 192, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }), wrap2))) {
        }
        if (!equalBytes(toBytes(av_n_on),
                andBytes(toBytes(new int[] { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0 }), wrap2))) {
        }
        andBytes2 = andBytes(toBytes(new int[] { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 0, 0, 0, 0 }), wrap2);
        if (!equalBytes(toBytes(en_n_of), andBytes2)) {
        }
        wrap3.position(6);
        i2 = wrap3.get() & ByteCompanionObject.MAX_VALUE;
        int i82 = 128;
        if ((wrap3.get() & ByteCompanionObject.MIN_VALUE) <= 0) {
        }
        if (i2 == 0) {
        }
        wrap3.position(8);
        if ((wrap3.get() & 8) <= 0) {
        }
        andBytes3 = andBytes(toBytes(STATUS_MODEL_NO_TYPE_MAX_BIT), wrap2);
        if (!equalBytes(toBytes(STATUS_MODEL_NO_TYPE_SEPARATE_2021), andBytes3)) {
        }
        andBytes4 = andBytes(toBytes(STATUS_VACANT_PROPERTY_MAX_BIT), wrap2);
        if (!equalBytes(toBytes(STATUS_VACANT_PROPERTY_OFF), andBytes4)) {
        }
        andBytes5 = andBytes(toBytes(STATUS_OPERATION_MODE2_MAX_BIT), wrap2);
        if (!equalBytes(toBytes(STATUS_OPERATION_MODE2_OFF), andBytes5)) {
        }
        length = copyOfRange.length / 4;
        ByteBuffer wrap42 = ByteBuffer.wrap(copyOfRange);
        i3 = 0;
        d = null;
        d2 = null;
        num = null;
        d3 = null;
        d4 = null;
        num2 = null;
        while (i3 < length) {
        }
        return airconStat;
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

    public static String byteArrayToHexString(byte[] bArr) {
        StringBuilder sb = new StringBuilder();
        int length = bArr.length;
        for (int i = 0; i < length; i++) {
            sb.append(String.format("%02x", new Object[] { Integer.valueOf(bArr[i] & -1) }));
        }
        return sb.toString();
    }

    private static void putArrayToList(List<Integer> list, int[] iArr) {
        list.addAll((List) Arrays.stream(iArr).boxed().collect(Collectors.toList()));
    }

}
