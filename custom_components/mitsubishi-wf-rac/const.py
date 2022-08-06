"""Constants used by the mitsubishi-wf-rac component."""

from homeassistant.const import CONF_ICON, CONF_NAME, CONF_TYPE
from homeassistant.components.climate.const import (
    HVAC_MODE_COOL,
    HVAC_MODE_HEAT,
    HVAC_MODE_DRY,
    HVAC_MODE_FAN_ONLY,
    HVAC_MODE_OFF,
    HVAC_MODE_AUTO,
    ClimateEntityFeature,
    HVACMode,
    FAN_AUTO,
    SWING_BOTH,
    SWING_HORIZONTAL,
    SWING_OFF,
    SWING_VERTICAL,
)

DOMAIN = "mitsubishi-wf-rac"
DEVICES = "wf-rac-devices"

CONF_OPERATOR_ID = "operator_id"
CONF_AIRCO_ID = "airco_id"

ATTR_INSIDE_TEMPERATURE = "inside_temperature"
ATTR_OUTSIDE_TEMPERATURE = "outside_temperature"

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

SUPPORT_FLAGS = (
    ClimateEntityFeature.TARGET_TEMPERATURE
    | ClimateEntityFeature.SWING_MODE
    | ClimateEntityFeature.FAN_MODE
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
    HVAC_MODE_AUTO: 0,
    HVAC_MODE_COOL: 1,
    HVAC_MODE_HEAT: 2,
    HVAC_MODE_FAN_ONLY: 3,
    HVAC_MODE_DRY: 4,
}

SWING_3D_AUTO = "3D Auto"
SWING_VERTICAL_POSITION_1 = "Highest"
SWING_VERTICAL_POSITION_2 = "Middle"
SWING_VERTICAL_POSITION_3 = "Normal"
SWING_VERTICAL_POSITION_4 = "Lowest"
SWING_VERTICAL_AUTO = "Up/Down Auto"

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
    HVAC_MODE_HEAT: "Heat",
    HVAC_MODE_COOL: "Cool",
    HVAC_MODE_AUTO: "Auto",
    HVAC_MODE_DRY: "Dry",
    HVAC_MODE_FAN_ONLY: "Fan",
}
