"""Constants used by the mitsubishi-wf-rac component."""

from datetime import timedelta
from homeassistant.const import CONF_ICON, CONF_NAME, CONF_TYPE
from homeassistant.components.climate.const import (
    HVACMode,
    ClimateEntityFeature,
    FAN_AUTO,
)

DOMAIN = "mitsubishi_wf_rac"
DEVICES = "wf-rac-devices"

MIN_TIME_BETWEEN_UPDATES=timedelta(seconds=60)

CONF_OPERATOR_ID = "operator_id"
CONF_AIRCO_ID = "airco_id"
CONF_AVAILABILITY_CHECK = "availability_check"
CONF_AVAILABILITY_RETRY_LIMIT = "availability_retry_limit"
CONF_CREATE_SWING_MODE_SELECT = "create_swing_mode_select"
ATTR_DEVICE_ID = "device_id"
ATTR_CONNECTED_ACCOUNTS = "connected_accounts"

ATTR_INSIDE_TEMPERATURE = "inside_temperature"
ATTR_OUTSIDE_TEMPERATURE = "outside_temperature"
ATTR_TARGET_TEMPERATURE = "target_temperature"

SENSOR_TYPE_TEMPERATURE = "temperature"

SENSOR_TYPES = {
    ATTR_INSIDE_TEMPERATURE: {
        CONF_NAME: "Inside Temperature",
        CONF_ICON: "mdi:thermometer",
        CONF_TYPE: SENSOR_TYPE_TEMPERATURE,
    },
    ATTR_OUTSIDE_TEMPERATURE: {
        CONF_NAME: "Outside Temperature",
        CONF_ICON: "mdi:thermometer",
        CONF_TYPE: SENSOR_TYPE_TEMPERATURE,
    },
}

SERVICE_SET_HORIZONTAL_SWING_MODE = "set_horizontal_swing_mode"
SERVICE_SET_VERTICAL_SWING_MODE = "set_vertical_swing_mode"

SUPPORT_FLAGS = (
    ClimateEntityFeature.FAN_MODE
    | ClimateEntityFeature.SWING_HORIZONTAL_MODE
    | ClimateEntityFeature.SWING_MODE
    | ClimateEntityFeature.TARGET_TEMPERATURE
    | ClimateEntityFeature.TURN_OFF
    | ClimateEntityFeature.TURN_ON
)

SUPPORTED_HVAC_MODES = [
    HVACMode.OFF,
    HVACMode.AUTO,
    HVACMode.COOL,
    HVACMode.DRY,
    HVACMode.HEAT,
    HVACMode.FAN_ONLY,
]

HVAC_TRANSLATION = {
    HVACMode.AUTO: 0,
    HVACMode.COOL: 1,
    HVACMode.HEAT: 2,
    HVACMode.FAN_ONLY: 3,
    HVACMode.DRY: 4,
}

SWING_3D_AUTO = "3D Auto"
SWING_VERTICAL_POSITION_1 = "Highest"
SWING_VERTICAL_POSITION_2 = "Middle"
SWING_VERTICAL_POSITION_3 = "Normal"
SWING_VERTICAL_POSITION_4 = "Lowest"
SWING_VERTICAL_AUTO = "Up/Down Auto"

SWING_HORIZONTAL_POSITION_1 = "Left-Left"
SWING_HORIZONTAL_POSITION_2 = "Left-Center"
SWING_HORIZONTAL_POSITION_3 = "Center-Center"
SWING_HORIZONTAL_POSITION_4 = "Center-Right"
SWING_HORIZONTAL_POSITION_5 = "Right-Right"
SWING_HORIZONTAL_POSITION_6 = "Left-Right"
SWING_HORIZONTAL_POSITION_7 = "Right-Left"
SWING_HORIZONTAL_AUTO = "Left/Right Auto"


SWING_MODE_TRANSLATION = {
    SWING_VERTICAL_AUTO: 0,
    SWING_VERTICAL_POSITION_1: 1,
    SWING_VERTICAL_POSITION_2: 2,
    SWING_VERTICAL_POSITION_3: 3,
    SWING_VERTICAL_POSITION_4: 4,
}

SUPPORT_SWING_MODES = [
    SWING_VERTICAL_AUTO,
    SWING_VERTICAL_POSITION_1,
    SWING_VERTICAL_POSITION_2,
    SWING_VERTICAL_POSITION_3,
    SWING_VERTICAL_POSITION_4,
    SWING_3D_AUTO,
]

SWING_HORIZONTAL_MODE_TRANSLATION = {
    SWING_HORIZONTAL_AUTO: 0,
    SWING_HORIZONTAL_POSITION_1: 1,
    SWING_HORIZONTAL_POSITION_2: 2,
    SWING_HORIZONTAL_POSITION_3: 3,
    SWING_HORIZONTAL_POSITION_4: 4,
    SWING_HORIZONTAL_POSITION_5: 5,
    SWING_HORIZONTAL_POSITION_6: 6,
    SWING_HORIZONTAL_POSITION_7: 7,
}

SUPPORT_SWING_HORIZONTAL_MODES = [
    SWING_HORIZONTAL_AUTO,
    SWING_HORIZONTAL_POSITION_1,
    SWING_HORIZONTAL_POSITION_2,
    SWING_HORIZONTAL_POSITION_3,
    SWING_HORIZONTAL_POSITION_4,
    SWING_HORIZONTAL_POSITION_5,
    SWING_HORIZONTAL_POSITION_6,
    SWING_HORIZONTAL_POSITION_7,
    SWING_3D_AUTO,
]


FAN_MODE_1 = "1 Lowest"
FAN_MODE_2 = "2 Low"
FAN_MODE_3 = "3 High"
FAN_MODE_4 = "4 Highest"

FAN_MODE_TRANSLATION = {
    FAN_AUTO: 0,
    FAN_MODE_1: 1,
    FAN_MODE_2: 2,
    FAN_MODE_3: 3,
    FAN_MODE_4: 4,
}

SUPPORTED_FAN_MODES = [
    FAN_AUTO,
    FAN_MODE_1,
    FAN_MODE_2,
    FAN_MODE_3,
    FAN_MODE_4,
]


OPERATION_LIST = {
    # HVAC_MODE_OFF: "Off",
    HVACMode.HEAT: "Heat",
    HVACMode.COOL: "Cool",
    HVACMode.AUTO: "Auto",
    HVACMode.DRY: "Dry",
    HVACMode.FAN_ONLY: "Fan",
}
