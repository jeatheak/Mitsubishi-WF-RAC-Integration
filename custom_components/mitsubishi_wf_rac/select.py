""" for select component used for horizontal swing."""
# pylint: disable = too-few-public-methods

import logging

from homeassistant.components.select import SelectEntity
from homeassistant.const import CONF_HOST
from homeassistant.util import Throttle

from .wfrac.models.aircon import AirconCommands
from .wfrac.device import MIN_TIME_BETWEEN_UPDATES, Device
from .const import (
    DOMAIN,
    HORIZONTAL_SWING_MODE_TRANSLATION,
    SWING_3D_AUTO,
    SWING_MODE_TRANSLATION,
    SWING_HORIZONTAL_AUTO,
    SUPPORT_HORIZONTAL_SWING_MODES,
    SUPPORT_SWING_MODES
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Setup select entries"""

    for device in hass.data[DOMAIN]:
        if device.host == entry.data[CONF_HOST]:
            _LOGGER.info("Setup Select: %s, %s", device.name, device.airco_id)
            entities = [HorizontalSwingSelect(device), SwingSelect(device)]

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
            list(SWING_MODE_TRANSLATION.keys())[
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
