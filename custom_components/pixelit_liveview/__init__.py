"""PixelIt Liveview integration.

Connects to a PixelIt matrix display's WebSocket (port 81) and exposes the
current live pixel content as a Home Assistant sensor. The sensor state is a
short status string; the full liveview hex + parsed pixels live in attributes.

Uses aiohttp (bundled with HA) for the WebSocket client — no external
dependency. The state is written directly via hass.states.async_set, which is
the most robust path for a YAML-only integration (no config flow / platform
registration needed).
"""
from __future__ import annotations

import logging

from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant

from .const import DOMAIN, SENSOR_ENTITY_ID
from .coordinator import PixelItLiveviewCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the integration from configuration.yaml (no config flow)."""
    conf = config.get(DOMAIN)
    if not conf:
        return True
    host = conf.get(CONF_HOST, "192.168.178.8")
    port = conf.get(CONF_PORT, 81)
    width = conf.get("width", 32)
    height = conf.get("height", 8)
    coordinator = PixelItLiveviewCoordinator(hass, host, port, width, height)
    hass.data.setdefault(DOMAIN, {})["coordinator"] = coordinator
    await coordinator.async_start()
    return True
