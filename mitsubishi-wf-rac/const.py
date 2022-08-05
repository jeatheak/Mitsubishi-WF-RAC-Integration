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
HORIZONTAL_POSITION_1 = "Left/Right Position 1"
HORIZONTAL_POSITION_2 = "Left/Right Position 2"
HORIZONTAL_POSITION_3 = "Left/Right Position 3"
HORIZONTAL_POSITION_4 = "Left/Right Position 4"

VERTICAL_POSITION_1 = "Up/Down Position 1"
VERTICAL_POSITION_2 = "Up/Down Position 2"
VERTICAL_POSITION_3 = "Up/Down Position 3"
VERTICAL_POSITION_4 = "Up/Down Position 4"

SUPPORT_SWING_MODES = [
    SWING_OFF,
    SWING_HORIZONTAL,
    SWING_VERTICAL,
    SWING_BOTH,
    SWING_3D_AUTO,
    HORIZONTAL_POSITION_1,
    HORIZONTAL_POSITION_2,
    HORIZONTAL_POSITION_3,
    HORIZONTAL_POSITION_4,
    VERTICAL_POSITION_1,
    VERTICAL_POSITION_2,
    VERTICAL_POSITION_3,
    VERTICAL_POSITION_4,
]

SUPPORTED_FAN_MODES = [
    FAN_AUTO,
    "1",
    "2",
    "3",
    "4",
]


OPERATION_LIST = {
    # HVAC_MODE_OFF: "Off",
    HVAC_MODE_HEAT: "Heat",
    HVAC_MODE_COOL: "Cool",
    HVAC_MODE_AUTO: "Auto",
    HVAC_MODE_DRY: "Dry",
    HVAC_MODE_FAN_ONLY: "Fan",
}
