"""PixelIt Liveview integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT, Platform
from homeassistant.core import HomeAssistant

from .const import CONF_HEIGHT, CONF_WIDTH, DEFAULT_HEIGHT, DEFAULT_WIDTH
from .coordinator import PixelItLiveviewCoordinator
from .frontend import ensure_frontend

type PixelItConfigEntry = ConfigEntry[PixelItLiveviewCoordinator]
PLATFORMS = (Platform.SENSOR,)


async def async_setup_entry(hass: HomeAssistant, entry: PixelItConfigEntry) -> bool:
    """Set up PixelIt from a config entry."""
    entry.runtime_data = PixelItLiveviewCoordinator(
        hass,
        entry.data[CONF_HOST],
        entry.data[CONF_PORT],
        entry.data.get(CONF_WIDTH, DEFAULT_WIDTH),
        entry.data.get(CONF_HEIGHT, DEFAULT_HEIGHT),
    )
    await ensure_frontend(hass)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.runtime_data.async_start(hass, entry)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: PixelItConfigEntry) -> bool:
    """Unload the sensor and stop the WebSocket client."""
    if not await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        return False
    await entry.runtime_data.async_stop()
    return True
