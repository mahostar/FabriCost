@echo off
REM ============================================================
REM  FabriCost - Build Standalone EXE (no installer)
REM  This script activates the venv and builds using PyInstaller
REM ============================================================

echo.
echo ========================================
echo   FabriCost - Building Standalone EXE
echo ========================================
echo.

REM -- Navigate to the script's directory --
pushd "%~dp0"

REM -- Check that .venv exists --
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo         Please run: python -m venv .venv
    echo         Then: .venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)

REM -- Activate the virtual environment --
echo [1/4] Activating virtual environment...
call .venv\Scripts\activate.bat

REM -- Ensure PyInstaller is installed --
echo [2/4] Ensuring PyInstaller is installed...
pip install pyinstaller>=6.0.0 --quiet

REM -- Check that required files exist --
if not exist "main.py" (
    echo [ERROR] main.py not found!
    pause
    exit /b 1
)
if not exist "FabriCost_Icon.ico" (
    echo [ERROR] FabriCost_Icon.ico not found!
    echo         Please make sure the icon file is in the project directory.
    pause
    exit /b 1
)
if not exist "FabriCost_Logo.png" (
    echo [ERROR] FabriCost_Logo.png not found!
    pause
    exit /b 1
)
if not exist "FabriCost.spec" (
    echo [ERROR] FabriCost.spec not found!
    pause
    exit /b 1
)

REM -- Build the EXE --
echo [3/4] Building FabriCost.exe with PyInstaller...
echo         This may take 2-5 minutes...
echo.
pyinstaller FabriCost.spec --clean --noconfirm

REM -- Check result --
if exist "dist\FabriCost\FabriCost.exe" (
    echo.
    echo ========================================
    echo   BUILD SUCCESSFUL!
    echo ========================================
    echo.
    echo   EXE Location: dist\FabriCost\FabriCost.exe
    echo.
    echo   To test: double-click dist\FabriCost\FabriCost.exe
    echo.
    echo [4/4] Done!
) else (
    echo.
    echo ========================================
    echo   BUILD FAILED!
    echo ========================================
    echo.
    echo   Check the error messages above.
    echo   Common fixes:
    echo     - pip install -r requirements.txt
    echo     - pip install pyinstaller
    echo.
)

popd
pause
