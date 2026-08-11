"""DataUpdateCoordinator for the PixelIt Liveview integration.

Maintains a persistent WebSocket connection to the PixelIt display and
publishes the latest liveview hex string + parsed pixels to HA.

Uses aiohttp (bundled with HA) for the WebSocket client — no external
dependency. The state is written directly via hass.states.async_set, which
works without a config flow or platform registration.

Stale-connection watchdog: PixelIt only pushes liveview data when the pixel
checksum changes (i.e. when the clock/display actually updates). If the display
content changes in the WebUI, the active screen can freeze and the WebSocket
connection can go "stale" — still open (so HA shows "connected") but no longer
receiving updates. Only a fresh connection (e.g. HA restart) recovers it. To
make this self-healing, we track whether data has ever arrived on the current
connection; if it has but then stops for RECEIVE_TIMEOUT seconds, we force a
reconnect. A reconnect opens a new connection exactly like an HA restart would.
"""
from __future__ import annotations

import asyncio
import json
import logging

import aiohttp

from homeassistant.core import HomeAssistant

from .const import DOMAIN, SENSOR_ENTITY_ID, SENSOR_NAME

_LOGGER = logging.getLogger(__name__)

# If we previously received liveview data on the current connection but then
# nothing arrives within this window, treat the connection as stale and reconnect.
RECEIVE_TIMEOUT = 15.0


class PixelItLiveviewCoordinator:
    """Fetch liveview data from a PixelIt display over WebSocket."""

    def __init__(self, hass: HomeAssistant, host: str, port: int, width: int, height: int):
        """Initialize."""
        self._hass = hass
        self._host = host
        self._port = port
        self._width = width
        self._height = height
        self._ws = None
        self._task: asyncio.Task | None = None
        self._connected = False
        self._hex = ""
        self._pixels: list[dict] = []
        self._had_data = False

    @property
    def ws_url(self) -> str:
        """WebSocket URL."""
        return f"ws://{self._host}:{self._port}"

    async def async_start(self) -> None:
        """Start the background WebSocket loop."""
        if self._task is None:
            self._task = self._hass.async_create_task(self._ws_loop())

    async def async_stop(self) -> None:
        """Stop the background WebSocket loop."""
        if self._task:
            self._task.cancel()
            self._task = None
        if self._ws:
            await self._ws.close()
            self._ws = None

    def _write_state(self) -> None:
        """Write the sensor state + attributes directly to HA."""
        state = "connected" if self._connected else "disconnected"
        attrs = {
            "friendly_name": SENSOR_NAME,
            "icon": "mdi:led-strip-variant",
            "connected": self._connected,
            "width": self._width,
            "height": self._height,
            "hex": self._hex,
            "pixels": self._pixels,
        }
        self._hass.states.async_set(SENSOR_ENTITY_ID, state, attrs)

    async def _ws_loop(self) -> None:
        """Keep the WebSocket connected and read liveview messages."""
        session = aiohttp.ClientSession()
        try:
            while True:
                try:
                    await self._run_connection(session)
                except asyncio.CancelledError:
                    raise
                except Exception as err:  # noqa: BLE001
                    _LOGGER.warning("PixelIt WebSocket error: %s", err)
                finally:
                    self._ws = None
                    self._connected = False
                    self._had_data = False
                    self._write_state()
                await asyncio.sleep(5)
        finally:
            await session.close()

    async def _run_connection(self, session: aiohttp.ClientSession) -> None:
        """Run a single WebSocket connection until it is stale, closed, or errors."""
        async with session.ws_connect(self.ws_url) as ws:
            self._ws = ws
            self._connected = True
            self._had_data = False
            self._write_state()
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
        self._write_state()

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
