"""Frontend support for the PixelIt Liveview integration.

Registers the bundled Lovelace card so the user does not have to add it
manually. Pattern follows thermostat_timeline (proven in HA 2026.8):

1) Copy the bundled card JS from the integration's www/ to /config/www/
   (served by HA at /local/...).
2) Register it as a Lovelace resource (storage mode).

Best-effort: failures must not block the integration or config flow.
"""
from __future__ import annotations

import hashlib
import logging
import shutil
from pathlib import Path

from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_call_later
from homeassistant.helpers.storage import Store

_LOGGER = logging.getLogger(__name__)

# The JS file shipped with this integration under ./www/
JS_FILENAME = "pixelit-liveview-card.js"

# Where Home Assistant serves files from config/www/ as /local/
RESOURCE_URL = f"/local/{JS_FILENAME}"
RESOURCE_TYPE = "module"


def _strip_query(url: str) -> str:
    try:
        return str(url).split("?", 1)[0]
    except Exception:
        return str(url)


def _token_from_hash(sha_hex: str) -> str:
    try:
        return str(int(sha_hex[:12], 16))
    except Exception:
        return sha_hex[:12] or "0"


def _get_lovelace_resources(hass: HomeAssistant):
    """Return the Lovelace ResourceStorageCollection when in storage mode, else None."""
    try:
        lovelace_data = hass.data.get("lovelace")
        if lovelace_data is None:
            return None
        resources = None
        if hasattr(lovelace_data, "resources"):
            resources = lovelace_data.resources
        elif isinstance(lovelace_data, dict):
            resources = lovelace_data.get("resources")
        if resources is None:
            return None
        if not hasattr(resources, "store") or resources.store is None:
            return None
        for attr in ("async_items", "async_create_item", "async_update_item"):
            if not hasattr(resources, attr):
                return None
        return resources
    except Exception:
        return None


def _sha256_sync(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 256), b""):
            h.update(chunk)
    return h.hexdigest()


async def _sha256(hass: HomeAssistant, path: Path) -> str:
    return await hass.async_add_executor_job(_sha256_sync, path)


async def ensure_frontend(hass: HomeAssistant) -> None:
    """Best-effort: copy the card JS to /config/www and register it as a resource."""
    try:
        await _ensure_js_in_www(hass)
    except Exception:
        _LOGGER.debug("ensure_frontend: failed copying JS to /config/www", exc_info=True)

    try:
        await _ensure_lovelace_resource_retry(hass, attempts_left=6)
    except Exception:
        _LOGGER.debug("ensure_frontend: failed registering Lovelace resource", exc_info=True)


async def _ensure_lovelace_resource_retry(hass: HomeAssistant, attempts_left: int) -> None:
    """Retry resource registration if Lovelace isn't fully ready yet."""
    if attempts_left <= 0:
        return
    resources = _get_lovelace_resources(hass)
    if resources is None:
        async_call_later(
            hass,
            5,
            lambda _now: hass.async_create_task(
                _ensure_lovelace_resource_retry(hass, attempts_left - 1)
            ),
        )
        return
    await _ensure_lovelace_resource(hass)


async def _ensure_js_in_www(hass: HomeAssistant) -> None:
    src = Path(__file__).parent / "www" / JS_FILENAME
    dst = Path(hass.config.path("www", JS_FILENAME))
    if not src.exists():
        _LOGGER.debug("ensure_frontend: bundled JS not found at %s", src)
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        try:
            if await _sha256(hass, src) == await _sha256(hass, dst):
                return
        except Exception:
            pass
    await hass.async_add_executor_job(shutil.copyfile, src, dst)


async def _ensure_lovelace_resource(hass: HomeAssistant) -> None:
    """Add/update /local/... as a Lovelace resource (storage mode) with cache-busting."""
    resources = _get_lovelace_resources(hass)
    if resources is None:
        return

    if not getattr(resources, "loaded", True):
        await resources.async_load()

    deployed = Path(hass.config.path("www", JS_FILENAME))
    token = "0"
    if deployed.exists():
        try:
            token = _token_from_hash(await _sha256(hass, deployed))
        except Exception:
            token = "0"
    url = f"{RESOURCE_URL}?v={token}"

    matches = []
    for entry in resources.async_items():
        try:
            if _strip_query(entry.get("url", "")) == RESOURCE_URL:
                matches.append(entry)
        except Exception:
            continue

    if matches:
        entry = matches[0]
        entry_url = str(entry.get("url", ""))
        if entry_url != url or entry.get("res_type") != RESOURCE_TYPE:
            await resources.async_update_item(
                entry["id"],
                {"res_type": RESOURCE_TYPE, "url": url},
            )
            _LOGGER.info("Updated Lovelace resource: %s", url)
        for dup in matches[1:]:
            try:
                await resources.async_delete_item(dup["id"])
            except Exception:
                pass
        return

    await resources.async_create_item({"res_type": RESOURCE_TYPE, "url": url})
    _LOGGER.info("Added Lovelace resource: %s", url)
