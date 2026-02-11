<div align="center">
  <img src="FabriCost_Logo.png" alt="FabriCost Logo" width="200">
  <h1>FabriCost</h1>
  <p><strong>Professional 3D Printing & Laser Cutting Price Calculator</strong></p>
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
  [![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
</div>

---

## 🚀 Overview

**FabriCost** is a powerful desktop application designed solely for makers and fabrication shops. It helps you accurately calculate quotes for **3D Printing** and **Laser Cutting** projects by factoring in material costs, machine time, energy usage, and markup.

Say goodbye to guesswork and spreadsheets—get professional, consistent pricing in seconds.

## ✨ Key Features

- **Dual Mode Calculator**: Switch instantly between 3D Printing and Laser Cutting modes.
- **Detailed Pricing Rules**:
  - **Material Cost**: Price per gram (for 3D printing).
  - **Hourly Rates**: Set standard and "exceeded" hourly rates.
  - **Thresholds**: Apply different rates after a certain number of hours.
  - **Markup Control**: Easily adjust your profit margin percentage.
- **PDF Generation**: Export professional quotes in detailed or simple formats.
- **Copy to Clipboard**: Quickly paste formatted quotes into WhatsApp, Email, or Slack.
- **Receipt Generation**: Create shareable images of the calculation for clients.
- **Multi-Language**: Fully localized in **English** and **French**.
- **Dark/Light Themed UI**: Modern, clean interface built with Tkinter.

## 🛠️ Installation

### For Users (Windows Installer)
Download the latest installer from the [Releases](https://github.com/mahostar/FabriCost/releases) page (coming soon) or build it yourself:

1. Download `FabriCost_Setup_v1.0.exe`
2. Run the installer
3. Launch **FabriCost** from your desktop!

### For Developers (Source Code)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mahostar/FabriCost.git
   cd FabriCost
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Mac/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**:
   ```bash
   python main.py
   ```

## 📦 Building from Source (EXE & Installer)

Want to build your own `.exe` or installer? We've made it easy with batch scripts included in the repo.

### Prerequisites
- Python 3.10+
- [Inno Setup 6](https://jrsoftware.org/isdl.php) (for installer only)

### Build Commands

| Goal | Command | Description |
|------|---------|-------------|
| **Build EXE** | `build_exe.bat` | Creates a standalone executable in `dist/FabriCost/` |
| **Build Installer** | `build_installer.bat` | Creates the full installer in `installer_output/` |

For a detailed guide, see [BUILD_COMMANDS.md](BUILD_COMMANDS.md).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <sub>Built with ❤️ by Mahou</sub>
</div>
