"""Config flow for HasWave Deprem integration."""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, DEFAULT_API_URL, DEFAULT_UPDATE_INTERVAL, DEFAULT_MIN_MAGNITUDE
from .api import HasWaveDepremAPI

_LOGGER = logging.getLogger(__name__)


def _load_strings() -> dict:
    """Load strings.json file."""
    strings_path = Path(__file__).parent / "strings.json"
    try:
        with open(strings_path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        _LOGGER.warning(f"Strings dosyası yüklenemedi: {e}")
        return {}


def _get_user_schema(strings: dict | None = None) -> vol.Schema:
    """Get user step schema with localized strings."""
    if strings is None:
        strings = _load_strings()
    
    return vol.Schema(
        {
            vol.Optional("api_url", default=DEFAULT_API_URL): str,
            vol.Optional("update_interval", default=DEFAULT_UPDATE_INTERVAL): int,
        }
    )


def _get_filters_schema(strings: dict | None = None) -> vol.Schema:
    """Get filters step schema with localized strings."""
    if strings is None:
        strings = _load_strings()
    
    return vol.Schema(
        {
            vol.Optional("all_earthquakes", default=True): bool,
            vol.Optional("min_magnitude", default=DEFAULT_MIN_MAGNITUDE): vol.Coerce(float),
            vol.Optional("city", default=""): str,
            vol.Optional("region", default=""): str,
        }
    )


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    # "Tüm depremler" seçeneği kontrolü
    all_earthquakes = data.get("all_earthquakes", True)
    
    # min_magnitude'u float'a çevir
    min_magnitude = data.get("min_magnitude", DEFAULT_MIN_MAGNITUDE)
    if isinstance(min_magnitude, str):
        try:
            min_magnitude = float(min_magnitude)
        except (ValueError, TypeError):
            min_magnitude = DEFAULT_MIN_MAGNITUDE
    elif not isinstance(min_magnitude, (int, float)):
        min_magnitude = DEFAULT_MIN_MAGNITUDE
    
    # Eğer "Tüm depremler" seçili değilse, city veya region kullan
    city = ""
    region = ""
    if not all_earthquakes:
        city = data.get("city", "")
        region = data.get("region", "")
    
    api = HasWaveDepremAPI(
        api_url=data.get("api_url", DEFAULT_API_URL),
        min_magnitude=float(min_magnitude),
        city=city,
        region=region,
    )
    
    result = await hass.async_add_executor_job(api.fetch_earthquakes)
    
    # None dönerse hata var demektir
    if result is None:
        raise CannotConnect
    
    # Boş liste de geçerli bir sonuçtur (deprem olmayabilir)
    if isinstance(result, list):
        if len(result) == 0:
            filter_info = f"Min Büyüklük={min_magnitude}"
            if not all_earthquakes:
                if city:
                    filter_info += f", İl={city}"
                if region:
                    filter_info += f", Bölge={region}"
            else:
                filter_info += ", Tüm Depremler"
            _LOGGER.info(f"API bağlantısı başarılı ama deprem verisi yok. Filtreler: {filter_info}")
        else:
            _LOGGER.info(f"API bağlantısı başarılı: {len(result)} deprem bulundu")
    
    return {"title": "HasWave Deprem"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HasWave Deprem."""
    
    VERSION = 1
    
    def __init__(self):
        """Initialize the config flow."""
        self._user_input = {}
    
    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step - basic settings."""
        strings = _load_strings()
        step_strings = strings.get("config", {}).get("step", {}).get("user", {})
        error_strings = strings.get("config", {}).get("error", {})
        
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=_get_user_schema(strings),
            )
        
        # Temel ayarları kaydet
        self._user_input.update(user_input)
        
        # Filtreler adımına geç
        return await self.async_step_filters()
    
    async def async_step_filters(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the filters step - advanced settings."""
        strings = _load_strings()
        step_strings = strings.get("config", {}).get("step", {}).get("filters", {})
        error_strings = strings.get("config", {}).get("error", {})
        
        if user_input is None:
            return self.async_show_form(
                step_id="filters",
                data_schema=_get_filters_schema(strings),
            )
        
        # Filtreleri ekle
        self._user_input.update(user_input)
        
        errors = {}
        
        try:
            info = await validate_input(self.hass, self._user_input)
        except CannotConnect:
            errors["base"] = error_strings.get("cannot_connect", "cannot_connect")
        except Exception:
            _LOGGER.exception("Unexpected exception")
            errors["base"] = error_strings.get("unknown", "unknown")
        else:
            return self.async_create_entry(title=info["title"], data=self._user_input)
        
        return self.async_show_form(
            step_id="filters",
            data_schema=_get_filters_schema(strings),
            errors=errors,
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""

