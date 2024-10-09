"""for select component used for horizontal swing."""
# pylint: disable = too-few-public-methods

import logging

from . import MitsubishiWfRacConfigEntry
from homeassistant.components.select import SelectEntity

from .wfrac.models.aircon import AirconCommands
from .wfrac.device import Device
from .const import (
    DOMAIN,
    HORIZONTAL_SWING_MODE_TRANSLATION,
    SUPPORT_HORIZONTAL_SWING_MODES,
    SUPPORT_SWING_MODES,
    SWING_MODE_TRANSLATION,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry: MitsubishiWfRacConfigEntry, async_add_entities):
    """Setup select entries"""

    device: Device = entry.runtime_data.device
    _LOGGER.info("Setup Horizontal and Vertical Select: %s, %s", device.name, device.airco_id)
    entities = [HorizontalSwingSelect(device), VerticalSwingSelect(device)]

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
        self._attr_available = self._device.available

    def select_option(self, option: str) -> None:
        """Change the selected option."""
        self._attr_current_option = option

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        await self._device.set_airco(
            {AirconCommands.WindDirectionLR: HORIZONTAL_SWING_MODE_TRANSLATION[option]}
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
        self._attr_name = f"{device.name} vertical swing direction"
        self._attr_device_info = device.device_info
        self._attr_icon = "mdi:weather-dust"
        self._attr_unique_id = (
            f"{DOMAIN}-{self._device.airco_id}-vertical-swing-direction"
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
        self._attr_available = self._device.available

    def select_option(self, option: str) -> None:
        """Change the selected option."""
        self._attr_current_option = option

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        await self._device.set_airco(
            {AirconCommands.WindDirectionUD: SWING_MODE_TRANSLATION[option]}
        )
        self.select_option(option)

    async def async_update(self):
        """Retrieve latest state."""
        self._update_state()
