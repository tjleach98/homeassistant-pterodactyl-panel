[![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/tjleach98/homeassistant-pterodactyl-panel/.github%2Fworkflows%2Fvalidate.yml?style=flat-square&label=validate)](https://github.com/tjleach98/homeassistant-pterodactyl-panel/actions/workflows/validate.yml)
[![GitHub Release](https://img.shields.io/github/release/tjleach98/homeassistant-pterodactyl-panel.svg?style=flat-square)](https://github.com/tjleach98/homeassistant-pterodactyl-panel/releases)
[![GitHub](https://img.shields.io/github/license/tjleach98/homeassistant-pterodactyl-panel.svg?style=flat-square)](LICENSE)
[![Downloads](https://img.shields.io/github/downloads/tjleach98/homeassistant-pterodactyl-panel/total?style=flat-square)](https://github.com/tjleach98/homeassistant-pterodactyl-panel/releases)

# Pterodactyl Panel Home Assistant Integration
This is a basic Home Assistant integration for the [Pterodactyl Panel](https://pterodactyl.io/). It uses the `py-dactyl` library available [here](https://github.com/iamkubi/pydactyl)

## Influence
The source code for this project is influenced by the [Proxmox VE](https://github.com/dougiteixeira/proxmoxve) integration.

## Installation
### Manual
Place the entire `custom_components/pterodactyl_panel` folder in this repo inside the `config/custom_components/` folder of your Home Assistant instance. 

If `custom_components` doesn't exist, create it. Click [here](https://developers.home-assistant.io/docs/creating_integration_file_structure/#where-home-assistant-looks-for-integrations) for more details.

Once the files are in place, restart Home Assistant and the integration should be available.

### HACS
Add this repository to HACS as a custom repository. Details for this can be found [here](https://hacs.xyz/docs/faq/custom_repositories).

## Setup
Go to Account Settings -> API Credentials -> Create API Key.

## Currently Available Sensors
### Button
#### Server
- Start
- Stop
- Restart

### Binary Sensor
#### Server
- Is Running
- Is Under Maintenance

### Sensor
#### Server
- Absolute CPU Usage
- Current State
- Disk Usage
- Memory Usage
- Network Upload/Download
- Current Node
- Uptime