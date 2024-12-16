"""Switch for the Pterodactyl Panel."""

from dataclasses import dataclass

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import PterodactylEntity, PterodactylEntityDescription


@dataclass(frozen=True, kw_only=True)
class PterodactylSwitchEntityDescription(
    PterodactylEntityDescription, SwitchEntityDescription
):
    """Describes Pterodactyl Panel switch entity."""


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Pterodactyl Panel switches."""
    for coordinator in config_entry.runtime_data:
        async_add_entities(
            [
                PterodactylPowerSwitchEntity(
                    coordinator,
                    config_entry,
                    PterodactylSwitchEntityDescription(
                        key="power_switch",
                        translation_key="pterodactyl_server_power_switch",
                        icon="mdi:power",
                    )
                ),
            ]
        )


class PterodactylPowerSwitchEntity(PterodactylEntity, SwitchEntity):
    """Represents a Pterodactyl Panel switch."""

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return self.coordinator.data.get('is_running')

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        await self.coordinator.send_power_action('start')

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        await self.coordinator.send_power_action('stop')
