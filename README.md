<h1 align="center" style="font-weight: bold">~: dont_unplug_ac :~</h1>
<p align="center">
  <img src="logo.jpg" width="50%" style="border-radius: 10px;"/>
</p>

> play an audio warning when a laptop's AC adapter gets unplugged.

## Table of Contents

- [About](#about)
- [Features](#features)
- [Requirements](#requirements)
- [Usage](#usage)

## About

This project aims to prevent accidental disconnection of a laptop's AC adapter, which can lead to unexpected shutdowns due to low-health battery.<br>
It monitors the power status of the laptop and plays an audio file when the AC adapter gets unplugged, allowing the user to reconnect the charger quickly before the battery runs out completely.

## Features

- Monitors power status of the laptop
- Plays audio warning when AC adapter gets unplugged
- Prevents unexpected shutdowns due to low-health battery
- Available for <strong>Linux</strong> and <strong>Windows</strong> (concept can be ported to <strong>Mac</strong>)

## Requirements

- Python 3.x
- <strong>Linux</strong> or <strong>Windows</strong> system

## Usage

To use this script:

1. Clone the repository:
   - `git clone https://github.com/ibrahemesam/dont_unplug_ac.git`
2. Install Python requirements:-
   - on <strong>Linux</strong>: `pip install -r requirements_linux.txt`
   - on <strong>Windows</strong>: `pip install -r requirements_win32.txt`
3. Configure the app to start automatically at boot:-
   - on <strong>Linux</strong>: make link to the `main.py` script into your startup applications directory ` ~/.local/share/autocorrect/`. Or create a <strong>systemd service</strong> file.
   - on <strong>Windows</strong>: make a batch file that runs `python.exe /path/to/main.py` and place that batch file into startup folder `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp`.
     Or use <strong>Windows Task Scheduler</strong> to add a task that runs at boot.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

> Give me a Star if you like it 🌟

## License

This project is licensed under the <a href="https://opensource.org/license/MIT">MIT License</a>
