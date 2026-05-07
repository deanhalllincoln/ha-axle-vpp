from __future__ import annotations

from datetime import datetime, timedelta

import homeassistant.util.dt as dt_util
from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

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


class AxleNextEventCalendar(CoordinatorEntity, CalendarEntity):
    _attr_name = "Axle Next Event"
    _attr_unique_id = "axle_vpp_next_event"
    _attr_device_info = DEVICE_INFO

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)

    @property
    def event(self) -> CalendarEvent | None:
        return self._build_event()

    async def async_get_events(
        self,
        hass: HomeAssistant,
        start_date: datetime,
        end_date: datetime,
    ) -> list[CalendarEvent]:
        event = self._build_event()
        if event is None:
            return []
        if event.end < start_date or event.start > end_date:
            return []
        return [event]

    def _build_event(self) -> CalendarEvent | None:
        data = self.coordinator.data or {}
        start_raw = data.get("start_time")
        end_raw = data.get("end_time")
        if not start_raw or not end_raw:
            return None

        try:
            start = datetime.fromisoformat(start_raw.replace("Z", "+00:00"))
            end = datetime.fromisoformat(end_raw.replace("Z", "+00:00"))
        except ValueError:
            return None

        if end <= dt_util.utcnow() - timedelta(minutes=1):
            return None

        import_export = data.get("import_export")
        description = (
            f"import_export: {import_export}" if import_export is not None else None
        )

        return CalendarEvent(
            start=start,
            end=end,
            summary="Axle VPP dispatch",
            description=description,
        )
