"""Data update coordinator for the Pterodactyl Panel integration."""

from datetime import timedelta
import logging
from typing import Any, Final

from pydactyl import PterodactylClient
from requests.exceptions import HTTPError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import PTERODACTYL_ID

_LOGGER = logging.getLogger(__name__)

DEFAULT_SCAN_INTERVAL: Final = timedelta(seconds=60)
RUNNING_VALUE: Final[str] = "running"


class PterodactylServerCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Pterodactyl Panel data update coordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: PterodactylClient,
        server: str,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the Pterodactyl Panel coordinator."""
        self.pterodactyl_api = client
        self.url = entry.data[CONF_HOST]
        self.server = server

        super().__init__(
            hass,
            _LOGGER,
            name=self.url,
            update_interval=DEFAULT_SCAN_INTERVAL,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch all Pterodactyl data."""
        data = {}
        server_id = self.server[PTERODACTYL_ID]

        try:
            # Pull from utilization endpoint
            server_utilization = await self.hass.async_add_executor_job(
                self.pterodactyl_api.client.servers.get_server_utilization, server_id
            )
            # Pull from server info endpoint
            server_info = await self.hass.async_add_executor_job(
                self.pterodactyl_api.client.servers.get_server, server_id
            )

        except HTTPError as e:
            if e.response.status_code == 401:
                raise ConfigEntryAuthFailed from e

            raise UpdateFailed(f"Failed to get data from {server_id}") from e

        # Add server utilization data.
        data["is_running"] = server_utilization["current_state"] == RUNNING_VALUE
        data["current_state"] = server_utilization["current_state"]
        data["memory"] = server_utilization["resources"]["memory_bytes"]
        data["cpu"] = server_utilization["resources"]["cpu_absolute"]
        data["disk"] = server_utilization["resources"]["disk_bytes"]
        data["network_tx"] = server_utilization["resources"]["network_tx_bytes"]
        data["network_rx"] = server_utilization["resources"]["network_rx_bytes"]
        data["uptime"] = server_utilization["resources"]["uptime"]

        # Add server info data.
        data["node"] = server_info["node"]
        data["is_node_under_maintenance"] = server_info["is_node_under_maintenance"]

        return data

    async def send_power_action(self, action: str):
        """Send power action to Pterodactyl Panel api."""
        await self.hass.async_add_executor_job(
            self.pterodactyl_api.client.servers.send_power_action,
            self.server[PTERODACTYL_ID],
            action,
        )
