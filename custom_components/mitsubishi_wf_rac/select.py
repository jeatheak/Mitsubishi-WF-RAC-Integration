"""for select component used for horizontal swing."""
# pylint: disable = too-few-public-methods

import logging

from . import MitsubishiWfRacConfigEntry
from homeassistant.components.select import SelectEntity

from .wfrac.models.aircon import AirconCommands
from .wfrac.device import Device
from .const import (
    DOMAIN,
    SWING_HORIZONTAL_MODE_TRANSLATION,
    SUPPORT_SWING_HORIZONTAL_MODES,
    SUPPORT_SWING_MODES,
    SWING_MODE_TRANSLATION, SWING_3D_AUTO,
    FAN_MODE_TRANSLATION,
    SUPPORTED_FAN_MODES,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(_hass, entry: MitsubishiWfRacConfigEntry, async_add_entities):
    """Setup select entries"""

    device: Device = entry.runtime_data.device
    _LOGGER.info("Setup Fan, Horizontal and Vertical Select: %s, %s", device.device_name, device.airco_id)
    if device.create_swing_mode_select:
        entities = [HorizontalSwingSelect(device), VerticalSwingSelect(device), FanSpeedSelect(device)]
        async_add_entities(entities)
    else:
        _LOGGER.info("No Setup Horizontal Select: %s, %s", device.device_name, device.airco_id)


class HorizontalSwingSelect(SelectEntity):
    """Select component to set the horizontal swing direction of the airco"""

    def __init__(self, device: Device) -> None:
        super().__init__()
        self._attr_options = SUPPORT_SWING_HORIZONTAL_MODES
        self._device = device
        self._attr_name = f"{device.device_name} horizontal swing direction"
        self._attr_device_info = device.device_info
        self._attr_icon = "mdi:weather-dust"
        self._attr_unique_id = (
            f"{DOMAIN}-{self._device.airco_id}-horizontal-swing-direction"
        )
        self.select_option(
            SWING_3D_AUTO
            if self._device.airco.Entrust
            else
            list(SWING_HORIZONTAL_MODE_TRANSLATION.keys())[
                self._device.airco.WindDirectionLR
            ]
        )

    def _update_state(self) -> None:
        self.select_option(
            SWING_3D_AUTO
            if self._device.airco.Entrust
            else
            list(SWING_HORIZONTAL_MODE_TRANSLATION.keys())[
                self._device.airco.WindDirectionLR
            ]
        )
        self._attr_available = self._device.available

    def select_option(self, option: str) -> None:
        """Change the selected option."""
        self._attr_current_option = option

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        _swing_auto = option == SWING_3D_AUTO
        if _swing_auto:
            await self._device.set_airco(
                {
                    AirconCommands.Entrust: _swing_auto,
                }
            )
        else:
            await self._device.set_airco(
                {
                    AirconCommands.WindDirectionLR: SWING_HORIZONTAL_MODE_TRANSLATION[option],
                    AirconCommands.Entrust: False,
                }
            )
        self.select_option(option)

    async def async_update(self):
        """Retrieve latest state."""
        self._update_state()

class VerticalSwingSelect(SelectEntity):
    """Select component to set the vertical swing direction of the airco"""

    def __init__(self, device: Device) -> None:
        super().__init__()
        self._attr_options = SUPPORT_SWING_MODES
        self._device = device
        self._attr_name = f"{device.device_name} vertical swing direction"
        self._attr_device_info = device.device_info
        self._attr_icon = "mdi:weather-dust"
        self._attr_unique_id = (
            f"{DOMAIN}-{self._device.airco_id}-vertical-swing-direction"
        )
        self.select_option(
            SWING_3D_AUTO
            if self._device.airco.Entrust
            else list(SWING_MODE_TRANSLATION.keys())[
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
        self._attr_available = self._device.available

    def select_option(self, option: str) -> None:
        """Change the selected option."""
        self._attr_current_option = option

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        _swing_auto = option == SWING_3D_AUTO
        if _swing_auto:
            await self._device.set_airco(
                {
                    AirconCommands.Entrust: _swing_auto,
                }
            )
        else:
            await self._device.set_airco(
                {
                    AirconCommands.WindDirectionUD: SWING_MODE_TRANSLATION[option],
                    AirconCommands.Entrust: False,
                }
            )
        self.select_option(option)

    async def async_update(self):
        """Retrieve latest state."""
        self._update_state()

class FanSpeedSelect(SelectEntity):
    """Select component to set the fan speed of the airco"""

    def __init__(self, device: Device) -> None:
        super().__init__()
        self._attr_options = SUPPORTED_FAN_MODES
        self._device = device
        self._attr_name = f"{device.device_name} fan speed"
        self._attr_device_info = device.device_info
        self._attr_icon = "mdi:fan"
        self._attr_unique_id = f"{DOMAIN}-{self._device.airco_id}-fan-speed"
        self._update_state()

    def _update_state(self) -> None:
        self.select_option(list(FAN_MODE_TRANSLATION.keys())[self._device.airco.AirFlow])
        self._attr_available = self._device.available

    def select_option(self, option: str) -> None:
        """Change the selected option."""
        self._attr_current_option = option

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        await self._device.set_airco(
            {
                AirconCommands.AirFlow: FAN_MODE_TRANSLATION[option]
            }
        )
        self.select_option(option)

    async def async_update(self):
        """Retrieve latest state."""
        self._update_state()
