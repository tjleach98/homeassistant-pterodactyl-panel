"""Config flow for the Pterodactyl Panel integration."""

from __future__ import annotations

from collections.abc import Mapping
import logging
from typing import Any, Final

from pydactyl import PterodactylClient
from pydactyl.exceptions import ClientConfigError
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_API_KEY, CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import Unauthorized

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCHEMA_HOST_AUTH: Final = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_API_KEY): str,
    }
)

SCHEMA_REAUTH: Final = vol.Schema(
    {
        vol.Required(CONF_API_KEY): str
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from SCHEMA_HOST_AUTH with values provided by the user.
    """
    url = data[CONF_HOST]
    api_key = data[CONF_API_KEY]

    try:
        pterodactyl_api = PterodactylClient(url, api_key)
        await hass.async_add_executor_job(pterodactyl_api.client.account.get_account)
    except ClientConfigError as exception:
        raise Unauthorized from exception

    return {CONF_HOST: url, CONF_API_KEY: api_key}


class ConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Pterodactyl Panel."""

    host: str

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except Unauthorized:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(info[CONF_HOST])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=info[CONF_HOST], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=SCHEMA_HOST_AUTH,
            errors=errors
        )

    async def async_step_reauth(
        self, entry_data: Mapping[str, Any]
    ) -> ConfigFlowResult:
        """Perform reauth upon an authentication error."""
        self.host = entry_data[CONF_HOST]
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Dialog that informs the user that reauth is required."""
        errors: dict[str, str] = {}
        if user_input:
            try:
                user_input[CONF_HOST] = self.host
                info = await validate_input(self.hass, user_input)
            except Unauthorized:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(info[CONF_HOST])
                self._abort_if_unique_id_mismatch(reason="wrong_account")
                return self.async_update_reload_and_abort(
                    self._get_reauth_entry(),
                    data_updates={CONF_API_KEY: info[CONF_API_KEY]},
                )
        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=SCHEMA_REAUTH,
            errors=errors,
        )
