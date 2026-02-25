from __future__ import annotations

from datetime import datetime, timedelta
import homeassistant.util.dt as dt_util

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.event import async_track_time_interval

from .const import DOMAIN

DEVICE_INFO = DeviceInfo(
    identifiers={(DOMAIN, "axle_vpp")},
    name="Axle VPP",
    manufacturer="Axle Energy",
    model="Virtual Power Plant",
)

# Core API sensors
SENSORS = {
    "start_time": "Axle Start Time",
    "end_time": "Axle End Time",
    "import_export": "Axle Import / Export",
    "updated_at": "Axle Updated At",
}

# Friendly timestamp sensors
FRIENDLY_SENSORS = {
    "start_time_friendly": "Axle Start Time (Friendly)",
    "end_time_friendly": "Axle End Time (Friendly)",
    "updated_at_friendly": "Axle Updated At (Friendly)",
}

# Calculated numeric/state sensors
EXTRA_SENSORS = {
    "event_minutes_to_start": "Axle Event Minutes To Start",
    "event_remaining_minutes": "Axle Event Remaining Minutes",
    "event_window_state": "Axle Event Window State",
}

# Time-based binary sensors
TIME_BASED_BINARY_SENSORS = {
    "event_in_progress": "Axle Event In Progress",
    "event_1_hour_before": "Axle Event 1 Hour Before",
    "event_2_hours_before": "Axle Event 2 Hours Before",
}

# Date-based binary sensors (your requested additions)
DATE_BASED_BINARY_SENSORS = {
    "event_tomorrow": "Axle Event Tomorrow",
    "event_later_today": "Axle Event Later Today",
    "event_completed_today": "Axle Event Completed Today",
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []

    # Standard sensors
    for key, name in SENSORS.items():
        entities.append(AxleSensor(coordinator, key, name))

    # Friendly timestamp sensors
    for key, name in FRIENDLY_SENSORS.items():
        entities.append(AxleFriendlySensor(coordinator, key, name))

    # Calculated sensors
    for key, name in EXTRA_SENSORS.items():
        entities.append(AxleEventSensor(coordinator, key, name))

    # Time-based binary sensors
    for key, name in TIME_BASED_BINARY_SENSORS.items():
        entities.append(AxleEventBinarySensor(coordinator, key, name))

    # Date-based binary sensors
    for key, name in DATE_BASED_BINARY_SENSORS.items():
        entities.append(AxleEventBinarySensor(coordinator, key, name))

    async_add_entities(entities)


# ------------------------------------------------------------------
# Base class
# ------------------------------------------------------------------

class AxleBase:
    def __init__(self, coordinator, key: str, name: str):
        self.coordinator = coordinator
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"axle_vpp_{key}"
        self._attr_device_info = DEVICE_INFO

    @property
    def available(self):
        return self.coordinator.last_update_success

    async def async_added_to_hass(self):
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )


# ------------------------------------------------------------------
# Direct API sensor
# ------------------------------------------------------------------

class AxleSensor(AxleBase, SensorEntity):
    @property
    def native_value(self):
        return (self.coordinator.data or {}).get(self._key)


# ------------------------------------------------------------------
# Friendly timestamp sensor
# ------------------------------------------------------------------

class AxleFriendlySensor(AxleBase, SensorEntity):
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    @property
    def native_value(self):
        mapping = {
            "start_time_friendly": "start_time",
            "end_time_friendly": "end_time",
            "updated_at_friendly": "updated_at",
        }

        raw = (self.coordinator.data or {}).get(mapping[self._key])
        if not raw:
            return None

        try:
            utc_dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
            return dt_util.as_local(utc_dt)
        except Exception:
            return None


# ------------------------------------------------------------------
# Calculated numeric/state sensors
# ------------------------------------------------------------------

class AxleEventSensor(AxleBase, SensorEntity):

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self.async_on_remove(
            async_track_time_interval(
                self.hass,
                self._handle_tick,
                timedelta(minutes=1),
            )
        )

    async def _handle_tick(self, now):
        self.async_write_ha_state()

    @property
    def native_value(self):
        data = self.coordinator.data or {}
        now = dt_util.utcnow()

        start_raw = data.get("start_time")
        end_raw = data.get("end_time")

        if not start_raw or not end_raw:
            return None

        try:
            start = datetime.fromisoformat(start_raw.replace("Z", "+00:00"))
            end = datetime.fromisoformat(end_raw.replace("Z", "+00:00"))
        except Exception:
            return None

        if self._key == "event_minutes_to_start":
            delta = (start - now).total_seconds() / 60
            return int(delta) if delta > 0 else 0

        if self._key == "event_remaining_minutes":
            delta = (end - now).total_seconds() / 60
            return int(delta) if delta > 0 else 0

        if self._key == "event_window_state":
            if start <= now <= end:
                return "in_progress"
            if now < start:
                return "upcoming"
            return "finished"

        return None


# ------------------------------------------------------------------
# Binary sensors (time & date based)
# ------------------------------------------------------------------

class AxleEventBinarySensor(AxleBase, BinarySensorEntity):

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self.async_on_remove(
            async_track_time_interval(
                self.hass,
                self._handle_tick,
                timedelta(minutes=1),
            )
        )

    async def _handle_tick(self, now):
        self.async_write_ha_state()

    @property
    def is_on(self):
        data = self.coordinator.data or {}
        now = dt_util.utcnow()

        start_raw = data.get("start_time")
        end_raw = data.get("end_time")

        if not start_raw or not end_raw:
            return False

        try:
            start = datetime.fromisoformat(start_raw.replace("Z", "+00:00"))
            end = datetime.fromisoformat(end_raw.replace("Z", "+00:00"))
        except Exception:
            return False

        local_now = dt_util.as_local(now)
        start_local = dt_util.as_local(start)
        end_local = dt_util.as_local(end)

        today = local_now.date()

        # Time-based
        if self._key == "event_in_progress":
            return start <= now <= end

        if self._key == "event_1_hour_before":
            delta = (start - now).total_seconds()
            return 0 <= delta <= 3600

        if self._key == "event_2_hours_before":
            delta = (start - now).total_seconds()
            return 3600 < delta <= 7200

        # Date-based (your requested sensors)

        if self._key == "event_tomorrow":
            return start_local.date() == (today + timedelta(days=1))

        if self._key == "event_later_today":
            return start_local.date() == today and now < start

        if self._key == "event_completed_today":
            return end_local.date() == today and now > end

        return False
