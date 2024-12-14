"""Binary Sensor for the Pterodactyl Panel."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Final

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import PterodactylEntity, PterodactylEntityDescription


@dataclass(frozen=True, kw_only=True)
class PterodactylBinarySensorEntityDescription(
    PterodactylEntityDescription, BinarySensorEntityDescription
):
    """Class describing Pterodactyl Panel Binary Sensors."""

    value_fn: Callable[[str | int | float], str | int | float] = lambda value: value


BINARY_SENSORS: Final[list[PterodactylBinarySensorEntityDescription]] = [
    PterodactylBinarySensorEntityDescription(
        key="is_node_under_maintenance",
        translation_key="pterodactyl_is_node_under_maintenance",
    ),
    PterodactylBinarySensorEntityDescription(
        key="is_running",
        device_class=BinarySensorDeviceClass.RUNNING,
        translation_key="pterodactyl_is_running",
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Pterodactyl Panel binary sensors."""
    for coordinator in config_entry.runtime_data:
        async_add_entities(
            [
                PterodactylBinarySensorEntity(coordinator, config_entry, sensor)
                for sensor in BINARY_SENSORS
                if sensor.key in coordinator.data
            ]
        )


class PterodactylBinarySensorEntity(PterodactylEntity, BinarySensorEntity):
    """Represents a Pterodactyl Panel binary sensor."""

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        val = self.coordinator.data.get(self.entity_description.key)
        return self.entity_description.value_fn(val)
