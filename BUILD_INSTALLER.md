# FabriCost - Building the Windows Installer

This guide will help you create a professional Windows installer for FabriCost with desktop shortcuts, start menu entries, and proper icons everywhere.

---

## 📋 Prerequisites

### 1. Python Environment
Make sure you have your virtual environment set up with all dependencies:

```powershell
# If you haven't already created the virtual environment:
python -m venv .venv

# Activate it:
.\.venv\Scripts\Activate.ps1

# Install all dependencies:
pip install -r requirements.txt

# Install PyInstaller (for building the .exe):
pip install pyinstaller
```

### 2. Inno Setup (Required for Installer)
Download and install **Inno Setup** (free):

**Download:** https://jrsoftware.org/isdl.php

- Download the latest version (e.g., `innosetup-6.x.x.exe`)
- Run the installer
- Use default installation path: `C:\Program Files (x86)\Inno Setup 6\`

---

## 🚀 Quick Build (Automated)

### Option 1: Use the Build Script (EASIEST)

Simply run the automated build script:

```powershell
.\build_installer.bat
```

This script will:
1. ✓ Activate your virtual environment
2. ✓ Install PyInstaller if needed
3. ✓ Create the Windows icon file from your logo
4. ✓ Build the executable with PyInstaller
5. ✓ Create the installer with Inno Setup

**Result:** You'll find `FabriCost_Setup_v1.0.exe` in the `installer_output` folder.

---

## 🔧 Manual Build (Step by Step)

If you prefer to build manually or the script encounters issues:

### Step 1: Create the Icon File

```powershell
python create_icon.py
```

This converts `FabriCost_Logo.png` to `FabriCost_Icon.ico` with multiple sizes for Windows.

### Step 2: Build the Executable

```powershell
pyinstaller FabriCost.spec --clean --noconfirm
```

**What this does:**
- Bundles your Python app into a standalone executable
- Includes all dependencies (Pillow, reportlab, pywin32)
- Embeds the FabriCost icon
- Includes the logo PNG file
- Creates a `dist\FabriCost\` folder with everything

**Time:** This takes 2-5 minutes depending on your computer.

### Step 3: Build the Installer

```powershell
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" FabriCost_Setup.iss
```

**What this does:**
- Creates a professional "Next, Next, Next" installer
- Adds desktop shortcut with the FabriCost logo
- Adds Start Menu entry with the logo
- Includes uninstaller
- Creates `installer_output\FabriCost_Setup_v1.0.exe`

**Time:** This takes 30 seconds to 1 minute.

---

## 📦 What You Get

After building, you'll have:

```
3dPrix/
├── dist/
│   └── FabriCost/              # Standalone app folder
│       ├── FabriCost.exe       # Main executable
│       ├── FabriCost_Logo.png  # Logo file
│       ├── FabriCost_Icon.ico  # Icon file
│       └── [many DLL files]    # Required libraries
│
└── installer_output/
    └── FabriCost_Setup_v1.0.exe  # ⭐ INSTALLER - Distribute this!
```

---

## ✅ Testing the Installer

1. **Locate the installer:**
   ```
   installer_output\FabriCost_Setup_v1.0.exe
   ```

2. **Run it** (double-click)

3. **Follow the installer:**
   - Click "Next"
   - Choose installation folder (default: `C:\Program Files\FabriCost`)
   - Check "Create a desktop icon" if you want
   - Click "Next"
   - Click "Install"
   - Click "Finish"

4. **Check the results:**
   - ✓ Desktop shortcut with FabriCost logo
   - ✓ Start Menu entry: "FabriCost"
   - ✓ When you run it, taskbar shows FabriCost logo (not Python logo)
   - ✓ Application window icon is FabriCost logo

---

## 🎯 Icon Verification Checklist

After installation, verify all icons are correct:

- [ ] Desktop shortcut shows FabriCost logo
- [ ] Start Menu entry shows FabriCost logo
- [ ] Taskbar button (when app is running) shows FabriCost logo
- [ ] Application window title bar shows FabriCost logo (small)
- [ ] Alt+Tab shows FabriCost logo

**If icons don't show correctly:**
- Make sure `FabriCost_Icon.ico` was created successfully
- Rebuild with `pyinstaller FabriCost.spec --clean --noconfirm`
- Sometimes Windows caches icons - try rebooting

---

## 🐛 Troubleshooting

### Problem: "PyInstaller not found"
**Solution:**
```powershell
pip install pyinstaller
```

### Problem: "Inno Setup not found"
**Solution:**
- Download from https://jrsoftware.org/isdl.php
- Install to default location
- Or edit `build_installer.bat` with your Inno Setup path

### Problem: "Module not found" errors when running the .exe
**Solution:**
- Make sure all packages are installed: `pip install -r requirements.txt`
- Check `FabriCost.spec` includes the missing module in `hiddenimports`
- Rebuild: `pyinstaller FabriCost.spec --clean`

### Problem: Icons show as default/generic icons
**Solution:**
- Verify `FabriCost_Icon.ico` exists and has multiple sizes
- Run `python create_icon.py` again
- Rebuild everything from scratch

### Problem: "sqlite3.dll not found"
**Solution:**
- This is usually bundled with Python, but if missing:
- Copy `sqlite3.dll` from your Python installation to `dist\FabriCost\`

### Problem: Installer crashes during build
**Solution:**
- Make sure `dist\FabriCost\` folder exists and contains `FabriCost.exe`
- Check file paths in `FabriCost_Setup.iss` are correct
- Try running Inno Setup manually and check error messages

---

## 📤 Distribution

Once built and tested, you can distribute `FabriCost_Setup_v1.0.exe`:

**File to share:** `installer_output\FabriCost_Setup_v1.0.exe`

**Size:** Approximately 40-60 MB (includes Python runtime and all libraries)

**Requirements for users:**
- Windows 7 or later
- No Python installation required
- No other dependencies required

Users simply:
1. Download `FabriCost_Setup_v1.0.exe`
2. Run it
3. Click Next → Next → Install → Finish
4. Done! FabriCost is ready to use

---

## 🔄 Updating the Version

To create version 1.1, 2.0, etc.:

1. **Edit `FabriCost_Setup.iss`:**
   ```iss
   #define MyAppVersion "1.1"  ; Change this
   ```

2. **Rebuild:**
   ```powershell
   .\build_installer.bat
   ```

3. **Result:** `FabriCost_Setup_v1.1.exe`

---

## 📝 Files Created by This Build Process

| File | Purpose |
|------|---------|
| `FabriCost_Icon.ico` | Windows icon file (created from PNG logo) |
| `build/` | Temporary build files (can be deleted) |
| `dist/FabriCost/` | Standalone application folder |
| `dist/FabriCost/FabriCost.exe` | Main executable |
| `installer_output/FabriCost_Setup_v1.0.exe` | **Final installer** |

---

## ⚡ Quick Reference

```powershell
# Complete build process (one command):
.\build_installer.bat

# Or manually:
python create_icon.py
pyinstaller FabriCost.spec --clean --noconfirm
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" FabriCost_Setup.iss

# Result:
# installer_output\FabriCost_Setup_v1.0.exe
```

---

## 🎉 Success!

You now have a professional Windows installer that:
- ✅ Has a "Next, Next, Next" installation process
- ✅ Creates desktop shortcuts with your logo
- ✅ Shows your logo in the taskbar
- ✅ Shows your logo everywhere in Windows
- ✅ Includes an uninstaller
- ✅ Requires no Python installation for users
- ✅ Works on any Windows 7+ computer

**Enjoy distributing FabriCost!** 🎊

