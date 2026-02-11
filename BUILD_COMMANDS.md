# FabriCost - Build Commands

Run all commands from: `c:\Users\mouha\Desktop\Travail\3dPrix`

---

## Step 1: Setup Virtual Environment (one-time)

```cmd
python -m venv .venv --clear
```

## Step 2: Install Dependencies

```cmd
cmd /c ".venv\Scripts\activate && pip install Pillow>=10.0.0 reportlab>=4.0.0 pywin32>=306 pyinstaller>=6.0.0"
```

## Step 3: Build Standalone EXE

```cmd
cmd /c ".venv\Scripts\activate && pyinstaller FabriCost.spec --clean --noconfirm"
```

**Output:** `dist\FabriCost\FabriCost.exe` — double-click to test.

> ⚠️ Ignore the `build\` folder — it's temporary PyInstaller files, NOT a runnable app.

## Step 4: Build Installer (requires Inno Setup installed)

```cmd
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" FabriCost_Setup.iss
```

**Output:** `installer_output\FabriCost_Setup_v1.0.exe` — share this with users!

---

## Quick Rebuild (all-in-one)

```cmd
cmd /c ".venv\Scripts\activate && pyinstaller FabriCost.spec --clean --noconfirm" && "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" FabriCost_Setup.iss
```

---

## Batch Scripts

| Script | What It Does |
|--------|-------------|
| `build_exe.bat` | Steps 2-3 (EXE only) |
| `build_installer.bat` | Steps 2-4 (EXE + installer) |
