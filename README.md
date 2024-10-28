# dont_unplug_ac

A Python script that plays an audio warning when a laptop's AC adapter is unplugged.

## Table of Contents

- [About](#about)
- [Features](#features)
- [Usage](#usage)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)

## About

This project aims to prevent accidental disconnection of a laptop's AC adapter, which can lead to unexpected shutdowns due to low battery. The script monitors the power status of the laptop and plays an audio file when the AC adapter is unplugged, allowing the user to reconnect the charger before the battery runs out completely.

## Features

- Monitors power status of the laptop
- Plays audio warnings when AC adapter is unplugged
- Prevents unexpected shutdowns due to low battery
- Designed for Linux systems (concept can be ported to Windows)

## Usage

To use this script:

1. Clone the repository
2. Install the required dependencies (see below)
3. Add the script to start automatically at boot

## Requirements

- Python 3.x
- `pyudev` library for monitoring system information
- `pygame` library for playing audio files

## Installation

To install the script:

1. Clone the repository:
```bash
git clone https://github.com/ibrahemesam/dont_unplug_ac.git
```
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

To configure the system to run the script automatically:

1. Add the script to your startup applications ` ~/.local/share/autocorrect/` or create a systemd service file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
> Give me a Star if you like it 🌟

## License

This project is licensed under the MIT License

