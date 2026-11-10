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
        return await self._async_configure("user", user_input)

    async def async_step_reconfigure(
        self, user_input: dict | None = None
    ) -> ConfigFlowResult:
        """Update the display address or dimensions on the existing entry."""
        return await self._async_configure("reconfigure", user_input)

    async def _async_configure(
        self, step_id: str, user_input: dict | None
    ) -> ConfigFlowResult:
        entry = self._get_reconfigure_entry() if step_id == "reconfigure" else None
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST].strip()
            port = user_input[CONF_PORT]
            if not host or any(char in host for char in "/?#@") or any(
                char.isspace() for char in host
            ):
                errors[CONF_HOST] = "invalid_host"
            else:
                existing = await self.async_set_unique_id(host)
                if existing is not None and (
                    entry is None or existing.entry_id != entry.entry_id
                ):
                    return self.async_abort(reason="already_configured")

                if await _test_connection(self.hass, host, port):
                    data = {**user_input, CONF_HOST: host}
                    if entry is None:
                        return self.async_create_entry(title=host, data=data)
                    self.hass.config_entries.async_update_entry(entry, unique_id=host)
                    return self.async_update_reload_and_abort(
                        entry, title=host, data_updates=data
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
            step_id=step_id,
            data_schema=self.add_suggested_values_to_schema(
                schema, user_input if user_input is not None else entry.data if entry else None
            ),
            errors=errors,
        )
