"""Base entity for the Pterodactyl Panel integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    PROPER_NAME,
    PTERODACTYL_DOCKER_IMAGE,
    PTERODACTYL_ID,
    PTERODACTYL_NAME,
)
from .coordinator import PterodactylServerCoordinator


class PterodactylEntityDescription(EntityDescription):
    """Describe a Pterodactyl Panel entity."""


class PterodactylEntity(CoordinatorEntity):
    """Base Pterodactyl Panel entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: PterodactylServerCoordinator,
        entry: ConfigEntry,
        description: PterodactylEntityDescription,
    ) -> None:
        """Initialize the Pterodactyl Panel sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = (
            f"{entry.entry_id}_{coordinator.server[PTERODACTYL_ID]}_{description.key}"
        )
        self._attr_device_info = DeviceInfo(
            entry_type=dr.DeviceEntryType.SERVICE,
            configuration_url=coordinator.url,
            identifiers={
                (
                    DOMAIN,
                    f"{entry.entry_id}_server_{coordinator.server[PTERODACTYL_ID]}",
                )
            },
            name=f"Server {coordinator.server[PTERODACTYL_NAME]}",
            manufacturer=PROPER_NAME,
            sw_version=coordinator.server[PTERODACTYL_DOCKER_IMAGE],
        )
        self.entity_description = description
