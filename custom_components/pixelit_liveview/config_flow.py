"""Config flow for the PixelIt Liveview integration.

Lets the user configure the PixelIt display (IP, port, matrix size) through the
Home Assistant UI (Einstellungen → Geräte & Dienste → Integration hinzufügen)
instead of editing configuration.yaml. Includes a connection test so the user
gets immediate feedback.

Field labels are localized via strings.json / translations (DE/EN).
"""
from __future__ import annotations

import logging

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_HEIGHT,
    CONF_WIDTH,
    DEFAULT_HEIGHT,
    DEFAULT_HOST,
    DEFAULT_PORT,
    DEFAULT_WIDTH,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


async def _test_connection(hass: HomeAssistant, host: str, port: int) -> bool:
    """Try to open a WebSocket to the PixelIt to verify the connection."""
    url = f"ws://{host}:{port}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(url, timeout=5) as ws:
                await ws.close()
        return True
    except Exception:  # noqa: BLE001
        return False


class PixelItLiveviewConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for PixelIt Liveview."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input[CONF_PORT]
            await self.async_set_unique_id(host)
            self._abort_if_unique_id_configured()

            if await _test_connection(self.hass, host, port):
                return self.async_create_entry(
                    title=host,
                    data={
                        CONF_HOST: host,
                        CONF_PORT: port,
                        CONF_WIDTH: user_input[CONF_WIDTH],
                        CONF_HEIGHT: user_input[CONF_HEIGHT],
                    },
                )
            errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST, default=DEFAULT_HOST): str,
                    vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
                    vol.Required(CONF_WIDTH, default=DEFAULT_WIDTH): int,
                    vol.Required(CONF_HEIGHT, default=DEFAULT_HEIGHT): int,
                }
            ),
            errors=errors,
        )
