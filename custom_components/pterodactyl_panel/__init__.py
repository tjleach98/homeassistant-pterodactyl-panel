"""Custom integration to integrate the Pterodactyl Panel with Home Assistant."""

from __future__ import annotations

import logging
from typing import Final

from pydactyl import PterodactylClient
from pydactyl.exceptions import ClientConfigError
from pydactyl.responses import PaginatedResponse
from requests.exceptions import HTTPError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, CONF_HOST, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady

from .const import DOMAIN, PTERODACTYL_ATTRIBUTES
from .coordinator import PterodactylServerCoordinator

_LOGGER: logging.Logger = logging.getLogger(__package__)

PLATFORMS: Final[list[str]] = [Platform.BINARY_SENSOR, Platform.BUTTON, Platform.SENSOR, Platform.SWITCH]

STARTUP_MESSAGE: Final = f"Starting setup for {DOMAIN}"


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Pterodactyl Panel from a config entry."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    url = config_entry.data.get(CONF_HOST)
    api_key = config_entry.data.get(CONF_API_KEY)

    try:
        pterodactyl_api = PterodactylClient(url, api_key)
        await hass.async_add_executor_job(pterodactyl_api.client.account.get_account)
    except ClientConfigError as exception:
        raise ConfigEntryAuthFailed from exception
    except HTTPError as exception:
        if exception.response.status_code == 401:
                raise ConfigEntryAuthFailed from exception

        raise ConfigEntryNotReady from exception

    coordinators: list[PterodactylServerCoordinator] = []

    server_list_pages: PaginatedResponse = await hass.async_add_executor_job(
        pterodactyl_api.client.servers.list_servers
    )
    server_list_data = server_list_pages.data

    # Get all servers if more than one page.
    if server_list_pages.meta['pagination']['total_pages'] > 1:
        server_list_data = await hass.async_add_executor_job(server_list_pages.collect)

    servers = [server_data[PTERODACTYL_ATTRIBUTES] for server_data in server_list_data]

    for server in servers:
        coordinator_server = PterodactylServerCoordinator(
            hass=hass, entry=config_entry, client=pterodactyl_api, server=server
        )
        await coordinator_server.async_refresh()
        coordinators.append(coordinator_server)

    config_entry.runtime_data = coordinators

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
