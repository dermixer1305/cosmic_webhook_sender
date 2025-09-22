import logging
import aiohttp
import asyncio
from homeassistant.core import HomeAssistant, ServiceCall

_LOGGER = logging.getLogger(__name__)
# Domain used to register the integration within Home Assistant.  This must
# match the directory name of the component.
DOMAIN = "cosmic_webhook_sender"

async def async_setup(hass: HomeAssistant, config: dict):
    async def async_send_webhook(call: ServiceCall):
        url = call.data.get("url")
        message = call.data.get("message", "")
        payload_type = call.data.get("payload_type", "discord")

        headers = {}
        payload = None

        if payload_type == "discord":
            headers["Content-Type"] = "application/json"
            payload = {"content": message}
        elif payload_type == "json":
            headers["Content-Type"] = "application/json"
            payload = {"message": message}
        elif payload_type == "form":
            # Send as URL‑encoded form data. aiohttp will use the raw data when
            # passing a string via ``data``.
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            payload = f"message={message}"
        elif payload_type == "raw":
            headers["Content-Type"] = "text/plain"
            payload = message

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload if isinstance(payload, dict) else None,
                                        data=payload if isinstance(payload, str) else None) as response:
                    if response.status != 200:
                        _LOGGER.error("Webhook failed: %s", await response.text())
        except Exception as e:
            _LOGGER.exception("Error sending webhook: %s", e)

    hass.services.async_register(DOMAIN, "send", async_send_webhook)
    return True
