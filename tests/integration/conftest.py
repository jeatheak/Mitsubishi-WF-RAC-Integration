"""Fixtures shared by the integration tests."""

from unittest.mock import AsyncMock

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.mitsubishi_wf_rac.const import DOMAIN
from custom_components.mitsubishi_wf_rac.coordinator import Device

from ..unit.live_captures import LIVE_CAPTURES


@pytest.fixture
async def platform_device(hass):
    """A Device holding one parsed live capture, with the API mocked out."""
    entry = MockConfigEntry(domain=DOMAIN, options={})
    entry.add_to_hass(hass)
    device = Device(hass, entry, "Test AC", "127.0.0.1", 51443, "device-id", "operator-id", "airco-id", swing_selects_enabled_default=True)
    device._api = AsyncMock()
    device._api.get_aircon_stats.return_value = {"numOfAccount": 1, "airconStat": LIVE_CAPTURES["on_cool"][0]}
    await device.update()
    return device
