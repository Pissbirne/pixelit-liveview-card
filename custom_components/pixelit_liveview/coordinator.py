"""Persistent WebSocket client for PixelIt Liveview."""
from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import Callable
from contextlib import suppress

import aiohttp
from yarl import URL

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

# If we previously received liveview data on the current connection but then
# nothing arrives within this window, treat the connection as stale and reconnect.
RECEIVE_TIMEOUT = 15.0


class PixelItLiveviewCoordinator:
    """Fetch liveview data from a PixelIt display over WebSocket."""

    def __init__(self, hass: HomeAssistant, host: str, port: int, width: int, height: int):
        """Initialize."""
        self._session = async_get_clientsession(hass)
        self.on_update: Callable[[], None] | None = None
        self._host = host
        self._port = port
        self._width = width
        self._height = height
        self._task: asyncio.Task | None = None
        self._connected = False
        self._hex = ""
        self._pixels: list[dict] = []
        self._had_data = False

    @property
    def ws_url(self) -> URL:
        """Build the WebSocket URL, including IPv6 support."""
        return URL.build(scheme="ws", host=self._host, port=self._port)

    def async_start(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Start an entry-owned task without delaying HA startup."""
        self._task = entry.async_create_background_task(
            hass, self._ws_loop(), "pixelit_liveview_websocket"
        )

    async def async_stop(self) -> None:
        """Wait for the WebSocket context to close."""
        if self._task is not None:
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task
            self._task = None

    def clear_listener(self) -> None:
        """Detach the sensor callback."""
        self.on_update = None

    @property
    def connected(self) -> bool:
        """Return the current connection status."""
        return self._connected

    @property
    def attributes(self) -> dict:
        """Return the latest frame."""
        return {
            "connected": self._connected,
            "width": self._width,
            "height": self._height,
            "hex": self._hex,
            "pixels": self._pixels,
        }

    def _publish(self) -> None:
        if self.on_update is not None:
            self.on_update()

    async def _ws_loop(self) -> None:
        """Keep the WebSocket connected and read liveview messages."""
        while True:
            try:
                await self._run_connection()
            except (aiohttp.ClientError, OSError, TimeoutError) as err:
                _LOGGER.debug("PixelIt WebSocket error for %s: %s", self._host, err)
            finally:
                self._connected = False
                self._had_data = False
                self._publish()
            await asyncio.sleep(5)

    async def _run_connection(self) -> None:
        """Run a single WebSocket connection until it is stale, closed, or errors."""
        async with self._session.ws_connect(self.ws_url) as ws:
            self._connected = True
            self._had_data = False
            self._publish()
            _LOGGER.debug("Connected to %s", self.ws_url)
            while True:
                try:
                    msg = await asyncio.wait_for(ws.receive(), timeout=RECEIVE_TIMEOUT)
                except asyncio.TimeoutError:
                    if self._had_data:
                        _LOGGER.warning(
                            "PixelIt connection stale (no data for %.0fs), reconnecting", RECEIVE_TIMEOUT
                        )
                        raise
                    # No data has ever arrived on this connection — PixelIt may
                    # legitimately be idle. Keep waiting instead of hammering it.
                    continue
                if msg.type == aiohttp.WSMsgType.TEXT:
                    self._handle_message(msg.data)
                elif msg.type in (
                    aiohttp.WSMsgType.CLOSED,
                    aiohttp.WSMsgType.ERROR,
                    aiohttp.WSMsgType.CLOSE,
                ):
                    break

    def _handle_message(self, message) -> None:
        if not isinstance(message, str):
            return
        try:
            obj = json.loads(message)
        except (json.JSONDecodeError, TypeError):
            return
        if not isinstance(obj, dict) or not isinstance(obj.get("liveview"), str):
            return
        hex_str = obj["liveview"]
        self._hex = hex_str
        self._pixels = self._parse_hex(hex_str)
        self._connected = True
        self._had_data = True
        self._publish()

    def _parse_hex(self, hex_str: str) -> list[dict]:
        """Parse the liveview hex string into a list of {r,g,b} pixels."""
        pixels: list[dict] = []
        expected = self._width * self._height * 6
        s = hex_str[:expected] if len(hex_str) >= expected else hex_str
        for i in range(0, len(s), 6):
            chunk = s[i : i + 6]
            if len(chunk) < 6:
                break
            try:
                r = int(chunk[0:2], 16)
                g = int(chunk[2:4], 16)
                b = int(chunk[4:6], 16)
            except ValueError:
                continue
            pixels.append({"r": r, "g": g, "b": b})
        return pixels
