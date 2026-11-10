"""Sensor exposing the latest PixelIt frame."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import PixelItConfigEntry
from .const import SENSOR_NAME
from .coordinator import PixelItLiveviewCoordinator


async def async_setup_entry(
    hass: HomeAssistant, entry: PixelItConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Add one sensor per configured display."""
    async_add_entities([PixelItLiveviewSensor(entry.entry_id, entry.runtime_data)])


class PixelItLiveviewSensor(SensorEntity):
    """Expose live pixels and connection status."""

    _attr_name = SENSOR_NAME
    _attr_icon = "mdi:led-strip-variant"
    _attr_should_poll = False
    _unrecorded_attributes = frozenset({"hex", "pixels"})

    def __init__(self, entry_id: str, coordinator: PixelItLiveviewCoordinator) -> None:
        """Initialize the sensor with a stable registry ID."""
        self._attr_unique_id = entry_id
        self._coordinator = coordinator

    async def async_added_to_hass(self) -> None:
        """Subscribe to WebSocket updates while the entity is loaded."""
        self._coordinator.on_update = self.async_write_ha_state
        self.async_on_remove(self._coordinator.clear_listener)

    @property
    def native_value(self) -> str:
        """Return the connection status used by existing cards."""
        return "connected" if self._coordinator.connected else "disconnected"

    @property
    def extra_state_attributes(self) -> dict:
        """Return the live frame and its dimensions."""
        return self._coordinator.attributes
