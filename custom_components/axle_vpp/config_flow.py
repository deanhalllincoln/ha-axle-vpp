from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_TOKEN
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

class AxleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(
                title="Axle VPP",
                data={CONF_TOKEN: user_input[CONF_TOKEN]},
            )

        schema = vol.Schema({
            vol.Required(CONF_TOKEN): str
        })

        return self.async_show_form(step_id="user", data_schema=schema)
