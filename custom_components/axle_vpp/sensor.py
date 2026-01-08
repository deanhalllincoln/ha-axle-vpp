from __future__ import annotations

from datetime import datetime
import homeassistant.util.dt as dt_util

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN


# Raw API sensors
SENSORS = {
    "start_time": "Axle Start Time",
    "end_time": "Axle End Time",
    "import_export": "Axle Import / Export",
    "updated_at": "Axle Updated At",
}

# Human-friendly datetime sensors
FRIENDLY_SENSORS = {
    "start_time_friendly": "Axle Start Time (Friendly)",
    "end_time_friendly": "Axle End Time (Friendly)",
    "updated_at_friendly": "Axle Updated At (Friendly)",
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SensorEntity] = []

    # Raw sensors
    for key, name in SENSORS.items():
        entities.append(AxleSensor(coordinator, key, name))

    # Friendly datetime sensors
    for key, name in FRIENDLY_SENSORS.items():
        entities.append(AxleFriendlySensor(coordinator, key, name))

    async_add_entities(entities)


class AxleSensor(SensorEntity):
    """Raw Axle API sensor."""

    def __init__(self, coordinator, key: str, name: str) -> None:
        self.coordinator = coordinator
        self._key = key
        self._attr_name = name

    @property
    def unique_id(self) -> str:
        return f"axle_vpp_{self._key}"

    @property
    def native_value(self):
        data = self.coordinator.data or {}
        return data.get(self._key)

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

    async def async_update(self) -> None:
        await self.coordinator.async_request_refresh()

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )


class AxleFriendlySensor(SensorEntity):
    """Human-friendly timestamp sensor derived from API data."""

    _attr_device_class = SensorDeviceClass.TIMESTAMP

    def __init__(self, coordinator, key: str, name: str) -> None:
        self.coordinator = coordinator
        self._key = key
        self._attr_name = name

    @property
    def unique_id(self) -> str:
        # IMPORTANT: different from raw sensor IDs
        return f"axle_vpp_{self._key}"

    @property
    def native_value(self):
        data = self.coordinator.data or {}

        mapping = {
            "start_time_friendly": "start_time",
            "end_time_friendly": "end_time",
            "updated_at_friendly": "updated_at",
        }

        source_key = mapping.get(self._key)
        raw_value = data.get(source_key)

        if not raw_value:
            return None

        try:
            # API returns ISO8601 UTC, usually with Z
            utc_dt = datetime.fromisoformat(
                raw_value.replace("Z", "+00:00")
            )
            local_dt = dt_util.as_local(utc_dt)
            return local_dt
        except Exception:
            return None

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

    async def async_update(self) -> None:
        await self.coordinator.async_request_refresh()

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )


