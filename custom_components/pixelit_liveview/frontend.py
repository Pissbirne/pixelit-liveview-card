"""Serve the bundled card and register its dashboard resource."""
from __future__ import annotations

import asyncio
import hashlib
import logging
from pathlib import Path

from homeassistant.components.http import StaticPathConfig
from homeassistant.components.lovelace import LOVELACE_DATA
from homeassistant.components.lovelace.resources import ResourceStorageCollection
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
JS_FILENAME = "pixelit-liveview-card.js"
RESOURCE_URL = f"/{DOMAIN}/{JS_FILENAME}"
LEGACY_URL = f"/local/{JS_FILENAME}"


async def ensure_frontend(hass: HomeAssistant) -> None:
    """Set up the shared resource once for all PixelIt entries."""
    frontend = hass.data.setdefault(DOMAIN, {})
    async with frontend.setdefault("frontend_lock", asyncio.Lock()):
        try:
            if "resource_url" not in frontend:
                source = Path(__file__).parent / "www" / JS_FILENAME
                content = await hass.async_add_executor_job(source.read_bytes)
                token = hashlib.sha256(content).hexdigest()[:12]
                await hass.http.async_register_static_paths(
                    [StaticPathConfig(RESOURCE_URL, str(source), False)]
                )
                frontend["resource_url"] = f"{RESOURCE_URL}?v={token}"

            lovelace = hass.data.get(LOVELACE_DATA)
            resources = lovelace.resources if lovelace is not None else None
            if isinstance(resources, ResourceStorageCollection):
                await _register_resource(resources, frontend["resource_url"])
        except Exception:
            _LOGGER.warning("Could not register the PixelIt dashboard card", exc_info=True)


async def _register_resource(resources: ResourceStorageCollection, url: str) -> None:
    """Migrate the previous resource in place and avoid duplicates."""
    await resources.async_get_info()
    matches = [
        item
        for item in resources.async_items()
        if item["url"].split("?", 1)[0] in (RESOURCE_URL, LEGACY_URL)
    ]
    if not matches:
        await resources.async_create_item({"res_type": "module", "url": url})
        return

    resource = matches[0]
    if resource["url"] != url or resource["type"] != "module":
        await resources.async_update_item(
            resource["id"], {"res_type": "module", "url": url}
        )
    for duplicate in matches[1:]:
        await resources.async_delete_item(duplicate["id"])
