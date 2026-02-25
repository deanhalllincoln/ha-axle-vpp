from __future__ import annotations

from datetime import timedelta, datetime
import logging
import homeassistant.util.dt as dt_util

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

NORMAL_INTERVAL = timedelta(minutes=10)
FAST_INTERVAL = timedelta(minutes=1)


class AxleCoordinator(DataUpdateCoordinator):
    """Coordinator for fetching Axle events and adjusting polling interval."""

    def __init__(self, hass: HomeAssistant, api) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=NORMAL_INTERVAL,
        )
        self.api = api

    async def _async_update_data(self):
        """Fetch the latest event data from the Axle API."""
        try:
            data = await self.api.async_get_event()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with Axle API: {err}") from err

        # Adjust polling interval based on event timing
        self._adjust_polling_based_on_event(data)

        return data

    def _adjust_polling_based_on_event(self, data: dict | None) -> None:
        """Switch polling interval depending on event schedule."""
        if not data:
            self._set_interval(NORMAL_INTERVAL)
            return

        start_raw = data.get("start_time")
        end_raw = data.get("end_time")

        if not start_raw or not end_raw:
            self._set_interval(NORMAL_INTERVAL)
            return

        try:
            start = datetime.fromisoformat(start_raw.replace("Z", "+00:00"))
            end = datetime.fromisoformat(end_raw.replace("Z", "+00:00"))
        except Exception:
            self._set_interval(NORMAL_INTERVAL)
            return

        now = dt_util.utcnow()

        # Fast polling: 2 hours before event start and during event
        if start - timedelta(hours=2) <= now <= end:
            self._set_interval(FAST_INTERVAL)
        else:
            self._set_interval(NORMAL_INTERVAL)

    def _set_interval(self, interval: timedelta) -> None:
        """Update the coordinator interval and fetch immediately if needed."""
        if self.update_interval != interval:
            _LOGGER.debug("Switching polling interval to %s", interval)
            self.update_interval = interval
            # Schedule an immediate fetch to apply the new interval
            self.hass.async_create_task(self.async_refresh())
