# Meshtastic GUI

A Python-based GUI application for interacting with Meshtastic devices, built using flet and the Meshtastic Python API. This project aims to provide a user-friendly desktop alternative to the official Meshtastic clients, eventually offering the same functionality as the iOS, Android, and web clients, in an offline-capable, native desktop form.

---

## Current Status

![Project Status](https://img.shields.io/badge/status-in%20progress-yellow)

This project is still under development and will continue evolving with time, feedback, and feature requests.

---

## Project Goals

The primary goal of this project is to provide a full-featured, offline-capable desktop client with the same features as the official Meshtastic mobile and web apps.

### Core Objectives

- Offline-first functionality
- Native Windows & Linux support
- Clean and modern UI
- All core Meshtastic Client functions

---

## Getting Started

### Requirements

- Python 3.14
- meshtastic
- flet

### Installation

```bash
git clone https://github.com/axlixr/meshtastic-desktop-application.git
cd meshtastic-desktop-application
```
```bash
python3.14 -m venv .venv
```
```bash
#Activate it on Linux/macOS
source .venv/bin/activate
```
```bash
#Activate it on Windows
.venv\Scripts\activate
```

### Running the App
-  **Linux** users will need **Sudo** when running the app for access to the serial port:
```bash
python main.py
```

---

## Current Features
- Serial Connection (USB)
- Network Connection (TCP)
- My Node Information
- Messaging (Primary Channel & Direct Messages)
- Connected Nodes
- Configure Long Name & Short Name

---

## Preview

<img src="img/preview1.png" alt="Meshtastic GUI Preview" width="800"/>

---

## License

This project is licensed under the GNU General Public License