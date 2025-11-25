"""API client for HasWave Deprem."""
from __future__ import annotations

import logging
from typing import Any
import requests

_LOGGER = logging.getLogger(__name__)


class HasWaveDepremAPI:
    """API client for HasWave Deprem."""
    
    def __init__(self, api_url: str, min_magnitude: float = 0.0, city: str = "", region: str = "") -> None:
        """Initialize the API client."""
        self.api_url = api_url
        self.min_magnitude = min_magnitude
        self.city = city
        self.region = region
    
    def fetch_earthquakes(self) -> list[dict[str, Any]] | None:
        """Fetch earthquakes from the API."""
        try:
            params = {
                "action": "latest",
                "limit": 50,
            }
            
            if self.min_magnitude > 0:
                params["min_magnitude"] = self.min_magnitude
            
            if self.city:
                params["city"] = self.city
            
            if self.region:
                params["region"] = self.region
            
            _LOGGER.debug(f"API isteği: {self.api_url} - Params: {params}")
            response = requests.get(self.api_url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                _LOGGER.debug(f"API yanıtı: {type(data)}, Keys: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
                
                if isinstance(data, dict):
                    if data.get("success"):
                        earthquakes = data.get("data", [])
                        if earthquakes:
                            _LOGGER.info(f"API'den {len(earthquakes)} deprem verisi alındı")
                        else:
                            _LOGGER.warning("API'den boş liste döndü (success=True ama data boş)")
                        return earthquakes
                    else:
                        _LOGGER.error(f"API hatası: {data.get('error', 'Bilinmeyen hata')}")
                        return None
                elif isinstance(data, list):
                    if data:
                        _LOGGER.info(f"API'den {len(data)} deprem verisi alındı (liste formatında)")
                    else:
                        _LOGGER.warning("API'den boş liste döndü")
                    return data
                else:
                    _LOGGER.error(f"Beklenmeyen API yanıt formatı: {type(data)}")
                    return None
            else:
                _LOGGER.error(f"HTTP hatası: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            _LOGGER.error(f"API bağlantı hatası: {e}", exc_info=True)
            return None
        
        return None

