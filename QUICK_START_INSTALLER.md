# 🚀 Quick Start - Build FabriCost Installer

## What You'll Get
A professional Windows installer (`FabriCost_Setup_v1.0.exe`) that:
- Creates desktop shortcuts with **your logo**
- Shows **your logo** in the taskbar (not Python logo)
- Has a "Next, Next, Next" installation experience
- Works on any Windows computer without Python

---

## Prerequisites (Install Once)

### 1. Install Inno Setup (5 minutes)
Download and install from: **https://jrsoftware.org/isdl.php**
- Click "Next, Next, Install" using default settings
- That's it!

### 2. Setup Python Environment
```powershell
# Create virtual environment
python -m venv .venv

# Activate it (PowerShell)
.\.venv\Scripts\Activate.ps1

# If you get an error about execution policy, run this ONCE:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install all dependencies
pip install -r requirements.txt
```

---

## Build the Installer (3 commands)

```powershell
# 1. Activate your virtual environment
.\.venv\Scripts\Activate.ps1

# 2. Run the build script (ONE COMMAND - builds everything!)
.\build_installer.bat

# 3. Done! Your installer is ready:
# installer_output\FabriCost_Setup_v1.0.exe
```

**Time:** 3-5 minutes total

---

## Or Use the Automated Script

Just double-click: **`build_installer.bat`**

The script will:
1. ✓ Create the icon file from your logo
2. ✓ Build the .exe with PyInstaller
3. ✓ Create the installer with Inno Setup
4. ✓ Tell you when it's done!

---

## Test Your Installer

1. Find the installer:
   ```
   installer_output\FabriCost_Setup_v1.0.exe
   ```

2. Double-click it and install

3. Check:
   - ✓ Desktop icon shows FabriCost logo
   - ✓ Run the app → taskbar shows FabriCost logo
   - ✓ Everything works!

---

## Distribute to Users

**Share this file:** `installer_output\FabriCost_Setup_v1.0.exe`

Users just:
1. Download it
2. Double-click
3. Click "Next, Next, Install"
4. Done!

**No Python required for users!**

---

## Troubleshooting

**Problem:** "Cannot run scripts"
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Problem:** "Inno Setup not found"
- Install Inno Setup from: https://jrsoftware.org/isdl.php
- Use default installation path

**Problem:** Need more help?
- Read the full guide: `BUILD_INSTALLER.md`

---

## File Structure After Build

```
3dPrix/
├── create_icon.py              # Converts PNG → ICO
├── FabriCost.spec              # PyInstaller config
├── FabriCost_Setup.iss         # Inno Setup config
├── build_installer.bat         # Automated build script
│
├── FabriCost_Icon.ico          # Created by build
│
├── dist/
│   └── FabriCost/              # Standalone app folder
│       └── FabriCost.exe       # The executable
│
└── installer_output/
    └── FabriCost_Setup_v1.0.exe  # 🎯 THE INSTALLER (share this!)
```

---

## That's It! 🎉

You now have a professional installer with your logo everywhere!

