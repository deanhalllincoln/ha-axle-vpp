from __future__ import annotations

from datetime import datetime

import homeassistant.util.dt as dt_util

from homeassistant.components.calendar import (
    CalendarEntity,
    CalendarEvent,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN


DEVICE_INFO = DeviceInfo(
    identifiers={(DOMAIN, "axle_vpp")},
    name="Axle VPP",
    manufacturer="Axle Energy",
    model="Virtual Power Plant",
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([AxleNextEventCalendar(coordinator)])


class AxleNextEventCalendar(CalendarEntity):

    _attr_name = "Axle Next Event"
    _attr_unique_id = "axle_next_event"
    _attr_device_info = DEVICE_INFO

    def __init__(self, coordinator):
        self.coordinator = coordinator

    @property
    def available(self):
        return self.coordinator.last_update_success

    async def async_added_to_hass(self):
        self.async_on_remove(
            self.coordinator.async_add_listener(
                self.async_write_ha_state
            )
        )

    @property
    def event(self):
        data = self.coordinator.data or {}

        start_raw = data.get("start_time")
        end_raw = data.get("end_time")

        if not start_raw or not end_raw:
            return None

        try:
            start = datetime.fromisoformat(
                start_raw.replace("Z", "+00:00")
            )

            end = datetime.fromisoformat(
                end_raw.replace("Z", "+00:00")
            )

        except Exception:
            return None

        import_export = data.get("import_export", "Dispatch")

        return CalendarEvent(
            summary=f"Axle {import_export} Event",
            start=dt_util.as_local(start),
            end=dt_util.as_local(end),
        )

    async def async_get_events(self, hass, start_date, end_date):
        data = self.coordinator.data or {}

        start_raw = data.get("start_time")
        end_raw = data.get("end_time")

        if not start_raw or not end_raw:
            return []

        try:
            start = datetime.fromisoformat(
                start_raw.replace("Z", "+00:00")
            )
            end = datetime.fromisoformat(
                end_raw.replace("Z", "+00:00")
            )
        except Exception:
            return []

        start = dt_util.as_utc(start)
        end = dt_util.as_utc(end)

        # Only return event if it overlaps requested range
        if end < start_date or start > end_date:
            return []

        return [
            CalendarEvent(
                summary=f"Axle {data.get('import_export', 'Dispatch')} Event",
                start=dt_util.as_local(start),
                end=dt_util.as_local(end),
            )
        ]

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data or {}

        return {
            "import_export": data.get("import_export"),
            "updated_at": data.get("updated_at"),
        }
