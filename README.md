# Cosmic Webhook Sender for Home Assistant

This custom integration allows you to send webhook messages (e.g., to Discord, Slack, or your own server) from Home Assistant.

The **Cosmic Webhook Sender** extends the basic idea of a webhook sender by giving your automations a stellar name. It continues to support multiple payload formats and asynchronous processing so your automations remain responsive.

## Features
- Send messages via Discord, JSON, raw text or form data
- Asynchronous request handling using aiohttp
- Easy integration into your automations

## Installation

1. Copy the `cosmic_webhook_sender` folder into your `config/custom_components/` directory.
2. Restart Home Assistant.
3. Call the service `cosmic_webhook_sender.send` in your automations.

## Example Automation

```yaml
action:
  - service: cosmic_webhook_sender.send
    data:
      url: "https://discord.com/api/webhooks/..."
      message: "Motion detected!"
      payload_type: "discord"
```

## Payload Types

| Type    | Description |
|---------|-------------|
| discord | Sends `{ "content": "message" }` |
| json    | Sends `{ "message": "message" }` |
| raw     | Sends plain text |
| form    | Sends as form-encoded `message=...` |
