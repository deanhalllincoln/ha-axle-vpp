from __future__ import annotations
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN

SENSORS = {
    "start_time": "Axle Start Time",
    "end_time": "Axle End Time",
    "import_export": "Axle Import-Export",
    "updated_at": "Axle Updated At"
}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = [AxleSensor(coordinator, key, name) for key, name in SENSORS.items()]
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
