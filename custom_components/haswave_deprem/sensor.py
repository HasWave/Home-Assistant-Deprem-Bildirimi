"""Sensor platform for HasWave Deprem."""
from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

from .const import DOMAIN

SENSOR_DESCRIPTIONS: dict[str, SensorEntityDescription] = {
    "latest": SensorEntityDescription(
        key="latest",
        name="Son Deprem",
        icon="mdi:earthquake",
    ),
    "magnitude": SensorEntityDescription(
        key="magnitude",
        name="Büyüklük",
        icon="mdi:gauge",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "max_magnitude": SensorEntityDescription(
        key="max_magnitude",
        name="Maksimum Büyüklük",
        icon="mdi:gauge",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "avg_magnitude": SensorEntityDescription(
        key="avg_magnitude",
        name="Ortalama Büyüklük",
        icon="mdi:gauge",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "count": SensorEntityDescription(
        key="count",
        name="Deprem Sayısı",
        icon="mdi:counter",
        state_class=SensorStateClass.MEASUREMENT,
    ),
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    
    entities = []
    for key, description in SENSOR_DESCRIPTIONS.items():
        entities.append(HasWaveDepremSensor(coordinator, description, key))
    
    async_add_entities(entities)


class HasWaveDepremSensor(CoordinatorEntity, SensorEntity):
    """Representation of a HasWave Deprem sensor."""
    
    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        description: SensorEntityDescription,
        sensor_key: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._sensor_key = sensor_key
        self._attr_unique_id = f"{DOMAIN}_{sensor_key}"
        self._attr_name = f"Deprem - {description.name}"
    
    @property
    def native_value(self) -> str | float | int | None:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        
        earthquakes = self.coordinator.data
        
        if self._sensor_key == "latest":
            if earthquakes:
                latest = earthquakes[0]
                return f"{latest.get('magnitude', 'N/A')} - {latest.get('location', 'N/A')}"
            return "Yok"
        
        elif self._sensor_key == "magnitude":
            if earthquakes:
                return float(earthquakes[0].get("magnitude", 0))
            return 0.0
        
        elif self._sensor_key == "max_magnitude":
            if earthquakes:
                magnitudes = [float(eq.get("magnitude", 0)) for eq in earthquakes]
                return max(magnitudes) if magnitudes else 0.0
            return 0.0
        
        elif self._sensor_key == "avg_magnitude":
            if earthquakes:
                magnitudes = [float(eq.get("magnitude", 0)) for eq in earthquakes]
                return sum(magnitudes) / len(magnitudes) if magnitudes else 0.0
            return 0.0
        
        elif self._sensor_key == "count":
            return len(earthquakes)
        
        return None
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        if not self.coordinator.data:
            return {}
        
        earthquakes = self.coordinator.data
        
        if self._sensor_key == "latest" and earthquakes:
            latest = earthquakes[0]
            return {
                "magnitude": latest.get("magnitude"),
                "location": latest.get("location"),
                "depth": latest.get("depth"),
                "time": latest.get("time"),
                "latitude": latest.get("latitude"),
                "longitude": latest.get("longitude"),
            }
        
        return {}

