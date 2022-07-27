"""Constants used by the mitsubishi-wf-rac component."""

from homeassistant.const import CONF_ICON, CONF_NAME, CONF_TYPE
from homeassistant.components.climate.const import (
    HVAC_MODE_COOL,
    HVAC_MODE_HEAT,
    HVAC_MODE_DRY,
    HVAC_MODE_FAN_ONLY,
    HVAC_MODE_OFF,
    HVAC_MODE_AUTO,
    SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_FAN_MODE,
    SUPPORT_SWING_MODE,
)

DOMAIN = "mitsubishi-wf-rac"
DEVICES = "wf-rac-devices"
ATTR_TARGET_TEMPERATURE = "target_temperature"
ATTR_INSIDE_TEMPERATURE = "inside_temperature"
ATTR_OUTSIDE_TEMPERATURE = "outside_temperature"

ATTR_SWING_LR_MODE = "horizontal_swing_mode"
ATTR_SWING_LR_MODES = "horizontal_swing_modes"
ATTR_SWING_UD_MODE = "vertical_swing_mode"
ATTR_SWING_UD_MODES = "vertical_swing_modes"

ATTR_STATE_ON = "on"
ATTR_STATE_OFF = "off"

SERVICE_SET_SWING_LR_MODE = "set_horizontal_swing_mode"
SERVICE_SET_SWING_LR_MODE = "set_vertical_swing_mode"

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

SUPPORT_FLAGS = SUPPORT_TARGET_TEMPERATURE | SUPPORT_FAN_MODE | SUPPORT_SWING_MODE

OPERATION_LIST = {
    HVAC_MODE_OFF: "Off",
    HVAC_MODE_HEAT: "Heat",
    HVAC_MODE_COOL: "Cool",
    HVAC_MODE_AUTO: "Auto",
    HVAC_MODE_DRY: "Dry",
    HVAC_MODE_FAN_ONLY: "Fan",
}
