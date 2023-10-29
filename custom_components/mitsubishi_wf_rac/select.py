""" for select component used for horizontal swing."""
# pylint: disable = too-few-public-methods

import logging

from homeassistant.components.select import SelectEntity
from homeassistant.const import CONF_HOST
from homeassistant.util import Throttle
from homeassistant.helpers.restore_state import RestoreEntity

from .wfrac.models.aircon import AirconCommands
from .wfrac.device import MIN_TIME_BETWEEN_UPDATES, Device
from .const import (
    API,
    DEVICES,
    DOMAIN,
    FAN_MODE,
    HORIZONTAL_SWING_MODE,
    HORIZONTAL_SWING_MODE_TRANSLATION,
    HVAC_MODE,
    PRESET_MODES,
    STORE,
    SUPPORTED_HVAC_MODES,
    SWING_3D_AUTO,
    SWING_MODE_TRANSLATION,
    SWING_HORIZONTAL_AUTO,
    SUPPORT_HORIZONTAL_SWING_MODES,
    SUPPORT_SWING_MODES,
    NUMBER_OF_PRESET_MODES,
    SUPPORTED_FAN_MODES,
    VERTICAL_SWING_MODE
)

_LOGGER = logging.getLogger(__name__)


MODE_TO_OPTIONS_MAPPING = {
    HORIZONTAL_SWING_MODE: SUPPORT_HORIZONTAL_SWING_MODES,
    VERTICAL_SWING_MODE: SUPPORT_SWING_MODES,
    FAN_MODE: SUPPORTED_FAN_MODES,
    HVAC_MODE: SUPPORTED_HVAC_MODES,
}


async def async_setup_entry(hass, entry, async_add_entities):
    """Setup select entries"""
    store = hass.data[DOMAIN][entry.entry_id][STORE]

    for device_obj in hass.data[DOMAIN].values():
        device = device_obj[API]
        if device.host == entry.data[CONF_HOST]:
            _LOGGER.info("Setup Select: %s, %s", device.name, device.airco_id)
            entities = [HorizontalSwingSelect(device), SwingSelect(device)]

            for i in range(1, NUMBER_OF_PRESET_MODES + 1):
                entities.extend(
                    [
                        PresetModeSelect(i, mode, store, hass)
                        for mode in MODE_TO_OPTIONS_MAPPING
                    ]
                )


            async_add_entities(entities)


class HorizontalSwingSelect(SelectEntity):
    """Select component to set the horizontal swing direction of the airco"""

    def __init__(self, device: Device) -> None:
        super().__init__()
        self._attr_options = SUPPORT_HORIZONTAL_SWING_MODES
        self._device = device
        self._attr_name = f"{device.name} horizontal swing direction"
        self._attr_device_info = device.device_info
        self._attr_icon = "mdi:weather-dust"
        self._attr_unique_id = (
            f"{DOMAIN}-{self._device.airco_id}-horizontal-swing-direction"
        )
        self.select_option(
            list(HORIZONTAL_SWING_MODE_TRANSLATION.keys())[
                self._device.airco.WindDirectionLR
            ]
        )

    def _update_state(self) -> None:
        self.select_option(
            list(HORIZONTAL_SWING_MODE_TRANSLATION.keys())[
                self._device.airco.WindDirectionLR
            ]
        )

    def select_option(self, option: str) -> None:
        """Change the selected option."""
        self._attr_current_option = option

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        await self._device.set_airco(
            {AirconCommands.WindDirectionLR: HORIZONTAL_SWING_MODE_TRANSLATION[option]}
        )
        self.select_option(option)

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Retrieve latest state."""
        await self._device.update()
        self._update_state()


class SwingSelect(SelectEntity):
    """Select component to set the swing direction of the airco"""

    def __init__(self, device: Device) -> None:
        super().__init__()
        self._attr_options = SUPPORT_SWING_MODES
        self._device = device
        self._attr_name = f"{device.name} swing direction"
        self._attr_device_info = device.device_info
        self._attr_icon = "mdi:weather-dust"
        self._attr_unique_id = (
            f"{DOMAIN}-{self._device.airco_id}-swing-direction"
        )
        self.select_option(
            list(SWING_MODE_TRANSLATION.keys())[
                self._device.airco.WindDirectionUD
            ]
        )

    def _update_state(self) -> None:
        self.select_option(
            SWING_3D_AUTO
            if self._device.airco.Entrust
            else list(SWING_MODE_TRANSLATION.keys())[
                self._device.airco.WindDirectionUD
            ]
        )

    def select_option(self, option: str) -> None:
        """Change the selected option."""
        self._attr_current_option = option

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        _airco = self._device.airco
        _swing_auto = option == SWING_3D_AUTO
        _swing_lr = (
            HORIZONTAL_SWING_MODE_TRANSLATION[SWING_HORIZONTAL_AUTO]
            if self._device.airco.Entrust
            else self._device.airco.WindDirectionLR
        )
        _swing_ud = _airco.WindDirectionUD

        if option != SWING_3D_AUTO:
            _swing_ud = SWING_MODE_TRANSLATION[option]

        await self._device.set_airco(
            {
                AirconCommands.WindDirectionUD: _swing_ud,
                AirconCommands.WindDirectionLR: _swing_lr,
                AirconCommands.Entrust: _swing_auto,
            }
        )
        self.select_option(option)

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Retrieve latest state."""
        await self._device.update()
        self._update_state()



class PresetModeSelect(SelectEntity, RestoreEntity):
    """Preset mode selects for swing and fan speed"""

    def __init__(self, i, mode, store, hass):
        self._hass = hass
        super().__init__()

        self.store = store
        self.i = i
        self.mode = mode

        # self.zone_variable = zone_variable
        self._attr_name = f"{DOMAIN} preset mode { i } { mode }"
        self._attr_unique_id = f"select_{DOMAIN}_{i}_{mode}"

        # self._current_option = None

        self._options = MODE_TO_OPTIONS_MAPPING[mode]

    async def async_added_to_hass(self) -> None:
        """Run when entity about to be added."""
        await super().async_added_to_hass()

        state = await self.async_get_last_state()
        if state and state.state in self._options:
            self.store[PRESET_MODES][self.i][self.mode] = state.state

    @property
    def options(self) -> list[str]:
        """Return the available options."""
        return self._options

    @property
    def current_option(self) -> str:
        """Return current options."""
        return self.store[PRESET_MODES][self.i][self.mode]

    async def async_select_option(self, option: str) -> None:
        """Select new (option)."""
        self.store[PRESET_MODES][self.i][self.mode] = option
        self.async_write_ha_state()
