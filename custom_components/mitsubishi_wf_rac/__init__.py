"""The WF-RAC sensor integration."""  # pylint: disable=invalid-name
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType

from homeassistant.const import CONF_HOST, CONF_PORT, CONF_NAME, CONF_DEVICE_ID
from homeassistant.components.climate.const import HVACMode

from .const import API, CONF_AIRCO_ID, CURRENT_PRESET_MODE, DOMAIN, CONF_OPERATOR_ID, FAN_MODE, HORIZONTAL_SWING_MODE, HVAC_MODE, NAME, NUMBER_OF_PRESET_MODES, PRESET_MODES, STORE, TEMPERATURE, VERTICAL_SWING_MODE
from .wfrac.device import Device

_LOGGER = logging.getLogger(__name__)

COMPONENT_TYPES = ["sensor", "climate", "number","select", "text"]


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Establish connection with mitsubishi-wf-rac."""
    default_names = {1: "home", 2: "comfort", 3: "boost", 4: "away"}
    preset_mode_store = {
        PRESET_MODES: {
            i: {
                NAME: default_names[i],
                FAN_MODE: "AUTO",
                VERTICAL_SWING_MODE: "LOW",
                HORIZONTAL_SWING_MODE: "LOW",
                HVAC_MODE: HVACMode.HEAT,
                TEMPERATURE: 21,
            }
            for i in range(1, NUMBER_OF_PRESET_MODES + 1)
        },
        CURRENT_PRESET_MODE: None,
    }

    if DOMAIN not in hass.data:
        hass.data.setdefault(DOMAIN, {})
        
    hass.data[DOMAIN][entry.entry_id] = {
        STORE: preset_mode_store
    }

    device: str = entry.data[CONF_HOST]
    name: str = entry.data[CONF_NAME]
    device_id: str = entry.data[CONF_DEVICE_ID]
    operator_id: str = entry.data[CONF_OPERATOR_ID]
    port: int = entry.data[CONF_PORT]
    airco_id: str = entry.data[CONF_AIRCO_ID]

    try:
        api = Device(hass, name, device, port, device_id, operator_id, airco_id)
        await api.update()  # initial update to get fresh values
        hass.data[DOMAIN][entry.entry_id][API] = api
    except Exception as ex:  # pylint: disable=broad-except
        _LOGGER.warning("Something whent wrong setting up device [%s] %s", device, ex)

    for component in COMPONENT_TYPES:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_remove_entry(hass, entry: ConfigEntry) -> None:
    """Handle removal of an entry."""
    for device in hass.data[DOMAIN]:
        temp_device: Device = device[API]
        if temp_device.host == entry.data[CONF_HOST]:
            try:
                await temp_device.delete_account()
                _LOGGER.info(
                    "Deleted operator ID [%s] from airco [%s]",
                    temp_device.operator_id,
                    temp_device.airco_id,
                )
                hass.data[DOMAIN][entry.entry_uid][API] = None
            except Exception as ex:  # pylint: disable=broad-except
                _LOGGER.warning(
                    "Something whent wrong deleting account from airco [%s] %s",
                    temp_device.name,
                    ex,
                )
