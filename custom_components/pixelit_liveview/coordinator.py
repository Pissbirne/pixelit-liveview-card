"""Persistent WebSocket client for PixelIt Liveview."""
from __future__ import annotations

import asyncio
import json
import logging
import re
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
HEX_FRAME = re.compile(r"[0-9a-fA-F]+")


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
                if self._connected:
                    self._connected = False
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
                        _LOGGER.debug(
                            "PixelIt sent no frames for %.0fs, reconnecting", RECEIVE_TIMEOUT
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
        frame = obj["liveview"][: self._width * self._height * 6]
        frame = frame[: len(frame) - len(frame) % 6]
        if not HEX_FRAME.fullmatch(frame):
            return

        self._had_data = True
        if frame != self._hex:
            self._hex = frame
            self._publish()
