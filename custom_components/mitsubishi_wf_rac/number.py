""" for number component used for preset mode temperature."""
# pylint: disable = too-few-public-methods

import logging

from homeassistant.components.number import NumberEntity, RestoreNumber

from homeassistant.const import CONF_HOST

from .const import (
    API,
    DOMAIN,
    NAME,
    PRESET_MODES,
    STORE,
    NUMBER_OF_PRESET_MODES,
    TEMPERATURE,

)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Setup text entries"""
    store = hass.data[DOMAIN][entry.entry_id][STORE]

    for device_obj in hass.data[DOMAIN].values():
        device = device_obj[API]
        if device.host == entry.data[CONF_HOST]:
            _LOGGER.info("Setup text: %s, %s", device.name, device.airco_id)
            entities: list(NumberEntity) = []

            entities.extend(
                [
                    PresetModeNumber(i, store, hass)
                    for i in range(1, NUMBER_OF_PRESET_MODES + 1)
                ]
            )

            async_add_entities(entities)

class PresetModeNumber(RestoreNumber, NumberEntity):
    """Preset mode number"""

    def __init__(self, i, store, hass):
        self._hass = hass
        super().__init__()

        self.store = store
        self.i = i
        self._attr_name = f"{DOMAIN} preset mode { i } temperature"
        self._attr_unique_id = f"number_{DOMAIN}_{i}_temperature"
        self._state = 0

    async def async_added_to_hass(self) -> None:
        """Run when entity about to be added."""
        await super().async_added_to_hass()

        state = await self.async_get_last_number_data()
        if state and state.native_value:
            self.store[PRESET_MODES][self.i][TEMPERATURE] = state.native_value

    @property
    def native_min_value(self) -> float:
        return 18

    @property
    def native_max_value(self) -> float:
        return 30

    @property
    def native_step(self) -> float:
        return 1

    @property
    def native_value(self) -> float:
        """Return the state of the entity."""
        return self.store[PRESET_MODES][self.i][TEMPERATURE]

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        self.store[PRESET_MODES][self.i][TEMPERATURE] = value
        self.async_write_ha_state()
