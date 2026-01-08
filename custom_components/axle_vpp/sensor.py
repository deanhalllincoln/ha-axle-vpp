from __future__ import annotations
from datetime import datetime
import homeassistant.util.dt as dt_util
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

SENSORS = {
    "start_time": "Axle Start Time",
    "end_time": "Axle End Time",
    "import_export": "Axle Import-Export",
    "updated_at": "Axle Updated At"
}

FRIENDLY_SENSORS = {
    "start_time_friendly": "Axle Start Time (Friendly)",
    "end_time_friendly": "Axle End Time (Friendly)",
    "updated_at_friendly": "Axle Updated At (Friendly)"
}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [AxleSensor(coordinator, key, name) for key, name in SENSORS.items()]
    # Add friendly datetime sensors
    entities += [AxleFriendlySensor(coordinator, key, name) for key, name in FRIENDLY_SENSORS.items()]

    async_add_entities(entities)

class AxleSensor(SensorEntity):
    def __init__(self, coordinator, key, name):
        self.coordinator = coordinator
        self._attr_name = name
        self._key = key

    @property
    def unique_id(self):
        return f"axle_vpp_{self._key}"

    @property
    def native_value(self):
        data = self.coordinator.data or {}
        return data.get(self._key)

    @property
    def should_poll(self):
        return False

    @property
    def available(self):
        return self.coordinator.last_update_success

    async def async_update(self):
        await self.coordinator.async_request_refresh()

    async def async_added_to_hass(self):
        self.async_on_remove(self.coordinator.async_add_listener(self.async_write_ha_state))


class AxleFriendlySensor(SensorEntity):
    """Sensor for human-friendly datetime."""

    def __init__(self, coordinator, key, name):
        self.coordinator = coordinator
        self._attr_name = name
        self._key = key
        self._attr_device_class = "timestamp"  # Home Assistant will format automatically

    @property
    def unique_id(self):
        return f"axle_vpp_{self._key}"

    @property
    def native_value(self):
        data = self.coordinator.data or {}

        # Map friendly keys to the actual API fields
        mapping = {
            "start_time_friendly": "start_time",
            "end_time_friendly": "end_time",
            "updated_at_friendly": "updated_at"
        }

        raw_value = data.get(mapping.get(self._key))
        if not raw_value:
            return None

        try:
            # Parse UTC datetime from API
            dt = datetime.fromisoformat(raw_value.replace("Z", "+00:00"))

            # Convert to Home Assistant local time (UK)
            dt_local = dt_util.as_local(dt)
            return dt_local.isoformat()  # HA timestamp sensor expects ISO format
        except Exception:
            return None

    @property
    def should_poll(self):
        return False

    @property
    def available(self):
        return self.coordinator.last_update_success

    async def async_update(self):
        await self.coordinator.async_request_refresh()

    async def async_added_to_hass(self):
        self.async_on_remove(self.coordinator.async_add_listener(self.async_write_ha_state))

