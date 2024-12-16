"""Sensor for the Pterodactyl Panel."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Final

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfInformation, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import PterodactylEntity, PterodactylEntityDescription


@dataclass(frozen=True, kw_only=True)
class PterodactylSensorEntityDescription(
    PterodactylEntityDescription, SensorEntityDescription
):
    """Describes Pterodactyl sensor entity."""

    conversion_fn: Callable | None = None
    value_fn: Callable[[str | int | float], str | int | float] = lambda value: value


SENSORS: Final[list[PterodactylSensorEntityDescription]] = [
    PterodactylSensorEntityDescription(
        key="cpu",
        translation_key="pterodactyl_cpu",
        icon="mdi:cpu-64-bit",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        conversion_fn=lambda x: (x * 100) if x >= 0 else 0,
        suggested_display_precision=0,
    ),
    PterodactylSensorEntityDescription(
        key="current_state",
        translation_key="pterodactyl_current_state",
    ),
    PterodactylSensorEntityDescription(
        key="disk",
        icon="mdi:harddisk",
        translation_key="pterodactyl_disk",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.DATA_SIZE,
        native_unit_of_measurement=UnitOfInformation.BYTES,
        suggested_unit_of_measurement=UnitOfInformation.GIGABYTES,
        suggested_display_precision=2,
    ),
    PterodactylSensorEntityDescription(
        key="memory",
        icon="mdi:memory",
        translation_key="pterodactyl_memory",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.DATA_SIZE,
        native_unit_of_measurement=UnitOfInformation.BYTES,
        suggested_display_precision=2,
        suggested_unit_of_measurement=UnitOfInformation.GIGABYTES,
    ),
    PterodactylSensorEntityDescription(
        key="network_rx",
        icon="mdi:download-network-outline",
        translation_key="pterodactyl_network_rx",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.DATA_SIZE,
        native_unit_of_measurement=UnitOfInformation.BYTES,
        suggested_unit_of_measurement=UnitOfInformation.GIGABYTES,
        suggested_display_precision=2,
    ),
    PterodactylSensorEntityDescription(
        key="network_tx",
        icon="mdi:upload-network-outline",
        translation_key="pterodactyl_network_tx",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.DATA_SIZE,
        native_unit_of_measurement=UnitOfInformation.BYTES,
        suggested_unit_of_measurement=UnitOfInformation.GIGABYTES,
        suggested_display_precision=2,
    ),
    PterodactylSensorEntityDescription(
        key="node",
        translation_key="pterodactyl_node",
    ),
    PterodactylSensorEntityDescription(
        key="uptime",
        icon="mdi:memory",
        translation_key="pterodactyl_uptime",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.MILLISECONDS,
        suggested_unit_of_measurement=UnitOfTime.HOURS,
        entity_registry_enabled_default=False,
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Pterodactyl sensors."""
    for coordinator in config_entry.runtime_data:
        async_add_entities(
            [
                PterodactylSensorEntity(coordinator, config_entry, sensor)
                for sensor in SENSORS
                if sensor.key in coordinator.data
            ]
        )


class PterodactylSensorEntity(PterodactylEntity, SensorEntity):
    """Represents a Pterodactyl sensor."""

    @property
    def native_value(self) -> str | int | float:
        """Return the state for this sensor."""
        val = self.coordinator.data.get(self.entity_description.key)
        return self.entity_description.value_fn(val)
