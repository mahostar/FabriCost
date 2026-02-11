# 📦 FabriCost Installer - Files Overview

This document explains what each file does in the installer build process.

---

## 🎯 Main Files (What You Need)

| File | Purpose | When to Use |
|------|---------|-------------|
| **`build_installer.bat`** | Automated build script | Run this to build everything! |
| **`QUICK_START_INSTALLER.md`** | Quick guide | Read this first |
| **`BUILD_INSTALLER.md`** | Detailed guide | For troubleshooting |

---

## 🔧 Configuration Files (Don't Edit Unless Needed)

### `create_icon.py`
**Purpose:** Converts `FabriCost_Logo.png` to `FabriCost_Icon.ico`

**What it does:**
- Creates a Windows icon file (.ico) from your PNG logo
- Includes multiple sizes: 16×16, 32×32, 48×48, 64×64, 128×128, 256×256
- Required for Windows shortcuts, taskbar, and window icons

**When to run:**
```powershell
python create_icon.py
```

**Output:** `FabriCost_Icon.ico`

---

### `FabriCost.spec`
**Purpose:** PyInstaller configuration file

**What it does:**
- Tells PyInstaller how to bundle your Python app into an .exe
- Specifies which files to include (logo, icon)
- Includes hidden imports (win32clipboard, PIL, etc.)
- Sets the icon for the executable
- Disables the console window (GUI only)

**Key settings:**
```python
datas=[
    ('FabriCost_Logo.png', '.'),  # Include logo
    ('FabriCost_Icon.ico', '.'),  # Include icon
],
icon='FabriCost_Icon.ico',  # Window icon
console=False,  # No console window
```

**When to run:**
```powershell
pyinstaller FabriCost.spec --clean --noconfirm
```

**Output:** `dist\FabriCost\FabriCost.exe` (and dependencies)

---

### `FabriCost_Setup.iss`
**Purpose:** Inno Setup configuration script

**What it does:**
- Creates the Windows installer (.exe)
- Defines installation steps ("Next, Next, Next")
- Creates desktop shortcuts with your logo
- Creates Start Menu entries with your logo
- Sets up uninstaller
- Supports multiple languages (English, French)

**Key settings:**
```iss
#define MyAppName "FabriCost"
#define MyAppVersion "1.0"
#define MyAppPublisher "Mahou"
#define MyAppIcon "FabriCost_Icon.ico"

SetupIconFile={#MyAppIcon}  ; Installer icon
```

**When to run:**
```powershell
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" FabriCost_Setup.iss
```

**Output:** `installer_output\FabriCost_Setup_v1.0.exe`

---

### `requirements.txt`
**Purpose:** Python dependencies

**Updated to include:**
```
Pillow>=10.0.0      # Image processing (logo, receipt images)
reportlab>=4.0.0    # PDF generation
pywin32>=306        # Windows clipboard functionality
pyinstaller>=6.0.0  # Building executable
```

---

## 📁 Folders Created During Build

| Folder | Contents | Can Delete? |
|--------|----------|-------------|
| **`build/`** | Temporary PyInstaller files | ✅ Yes (after build) |
| **`dist/FabriCost/`** | Standalone app folder with .exe | ⚠️ Needed for installer |
| **`installer_output/`** | Final installer .exe | ❌ No - this is your output! |

---

## 🔄 Build Process Flow

```
1. create_icon.py
   ↓ creates
   FabriCost_Icon.ico

2. pyinstaller FabriCost.spec
   ↓ creates
   dist/FabriCost/FabriCost.exe
   (+ all dependencies)

3. Inno Setup (FabriCost_Setup.iss)
   ↓ packages
   installer_output/FabriCost_Setup_v1.0.exe
   ↓
   🎉 DONE! Distribute this file!
```

---

## 🎨 Logo Files in the Project

| File | Format | Use |
|------|--------|-----|
| **`FabriCost_Logo.png`** | PNG | Original logo, displayed in app UI |
| **`FabriCost_Icon.ico`** | ICO | Windows icon (created by `create_icon.py`) |

**How icons are used:**
1. **In the app code (`main.py`):**
   - Loads `FabriCost_Logo.png` for splash screen and menu
   - Uses `tk.PhotoImage` for window icon

2. **In the executable:**
   - `FabriCost_Icon.ico` embedded by PyInstaller
   - Shows in taskbar, Alt+Tab, window title

3. **In shortcuts:**
   - `FabriCost_Icon.ico` referenced by Inno Setup
   - Shows on desktop and Start Menu

---

## ⚙️ Customization Points

### Change App Version
**Edit:** `FabriCost_Setup.iss`
```iss
#define MyAppVersion "1.1"  ; Change this
```

### Change Author Name
**Edit:** `FabriCost_Setup.iss`
```iss
#define MyAppPublisher "Your Name"  ; Change this
```

### Add More Files to Bundle
**Edit:** `FabriCost.spec`
```python
datas=[
    ('FabriCost_Logo.png', '.'),
    ('your_file.txt', '.'),  ; Add this
],
```

### Change Installation Directory
**Edit:** `FabriCost_Setup.iss`
```iss
DefaultDirName={autopf}\FabriCost  ; Change this
```

---

## 🐛 Debugging

### Check if icon was created correctly
```powershell
# Should exist and be ~100 KB
dir FabriCost_Icon.ico
```

### Check if .exe was built correctly
```powershell
# Should exist with your logo icon
dir dist\FabriCost\FabriCost.exe

# Test it directly
.\dist\FabriCost\FabriCost.exe
```

### Check if installer was created
```powershell
# Should exist and be 40-60 MB
dir installer_output\FabriCost_Setup_v1.0.exe
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `QUICK_START_INSTALLER.md` | Quick 5-minute guide |
| `BUILD_INSTALLER.md` | Complete detailed guide with troubleshooting |
| `INSTALLER_FILES_OVERVIEW.md` | This file - explains all files |

---

## ✅ Checklist for First Build

- [ ] Python virtual environment created and activated
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Inno Setup installed from https://jrsoftware.org/isdl.php
- [ ] `FabriCost_Logo.png` exists in project folder
- [ ] Run `build_installer.bat`
- [ ] Check `installer_output\FabriCost_Setup_v1.0.exe` was created
- [ ] Test the installer on your computer
- [ ] Verify desktop shortcut shows your logo
- [ ] Run app and verify taskbar shows your logo
- [ ] Ready to distribute! 🎉

---

## 🎯 Final Output

**File to distribute:** `installer_output\FabriCost_Setup_v1.0.exe`

**What users get when they install:**
- Desktop shortcut with FabriCost logo
- Start Menu entry with FabriCost logo
- FabriCost application that shows your logo in taskbar
- Working 3D and Laser calculators with all features
- No Python required!

---

## 💡 Tips

1. **Always clean build for release:**
   ```powershell
   pyinstaller FabriCost.spec --clean --noconfirm
   ```

2. **Test the installer before distributing:**
   - Install on a fresh Windows VM if possible
   - Check all icons appear correctly
   - Test all app features

3. **Version control:**
   - Update version number in `FabriCost_Setup.iss`
   - Keep old installers for rollback

4. **File size:**
   - Installer will be 40-60 MB
   - This is normal - includes Python runtime
   - Users don't need Python installed

---

That's everything you need to know about the installer build system! 🚀

