""" for text component used for preset mode name."""
# pylint: disable = too-few-public-methods

import logging

from homeassistant.components.text import TextEntity

from homeassistant.const import CONF_HOST
from homeassistant.helpers.restore_state import RestoreEntity

from .const import (
    API,
    DOMAIN,
    NAME,
    PRESET_MODES,
    STORE,
    NUMBER_OF_PRESET_MODES,

)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Setup text entries"""
    store = hass.data[DOMAIN][entry.entry_id][STORE]

    for device_obj in hass.data[DOMAIN].values():
        device = device_obj[API]
        if device.host == entry.data[CONF_HOST]:
            _LOGGER.info("Setup text: %s, %s", device.name, device.airco_id)
            entities: list(TextEntity) = []

            # entities.extend(
            #     [
            #         PresetModeText(i, store, hass)
            #         for i in range(1, NUMBER_OF_PRESET_MODES + 1)
            #     ]
            # )

            # async_add_entities(entities)

class PresetModeText(TextEntity, RestoreEntity):
    """Preset mode text"""

    def __init__(self, i, store, hass):
        self._hass = hass
        super().__init__()

        self.i = i
        self.store = store
        self._attr_name = f"{DOMAIN} preset mode {i} name"
        self._attr_unique_id = f"text_{DOMAIN}_{i}_name"
        self._state = 0

    async def async_added_to_hass(self) -> None:
        """Run when entity about to be added."""
        await super().async_added_to_hass()

        state = await self.async_get_last_state()
        if state and state.state:
            self.store[PRESET_MODES][self.i][NAME] = state.state

    @property
    def native_value(self) -> float:
        """Return the state of the entity."""
        return self.store[PRESET_MODES][self.i][NAME]

    async def async_set_value(self, value: str) -> None:
        """Update the current value."""
        self.store[PRESET_MODES][self.i][NAME] = value
        self.async_write_ha_state()
