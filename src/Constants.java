package src;

public final class Constants {
    public static final String API_BASE = "https://spa.smartmair.com/";
    public static final String API_BASE_DEMO = ("https://spa.smartmair.com/" + "demo/");
    public static final String API_SUFFIX = "";
    public static final int APPLICATION_MODE_DEMO = 0;
    public static final int APPLICATION_MODE_EXTERNAL = 2;
    public static final int APPLICATION_MODE_INTERNAL = 1;

    /* renamed from: ASSETS＿PATH reason: contains not printable characters */
    public static final String f618ASSETSPATH = "file:///android_asset/";
    public static final int AUTO_MODE = 0;
    public static final int AUTO_WIND = 0;
    public static final String BACKSTACK_TAG_START_UP = "startUp";
    public static final String BASE_TAG = "AirconAppDebugLog:";
    public static final String BUNDLE_KEY_STARTING_POINT_SCREEN = "startingPointScreen";
    public static final int CENTER_WIND = 3;
    public static final double CHANGE_TEMP = 0.5d;
    public static final String CHANNEL_ID_FORGET = "forget";
    public static final String COMMAND_DELETE_ACCOUNT_INFO = "deleteAccountInfo";
    public static final String COMMAND_GET_AIRCON_STAT = "getAirconStat";
    public static final String COMMAND_GET_DEVICE_INFO = "getDeviceInfo";
    public static final String COMMAND_SET_AIRCON_STAT = "setAirconStat";
    public static final String COMMAND_SET_NETWORK_INFO = "setNetworkInfo";
    public static final String COMMAND_SET_OPTION_SETTING = "setOptionSetting";
    public static final String COMMAND_UPDATE_ACCOUNT_INFO = "updateAccountInfo";
    public static final String COMMAND_UPDATE_FIRMWARE = "updateFirmware";
    public static final int COOL_MODE = 1;
    public static final int CYCLE_UPDATE_MSEC_LONG = 60000;
    public static final int CYCLE_UPDATE_MSEC_SHORT = 5000;
    public static final String DEFAULT_ELECTRIC_BILL = "-";
    public static final float DEFAULT_POSITION_OFFSET = 0.5f;
    public static final String DEFAULT_PRESET_TEMPERATURE_DECIMAL = "0";
    public static final String DEFAULT_PRESET_TEMPERATURE_INTEGER = "25";
    public static final String DEFAULT_TEMPERATURE = "--.-";
    public static final String DEFAULT_TEMPERATURE_CONNECTION_ERROR = "-";
    public static final String DEFAULT_TEMP_INFO_TEMPERATURE = "--.--";
    public static final int DRY_MODE = 4;
    public static final int ENTRUST_OFF = 0;
    public static final int ENTRUST_ON = 1;
    public static final int ERROR_MODE = 99;
    public static final double ERROR_TEMP = 99.9d;
    public static final int FAVORITE_ID_1 = 1;
    public static final int FAVORITE_ID_2 = 2;
    public static final int GET_AIRCON_LIST_INTERNAL_DELAY = 500;
    public static final int GPS_SERVICE_NOTIFICATION_ID = 10;
    public static final float GRAPH_AXIS_DEFAULT = 10.0f;
    public static final float GRAPH_MAXIMUM_COEFFICIENT = 1.25f;
    public static final String GROUP = "airconApp";
    public static final String GROUP_ID_PUSH = "pushNotification";
    public static final int HIGHER_WIND = 1;
    public static final int HOME_LEAVE_MODE_FAN_SPEED_FOR_COOLING_DEFAULT = 0;
    public static final int HOME_LEAVE_MODE_FAN_SPEED_FOR_HEATING_DEFAULT = 0;
    public static final int HOME_LEAVE_MODE_TEMP_RULE_FOR_COOLING_CHANGE = 3;
    public static final int HOME_LEAVE_MODE_TEMP_RULE_FOR_COOLING_DEFAULT = 35;
    public static final int HOME_LEAVE_MODE_TEMP_RULE_FOR_COOLING_MAX = 35;
    public static final int HOME_LEAVE_MODE_TEMP_RULE_FOR_COOLING_MIN = 26;
    public static final int HOME_LEAVE_MODE_TEMP_RULE_FOR_HEATING_CHANGE = 5;
    public static final int HOME_LEAVE_MODE_TEMP_RULE_FOR_HEATING_DEFAULT = 0;
    public static final int HOME_LEAVE_MODE_TEMP_RULE_FOR_HEATING_MAX = 15;
    public static final int HOME_LEAVE_MODE_TEMP_RULE_FOR_HEATING_MIN = 0;
    public static final int HOME_LEAVE_MODE_TEMP_SETTING_FOR_COOLING_CHANGE = 1;
    public static final int HOME_LEAVE_MODE_TEMP_SETTING_FOR_COOLING_DEFAULT = 33;
    public static final int HOME_LEAVE_MODE_TEMP_SETTING_FOR_COOLING_MAX = 33;
    public static final int HOME_LEAVE_MODE_TEMP_SETTING_FOR_COOLING_MIN = 26;
    public static final int HOME_LEAVE_MODE_TEMP_SETTING_FOR_HEATING_CHANGE = 1;
    public static final int HOME_LEAVE_MODE_TEMP_SETTING_FOR_HEATING_DEFAULT = 10;
    public static final int HOME_LEAVE_MODE_TEMP_SETTING_FOR_HEATING_MAX = 18;
    public static final int HOME_LEAVE_MODE_TEMP_SETTING_FOR_HEATING_MIN = 10;
    public static final int HOT_MODE = 2;
    public static final int INIT_FAVORITE_AIR_FLOW = 0;
    public static final int INIT_FAVORITE_ENTRUST = 0;
    public static final int INIT_FAVORITE_OPERATION_MODE = 0;
    public static final double INIT_FAVORITE_TEMP = 25.0d;
    public static final int INIT_FAVORITE_WIND_LR = 3;
    public static final int INIT_FAVORITE_WIND_UD = 0;
    public static final double INIT_TEMP = 25.0d;
    public static final int JET_WIND = 4;
    public static final String LANGUAGE_EN = "en";
    public static final int LEFT_WIND = 1;
    public static final int LOWER_WIND = 4;
    public static final int MAX_AIR_FLOW = 4;
    public static final int MAX_OPERATION_MODE = 4;
    public static final int MAX_REGISTERED_AIRCON = 16;
    public static final double MAX_TEMP = 30.0d;
    public static final int MAX_WIND_DIRECTION_LR = 7;
    public static final int MAX_WIND_DIRECTION_UD = 4;
    public static final int MIDDLE_WIND = 2;
    public static final int MIN_AIR_FLOW = 0;
    public static final int MIN_OPERATION_MODE = 0;
    public static final double MIN_TEMP = 18.0d;
    public static final int MIN_WIND_DIRECTION_LR = 0;
    public static final int MIN_WIND_DIRECTION_UD = 0;
    public static final int MODEL_NO_TYPE_GLOBAL_2022 = 1;
    public static final int MODEL_NO_TYPE_HIGH_END_FOR_JAPANESE_2023 = 2;
    public static final int MODEL_NO_TYPE_SEPARATE_2021 = 0;
    public static final String NOTIFYDESCRIPTION = "notification";
    public static final int OFFSET_MONTHS_COUNT_FOR_GET_CONSUMPTION = 35;
    public static final int OFF_MODE = 0;
    public static final int ON_MODE = 1;
    public static final int OPERATION_MODE2_NONE = 0;
    public static final int OPERATION_MODE2_SELF_CREAN = 1;
    public static final String OS_TYPE = "android";
    public static final String PLAY_STORE_URL_BASE = "https://play.google.com/store/apps/details?id=";
    public static final int RIGHT_WIND = 5;
    public static final int SEND_AIR_MODE = 3;
    public static final int SLIGHTLY_HIGHER_WIND = 2;
    public static final int SLIGHTLY_LEFT_WIND = 2;
    public static final int SLIGHTLY_LOWER_WIND = 3;
    public static final int SLIGHTLY_RIGHT_WIND = 4;
    public static final int SPLASH_VIEW_MILL_SEC = 1500;
    public static final int SPOT_WIND = 7;
    public static final int STRONG_WIND = 3;
    public static final int SWING_WIND_LR = 0;
    public static final int SWING_WIND_UD = 0;
    public static final double TEMPERATURE_INDIA = 24.0d;
    public static final double TEMP_INFORMATION_CHANGE_TEMP = 1.0d;
    public static final int TEMP_INFORMATION_TEMP_MAX = 52;
    public static final int TEMP_INFORMATION_TEMP_MIN = 0;
    public static final String TIMEZONE_INDIA = "Asia/Kolkata";
    public static final String TIMEZONE_TOKYO = "Asia/Tokyo";
    public static final int TIME_OUT_SEC = 20;
    public static final int UNIT_SPACE_OFFSET = 30;
    public static final int UPDATE_AIRCON_TIMING = 2000;
    public static final String USED_ELECTRICITY_BILL_GRAPH_DATE_FORMAT_yyyyMM = "yyyyMM";
    public static final int USED_ELECTRICITY_BILL_GRAPH_MAX_MONTH_COUNT = 48;
    public static final int USED_ELECTRICITY_BILL_GRAPH_MONTH_COUNT = 12;
    public static final double VACANT_PROPERTY_CHANGE_TEMP = 1.0d;
    public static final double VACANT_PROPERTY_COOL_MODE_MAX_TEMP = 33.0d;
    public static final double VACANT_PROPERTY_COOL_MODE_MIN_TEMP = 31.0d;
    public static final double VACANT_PROPERTY_COOL_MODE_TEMP_DEFAULT = 31.0d;
    public static final double VACANT_PROPERTY_HOT_MODE_MAX_TEMP = 17.0d;
    public static final double VACANT_PROPERTY_HOT_MODE_MIN_TEMP = 10.0d;
    public static final double VACANT_PROPERTY_HOT_MODE_TEMP_DEFAULT = 10.0d;
    public static final int VACANT_PROPERTY_OFF = 0;
    public static final int VACANT_PROPERTY_ON = 1;
    public static final int VISIBLE_X_RANGE_MAXIMUM = 6;
    public static final int WEAK_WIND = 1;
    public static final int WIDE_WIND = 6;
    public static final String WIRELESS_IF_API_BASE = "http://";
    static final String WIRELESS_IF_API_PORT = ":51443";
    public static final String WIRELESS_IF_PATH = "/beaver/command/";
    public static final int Y_AXIS_LABEL_COUNT = 6;

    /* renamed from: jp.co.mhi_mth.smartmair.util.Constants$TempAddType */
    public enum TempAddType {
        None,
        Add,
        Sub
    }

    /* renamed from: jp.co.mhi_mth.smartmair.util.Constants$OperationModeType */
    public enum OperationModeType {
        Auto(0),
        Cool(1),
        Hot(2),
        SendAir(3),
        Dry(4);

        /* renamed from: id */
        private final int f589id;

        private OperationModeType(int i) {
            this.f589id = i;
        }

        public static OperationModeType init(int i) {
            for (OperationModeType operationModeType : values()) {
                if (operationModeType.rawValue() == i) {
                    return operationModeType;
                }
            }
            return null;
        }

        public int rawValue() {
            return this.f589id;
        }
    }

    /* renamed from: jp.co.mhi_mth.smartmair.util.Constants$TempRangeType */
    public enum TempRangeType {
        Normal,
        VacantPropertyCoolTemp,
        VacantPropertyHotTemp,
        OutOfRange;

        public static TempRangeType init(int i) {
            return init(Double.valueOf((double) i).doubleValue());
        }

        public static TempRangeType init(double d) {
            if (d < 10.0d) {
                return OutOfRange;
            }
            if (d <= 17.0d) {
                return VacantPropertyHotTemp;
            }
            if (d < 18.0d) {
                return OutOfRange;
            }
            if (d > 33.0d) {
                return OutOfRange;
            }
            if (d >= 31.0d) {
                return VacantPropertyCoolTemp;
            }
            if (d > 30.0d) {
                return OutOfRange;
            }
            return Normal;
        }
    }

    /* renamed from: jp.co.mhi_mth.smartmair.util.Constants$TempUnitType */
    public enum TempUnitType {
        Celsius(0),
        Fahrenheit(1);

        /* renamed from: id */
        private final int f591id;

        private TempUnitType(int i) {
            this.f591id = i;
        }

        public static TempUnitType init(int i) {
            TempUnitType tempUnitType = Celsius;
            return tempUnitType.rawValue() == i ? tempUnitType : Fahrenheit;
        }

        public int rawValue() {
            return this.f591id;
        }

        public boolean isCelsius() {
            return this == Celsius;
        }
    }

    /* renamed from: jp.co.mhi_mth.smartmair.util.Constants$TempSettingType */
    public enum TempSettingType {
        Normal,
        VacantProperty;

        public static TempSettingType init(boolean z) {
            return z ? VacantProperty : Normal;
        }
    }

    /* renamed from: jp.co.mhi_mth.smartmair.util.Constants$TempItemType */
    public enum TempItemType {
        presetTemp,
        vacantPropertyCooling,
        vacantPropertyHeating,
        tempInformation,
        homeLeaveModeTempRuleForCooling,
        homeLeaveModeTempRuleForHeating,
        homeLeaveModeTempSettingForCooling,
        homeLeaveModeTempSettingForHeating;

        public double getMax() {
            switch (this) {
                case vacantPropertyCooling:
                    return 33.0d;
                case vacantPropertyHeating:
                    return 17.0d;
                case tempInformation:
                    return 52.0d;
                case homeLeaveModeTempRuleForCooling:
                    return 35.0d;
                case homeLeaveModeTempRuleForHeating:
                    return 15.0d;
                case homeLeaveModeTempSettingForCooling:
                    return 33.0d;
                case homeLeaveModeTempSettingForHeating:
                    return 18.0d;
                default:
                    return 30.0d;
            }
        }

        public double getMin() {
            switch (this) {
                case vacantPropertyCooling:
                    return 31.0d;
                case vacantPropertyHeating:
                    return 10.0d;
                case tempInformation:
                    return Double.longBitsToDouble(1);
                case homeLeaveModeTempRuleForCooling:
                    return 26.0d;
                case homeLeaveModeTempRuleForHeating:
                    return Double.longBitsToDouble(1);
                case homeLeaveModeTempSettingForCooling:
                    return 26.0d;
                case homeLeaveModeTempSettingForHeating:
                    return 10.0d;
                default:
                    return 18.0d;
            }
        }

        public double getAdd() {
            switch (this) {
                case vacantPropertyCooling:
                case vacantPropertyHeating:
                case tempInformation:
                    return 1.0d;
                case homeLeaveModeTempRuleForCooling:
                    return 3.0d;
                case homeLeaveModeTempRuleForHeating:
                    return 5.0d;
                case homeLeaveModeTempSettingForCooling:
                case homeLeaveModeTempSettingForHeating:
                    return 1.0d;
                default:
                    return 0.5d;
            }
        }
    }

    /*
     * renamed from: jp.co.mhi_mth.smartmair.util.Constants$ButtonOperationDelayType
     */
    public enum ButtonOperationDelayType {
        SHORT(500),
        LONG(Constants.UPDATE_AIRCON_TIMING),
        NONE(0);

        private final int delayMillis;

        private ButtonOperationDelayType(int i) {
            this.delayMillis = i;
        }

        public int getDelayMillis() {
            return this.delayMillis;
        }
    }

    public static String getApiBase() {
        return API_BASE;
    }

    public static final String API_GET_AIRCON_STAT() {
        return getApiBase() + "command/getAirconStat" + "";
    }

    public static final String API_SET_AIRCON_STAT() {
        return getApiBase() + "command/setAirconStat" + "";
    }

    public static final String API_GET_CALENDAR_STAT() {
        return getApiBase() + "server/getCalendarInfo" + "";
    }

    public static final String API_GET_WEEKLY_TIMER() {
        return getApiBase() + "server/getWeeklyTimer" + "";
    }

    public static final String API_SET_WEEKLY_TIMER() {
        return getApiBase() + "server/setWeeklyTimer" + "";
    }

    public static final String API_CHECK_CALENDAR() {
        return getApiBase() + "server/checkCalendar" + "";
    }

    public static final String API_SET_CALENDAR_STAT() {
        return getApiBase() + "server/setCalendarInfo" + "";
    }

    public static final String API_REG_AIRCON_ACCOUNT() {
        return getApiBase() + "server/setAirconAccount" + "";
    }

    public static final String API_GET_ELECTRICITY_INFORMATION_ACCOUNT() {
        return getApiBase() + "server/getConsumption" + "";
    }

    public static final String API_GET_AIRCON_SETTING() {
        return getApiBase() + "server/getAirconSetting" + "";
    }

    public static final String API_SET_OPTION_SETTING() {
        return getApiBase() + "server/setOptionSetting" + "";
    }

    public static final String API_SET_AIRCON_ACCOUNT() {
        return getApiBase() + "server/setAirconAccount" + "";
    }

    public static final String API_DEL_AIRCON_ACCOUNT() {
        return getApiBase() + "server/delAirconAccount" + "";
    }

    public static final String API_GET_ENDPOINT() {
        return getApiBase() + "wirelesskit/getEndpoint" + "";
    }

    public static final String API_SEND_FORGOTTEN_MANAGEMENT() {
        return getApiBase() + "server/sendForgottenManagement" + "";
    }

    public static final String API_SET_DEVICE_TOKEN() {
        return getApiBase() + "server/setDeviceToken" + "";
    }

    public static final String API_GET_NOTIFICATION_STAT() {
        return getApiBase() + "server/getInformation" + "";
    }

    public static final String API_GET_DEVICE_INFO() {
        return getApiBase() + "beaver/command" + "";
    }

    public static final String API_GET_FIRMWARE() {
        return getApiBase() + "server/getFirmware" + "";
    }

    public static final String API_GET_CONSUMPTION() {
        return getApiBase() + "server/getConsumption" + "";
    }

    public static final String API_SET_AIRCON_NAME() {
        return getApiBase() + "server/setAirconName" + "";
    }

    public static final String API_MAKE_ACCOUNT() {
        return getApiBase() + "server/makeAccount" + "";
    }

    public static final String ApiGetAppVersion() {
        return getApiBase() + "server/getAppVersion" + "";
    }

    public static final String API_GET_AIRCON_FOR_MOVING() {
        return getApiBase() + "server/getAirconForMoving" + "";
    }

    public static final String API_SET_ACCOUNT() {
        return getApiBase() + "server/setAccount" + "";
    }

    /* renamed from: jp.co.mhi_mth.smartmair.util.Constants$ScreenType */
    public enum ScreenType {
        None(0),
        A01RuleServiceAgreement(1),
        A02Startup(2),
        A03MainMenu(3),
        A04Login(4),
        A05PersonInfoHandleAgree(5),
        A06AccountCreation(6),
        A08PasswordReminder(8),
        A09AirconList(9),
        A10WirelessLANSetting(10),
        A11AirconDetail(11),
        A12OptionSetting(12),
        A13WeeklyTimer(13),
        A14Calendar(14),
        A15Favorite(15),
        A16UsedElectricityBillGraph(16),
        A17AppSettings(17),
        A18ModeSwitch(18),
        A19AppInitialize(19),
        A20AppVerDisplay(20),
        A21LanguageTimezoneSetting(21),
        A22NotificationList(22),
        A23NotificationDetail(23),
        A24Splash(24);

        /* renamed from: id */
        private int f590id;

        private ScreenType(int i) {
            this.f590id = i;
        }

        public int getId() {
            return this.f590id;
        }

        public static ScreenType valueOf(int i) {
            for (ScreenType screenType : values()) {
                if (screenType.f590id == i) {
                    return screenType;
                }
            }
            return None;
        }
    }

    private Constants() {
    }
}
