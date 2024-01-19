""" for Climate integration."""
from __future__ import annotations
import asyncio
from datetime import timedelta
import logging
from typing import Any

import voluptuous as vol

from homeassistant.components.climate import (
    ClimateEntity,
    ConfigEntry,
)
from homeassistant.components.climate.const import HVACMode, FAN_AUTO
from homeassistant.const import UnitOfTemperature, ATTR_TEMPERATURE
from homeassistant.util import Throttle
from homeassistant.const import CONF_HOST
from homeassistant.helpers import config_validation as cv, entity_platform
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.typing import HomeAssistantType

from .wfrac.device import MIN_TIME_BETWEEN_UPDATES, Device
from .wfrac.models.aircon import AirconCommands
from .const import (
    API,
    CURRENT_PRESET_MODE,
    DOMAIN,
    FAN_MODE,
    FAN_MODE_TRANSLATION,
    HORIZONTAL_SWING_MODE,
    HVAC_MODE,
    HVAC_TRANSLATION,
    NAME,
    PRESET_MODES,
    SERVICE_SET_HORIZONTAL_SWING_MODE,
    SERVICE_SET_VERTICAL_SWING_MODE,
    STORE,
    SUPPORT_FLAGS,
    SWING_HORIZONTAL_AUTO,
    SWING_VERTICAL_AUTO,
    SUPPORT_SWING_MODES,
    SUPPORTED_FAN_MODES,
    SUPPORTED_HVAC_MODES,
    SWING_3D_AUTO,
    SWING_MODE_TRANSLATION,
    HORIZONTAL_SWING_MODE_TRANSLATION,
    TEMPERATURE,
    VERTICAL_SWING_MODE,
)

_LOGGER = logging.getLogger(__name__)
MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=10)
UPDATE_CONSOLIDATION_PERIOD = timedelta(milliseconds=500)


async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities):
    """Setup climate entities"""
    store = hass.data[DOMAIN][entry.entry_id][STORE]
    
    for device_obj in hass.data[DOMAIN].values():
        device = device_obj[API]
        if device.host == entry.data[CONF_HOST]:
            _LOGGER.info("Setup climate for: %s, %s", device.name, device.airco_id)
            async_add_entities([AircoClimate(device, hass, store)])

    platform = entity_platform.async_get_current_platform()

    platform.async_register_entity_service(
        SERVICE_SET_HORIZONTAL_SWING_MODE,
        {
            vol.Required("swing_mode"): cv.string,
        },
        "async_set_horizontal_swing_mode",
    )

    platform.async_register_entity_service(
        SERVICE_SET_VERTICAL_SWING_MODE,
        {
            vol.Required("swing_mode"): cv.string,
        },
        "async_set_swing_mode",
    )


class AircoClimate(ClimateEntity, RestoreEntity):
    """Representation of a climate entity"""

    _attr_supported_features: int = SUPPORT_FLAGS
    _attr_temperature_unit: str = UnitOfTemperature.CELSIUS
    _attr_hvac_modes: list[HVACMode] = SUPPORTED_HVAC_MODES
    _attr_fan_modes: list[str] = SUPPORTED_FAN_MODES
    _attr_hvac_mode: HVACMode = HVACMode.OFF
    _attr_fan_mode: str = FAN_AUTO
    _attr_swing_mode: str | None = SWING_VERTICAL_AUTO
    _attr_swing_modes: list[str] | None = SUPPORT_SWING_MODES
    _attr_horizontal_swing_mode: str | None = SWING_HORIZONTAL_AUTO
    # _attr_horizontal_swing_modes: list[str] | None = SUPPORT_HORIZONTAL_SWING_MODES
    _attr_min_temp: float = 16
    _attr_max_temp: float = 30
    preset_mode: any = None

    def __init__(self, device: Device, hass:HomeAssistantType, store) -> None:
        self._device = device
        self._hass = hass
        self.store = store
        self._attr_name = device.name
        self._attr_device_info = device.device_info
        self._attr_unique_id = f"{DOMAIN}-{self._device.airco_id}-climate"
        self._consolidatedParams = {}
        self._update_state()

    async def async_added_to_hass(self):
        """Register for sensor updates."""
        # state = await self.async_get_last_state()
        self.store[CURRENT_PRESET_MODE] = self.store[PRESET_MODES][1][NAME]

    async def async_set_temperature(self, **kwargs) -> None:
        """Set new target temperature."""
        opts = {AirconCommands.PresetTemp: kwargs.get(ATTR_TEMPERATURE)}

        if "hvac_mode" in kwargs:
            hvac_mode = kwargs.get("hvac_mode")
            opts.update(
                {
                    AirconCommands.OperationMode: self._device.airco.OperationMode
                    if hvac_mode == HVACMode.OFF
                    else HVAC_TRANSLATION[hvac_mode],
                    AirconCommands.Operation: hvac_mode != HVACMode.OFF,
                }
            )

        await self._set_airco(opts)

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        """Set new target fan mode."""
        await self._set_airco(
            {AirconCommands.AirFlow: FAN_MODE_TRANSLATION[fan_mode]}
        )

    async def async_turn_on(self) -> None:
        """Turn the entity on."""
        await self._set_airco({AirconCommands.Operation: True})

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target hvac mode."""
        await self._set_airco(
            {
                AirconCommands.OperationMode: self._device.airco.OperationMode
                if hvac_mode == HVACMode.OFF
                else HVAC_TRANSLATION[hvac_mode],
                AirconCommands.Operation: hvac_mode != HVACMode.OFF,
            }
        )

    async def async_set_swing_mode(self, swing_mode: str) -> None:
        """Set new target swing operation."""
        _airco = self._device.airco
        _swing_auto = swing_mode == SWING_3D_AUTO
        _swing_lr = (
            HORIZONTAL_SWING_MODE_TRANSLATION[SWING_HORIZONTAL_AUTO]
            if self._device.airco.Entrust
            else self._device.airco.WindDirectionLR
        )
        _swing_ud = _airco.WindDirectionUD

        if swing_mode != SWING_3D_AUTO:
            _swing_ud = SWING_MODE_TRANSLATION[swing_mode]

        await self._set_airco(
            {
                AirconCommands.WindDirectionUD: _swing_ud,
                AirconCommands.WindDirectionLR: _swing_lr,
                AirconCommands.Entrust: _swing_auto,
            }
        )

    async def async_set_horizontal_swing_mode(self, swing_mode: str) -> None:
        """Set new target horizontal swing operation."""
        _airco = self._device.airco
        _swing_lr = HORIZONTAL_SWING_MODE_TRANSLATION[swing_mode]
        _swing_ud = (
            HORIZONTAL_SWING_MODE_TRANSLATION[SWING_VERTICAL_AUTO]
            if self._device.airco.Entrust
            else self._device.airco.WindDirectionUD
        )

        _LOGGER.debug("airco: %s", _airco)

        await self._set_airco(
            {
                AirconCommands.WindDirectionUD: _swing_ud,
                AirconCommands.WindDirectionLR: _swing_lr,
                AirconCommands.Entrust: False,  # always set to false otherwise sevice won't have effect
            }
        )

    async def async_turn_off(self) -> None:
        """Turn the entity off."""
        await self._set_airco({AirconCommands.Operation: False})
    
    async def _set_airco(self, params: dict[AirconCommands, Any]) -> None:
        will_do_update = not self._consolidatedParams
        self._consolidatedParams.update(params)
        
        if will_do_update:
            self._hass.async_add_job(self._set_airco_after_delay)

    async def _set_airco_after_delay(self):
        await asyncio.sleep(UPDATE_CONSOLIDATION_PERIOD.total_seconds())
        params = self._consolidatedParams.copy()
        self._consolidatedParams.clear()
        await self._device.set_airco(params)
        self._update_state()
        self.async_write_ha_state()

    @property
    def preset_mode(self):
        """Return the current preset mode"""
        self.determine_preset_mode()
        return self.store[CURRENT_PRESET_MODE]

    @property
    def preset_modes(self):
        """Return a list of available preset modes."""
        return [mode[NAME] for mode in self.store[PRESET_MODES].values()]

    def determine_preset_mode(self) -> str | None:
        """Method to determine preset mode"""
        # _LOGGER.error("Determine preset mode")

        self.store[CURRENT_PRESET_MODE] = None
        for mode in self.store[PRESET_MODES].values():
            if self._is_current_mode(mode):
                # _LOGGER.error("Determined mode %s", mode[NAME])
                self.store[CURRENT_PRESET_MODE] = mode[NAME]
                break

    def _is_current_mode(self, mode):
        # _LOGGER.error("Is current mode %s?", mode[NAME])
        if mode[HVAC_MODE] == HVACMode.OFF:
            return mode[HVAC_MODE] == self._attr_hvac_mode
        if mode[TEMPERATURE] != self._attr_target_temperature:
            return False
        if mode[FAN_MODE] != self._attr_fan_mode:
            return False
        if mode[VERTICAL_SWING_MODE] != self._attr_swing_mode:
            return False
        if mode[VERTICAL_SWING_MODE] != SWING_3D_AUTO and mode[HORIZONTAL_SWING_MODE] != self._attr_horizontal_swing_mode:
            return False
        
        return True

    async def async_set_preset_mode(self, preset_mode):
        """Set new preset mode."""
        self.store[CURRENT_PRESET_MODE] = preset_mode
        # self.async_write_ha_state()

        preset_mode_obj = None
        for mode in self.store[PRESET_MODES].values():
            if mode[NAME] == preset_mode:
                preset_mode_obj = mode

        if preset_mode_obj[HVAC_MODE] == HVACMode.OFF:
            await self.async_set_hvac_mode(preset_mode_obj[HVAC_MODE])
        else:

            opts = {
                AirconCommands.Operation: True,
                AirconCommands.PresetTemp: preset_mode_obj[TEMPERATURE],
                AirconCommands.AirFlow: FAN_MODE_TRANSLATION[preset_mode_obj[FAN_MODE]],

            }

            vertical_swing_mode = preset_mode_obj[VERTICAL_SWING_MODE]
            horizontal_swing_mode = preset_mode_obj[HORIZONTAL_SWING_MODE]
            _swing_auto = vertical_swing_mode == SWING_3D_AUTO
            _swing_lr = (
                HORIZONTAL_SWING_MODE_TRANSLATION[SWING_HORIZONTAL_AUTO]
                if _swing_auto
                else HORIZONTAL_SWING_MODE_TRANSLATION[horizontal_swing_mode]
            )
            _swing_ud = self._device.airco.WindDirectionUD

            if vertical_swing_mode != SWING_3D_AUTO:
                _swing_ud = SWING_MODE_TRANSLATION[vertical_swing_mode]

            opts.update({
                AirconCommands.WindDirectionUD: _swing_ud,
                AirconCommands.WindDirectionLR: _swing_lr,
                AirconCommands.Entrust: _swing_auto,
            })

            _LOGGER.debug(opts)

            await self._set_airco(opts)

    def _update_state(self) -> None:
        """Private update attributes"""
        airco = self._device.airco

        self._attr_target_temperature = airco.PresetTemp
        self._attr_current_temperature = airco.IndoorTemp
        self._attr_fan_mode = list(FAN_MODE_TRANSLATION.keys())[airco.AirFlow]
        self._attr_swing_mode = (
            SWING_3D_AUTO
            if airco.Entrust
            else list(SWING_MODE_TRANSLATION.keys())[airco.WindDirectionUD]
        )
        self._attr_horizontal_swing_mode = list(
            HORIZONTAL_SWING_MODE_TRANSLATION.keys())[airco.WindDirectionLR]
        self._attr_hvac_mode = list(HVAC_TRANSLATION.keys())[airco.OperationMode]

        if airco.Operation is False:
            self._attr_hvac_mode = HVACMode.OFF
        else:
            _new_mode: HVACMode = None
            _mode = airco.OperationMode
            if _mode == 0:
                _new_mode = HVACMode.AUTO
            elif _mode == 1:
                _new_mode = HVACMode.COOL
            elif _mode == 2:
                _new_mode = HVACMode.HEAT
            elif _mode == 3:
                _new_mode = HVACMode.FAN_ONLY
            elif _mode == 4:
                _new_mode = HVACMode.DRY
            self._attr_hvac_mode = _new_mode
        
        self.determine_preset_mode()

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Retrieve latest state."""
        await self._device.update()
        self._update_state()
