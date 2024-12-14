"""Button for the Pterodactyl Panel."""

from dataclasses import dataclass
import logging
from typing import Final

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import PterodactylEntity, PterodactylEntityDescription

_LOGGER = logging.getLogger(__name__)


@dataclass
class PterodactylButtonEntityDescription(
    PterodactylEntityDescription, ButtonEntityDescription
):
    """Describes Pterodactyl Panel button entity."""


BUTTONS: Final[list[PterodactylButtonEntityDescription]] = [
    PterodactylButtonEntityDescription(
        key="server_restart",
        translation_key="pterodactyl_server_restart",
    ),
    PterodactylButtonEntityDescription(
        key="server_start",
        translation_key="pterodactyl_server_start",
    ),
    PterodactylButtonEntityDescription(
        key="server_stop",
        translation_key="pterodactyl_server_stop",
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Pterodactyl Panel buttons."""
    for coordinator in config_entry.runtime_data:
        async_add_entities(
            [
                PterodactylButtonEntity(coordinator, config_entry, button)
                for button in BUTTONS
            ]
        )


class PterodactylButtonEntity(PterodactylEntity, ButtonEntity):
    """Represents a Pterodactyl Panel button."""

    async def async_press(self) -> None:
        """Handle the button press."""
        power_action = ""
        match self.entity_description.key:
            case "server_start":
                power_action = "start"
            case "server_stop":
                power_action = "stop"
            case "server_restart":
                power_action = "restart"
            case _:
                raise ServiceValidationError("Button must be start, stop, or restart")

        await self.coordinator.send_power_action(power_action)
