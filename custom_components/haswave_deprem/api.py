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
            
            response = requests.get(self.api_url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and data.get("success"):
                    return data.get("data", [])
                elif isinstance(data, list):
                    return data
            else:
                _LOGGER.error(f"HTTP hatası: {response.status_code}")
                
        except Exception as e:
            _LOGGER.error(f"API bağlantı hatası: {e}")
        
        return []

