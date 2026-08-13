"""PixelIt Liveview integration.

Connects to a PixelIt matrix display's WebSocket (port 81) and exposes the
current live pixel content as a Home Assistant sensor. The sensor state is a
short status string; the full liveview hex + parsed pixels live in attributes.

Uses aiohttp (bundled with HA) for the WebSocket client — no external
dependency. Configured via a config flow (HA UI), not configuration.yaml.
"""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant

from .const import CONF_HEIGHT, CONF_WIDTH, DOMAIN
from .coordinator import PixelItLiveviewCoordinator
from .frontend import ensure_frontend

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the integration from a config entry (created via the HA UI)."""
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    width = entry.data.get(CONF_WIDTH, 32)
    height = entry.data.get(CONF_HEIGHT, 8)

    coordinator = PixelItLiveviewCoordinator(hass, host, port, width, height)
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await coordinator.async_start()

    # Register the Lovelace card as a frontend resource automatically.
    await ensure_frontend(hass)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    coordinator = hass.data[DOMAIN].get(entry.entry_id)
    if coordinator:
        await coordinator.async_stop()
    hass.data[DOMAIN].pop(entry.entry_id, None)
    return True
