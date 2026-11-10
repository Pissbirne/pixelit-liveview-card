"""Configure a PixelIt display through Home Assistant."""
from __future__ import annotations

import asyncio

import aiohttp
import voluptuous as vol
from yarl import URL

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    CONF_HEIGHT,
    CONF_WIDTH,
    DEFAULT_HEIGHT,
    DEFAULT_HOST,
    DEFAULT_PORT,
    DEFAULT_WIDTH,
    DOMAIN,
)


async def _test_connection(hass: HomeAssistant, host: str, port: int) -> bool:
    """Verify the PixelIt WebSocket handshake within five seconds."""
    try:
        url = URL.build(scheme="ws", host=host, port=port)
        session = async_get_clientsession(hass)
        async with asyncio.timeout(5):
            async with session.ws_connect(url):
                return True
    except (aiohttp.ClientError, OSError, TimeoutError, ValueError):
        return False


class PixelItLiveviewConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for PixelIt Liveview."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST].strip()
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

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST, default=DEFAULT_HOST): str,
                vol.Required(CONF_PORT, default=DEFAULT_PORT): vol.All(
                    int, vol.Range(min=1, max=65535)
                ),
                vol.Required(CONF_WIDTH, default=DEFAULT_WIDTH): vol.All(
                    int, vol.Range(min=1)
                ),
                vol.Required(CONF_HEIGHT, default=DEFAULT_HEIGHT): vol.All(
                    int, vol.Range(min=1)
                ),
            }
        )
        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(schema, user_input),
            errors=errors,
        )
