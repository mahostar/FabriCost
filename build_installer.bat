@echo off
REM ============================================================
REM  FabriCost - Build Full Installer (EXE + Setup)
REM  Builds the standalone EXE first, then the Inno Setup installer
REM ============================================================

echo.
echo =============================================
echo   FabriCost - Building Full Installer
echo =============================================
echo.

REM -- Navigate to the script's directory --
pushd "%~dp0"

REM ============================
REM  STEP 1: Build the EXE
REM ============================
echo [STEP 1/2] Building standalone EXE...
echo.
call build_exe.bat

REM -- Check that the EXE was created --
if not exist "dist\FabriCost\FabriCost.exe" (
    echo.
    echo [ERROR] EXE build failed! Cannot proceed with installer.
    pause
    exit /b 1
)

REM ============================
REM  STEP 2: Build Inno Setup Installer
REM ============================
echo.
echo [STEP 2/2] Building Inno Setup installer...
echo.

REM -- Try to find Inno Setup ISCC.exe --
set "ISCC_PATH="

REM Check for local copy of Inno Setup
if exist "innosetup-6.6.1.exe" (
    echo Found local Inno Setup installer: innosetup-6.6.1.exe
)

REM Check common Inno Setup install locations
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    set "ISCC_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
)
if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    set "ISCC_PATH=C:\Program Files\Inno Setup 6\ISCC.exe"
)

if "%ISCC_PATH%"=="" (
    echo.
    echo [ERROR] Inno Setup ISCC.exe not found!
    echo.
    echo   Please install Inno Setup first:
    echo     1. Run: innosetup-6.6.1.exe  (in this folder)
    echo     2. Use default installation path
    echo     3. Re-run this script
    echo.
    echo   Or install from: https://jrsoftware.org/isdl.php
    echo.
    pause
    exit /b 1
)

echo Using Inno Setup: %ISCC_PATH%
echo.

REM -- Create output directory --
if not exist "installer_output" mkdir installer_output

REM -- Compile the installer --
"%ISCC_PATH%" FabriCost_Setup.iss

REM -- Check result --
if exist "installer_output\FabriCost_Setup_v1.0.exe" (
    echo.
    echo =============================================
    echo   INSTALLER BUILD SUCCESSFUL!
    echo =============================================
    echo.
    echo   Installer: installer_output\FabriCost_Setup_v1.0.exe
    echo.
    echo   Share this file with your users!
    echo   They just double-click and follow the wizard.
    echo.
) else (
    echo.
    echo =============================================
    echo   INSTALLER BUILD FAILED!
    echo =============================================
    echo.
    echo   Make sure Inno Setup is installed correctly.
    echo.
)

popd
pause
