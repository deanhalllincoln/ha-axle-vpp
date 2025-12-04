from __future__ import annotations
import aiohttp
import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant

from .const import DOMAIN, API_URL, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

class AxleCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, token: str):
        self.hass = hass
        self.token = token

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(API_URL, headers=headers) as resp:
                    if resp.status != 200:
                        raise UpdateFailed(f"HTTP {resp.status}")
                    return await resp.json()
        except Exception as err:
            raise UpdateFailed(f"Failed to fetch Axle VPP data: {err}") from err
