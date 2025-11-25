"""Config flow for HasWave Deprem integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, DEFAULT_API_URL, DEFAULT_UPDATE_INTERVAL, DEFAULT_MIN_MAGNITUDE
from .api import HasWaveDepremAPI

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Optional("api_url", default=DEFAULT_API_URL): str,
        vol.Optional("update_interval", default=DEFAULT_UPDATE_INTERVAL): int,
        vol.Optional("min_magnitude", default=DEFAULT_MIN_MAGNITUDE): float,
        vol.Optional("city", default=""): str,
        vol.Optional("region", default=""): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    api = HasWaveDepremAPI(
        api_url=data.get("api_url", DEFAULT_API_URL),
        min_magnitude=data.get("min_magnitude", DEFAULT_MIN_MAGNITUDE),
        city=data.get("city", ""),
        region=data.get("region", ""),
    )
    
    result = await hass.async_add_executor_job(api.fetch_earthquakes)
    
    if result is None:
        raise CannotConnect
    
    return {"title": "HasWave Deprem"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HasWave Deprem."""
    
    VERSION = 1
    
    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )
        
        errors = {}
        
        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except Exception:
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=info["title"], data=user_input)
        
        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""

