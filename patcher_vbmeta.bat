@echo off
setlocal enabledelayedexpansion
title Universal MTK VBMeta Patcher - Open Source Tool

color 0A

:: ===========================================================
::  Configuration
:: ===========================================================
set "IMG_NAME=vbmeta_mod.img"
set "AVB_SCRIPT=avbtool.py"
set "LOG_FILE=avbtool_log.txt"
set "PY_CMD="
set "SLOT_ARG="

echo =======================================================
echo   UNIVERSAL MEDIATEK (MTK) VBMETA PATCHER ^& ROOT HELPER
echo =======================================================
echo.
echo This tool will, on the connected device:
echo   1. Build a vbmeta image with AVB verification disabled
echo   2. Flash it to vbmeta / vbmeta_system / vbmeta_vendor
echo   3. Erase the metadata partition
echo   4. Perform a full data wipe (fastboot -w)
echo.
echo Requirements: bootloader already OEM-unlocked, fastboot
echo and Python 3 on PATH, and avbtool.py in this folder.
echo =======================================================
echo.

:: ===========================================================
:: STEP 0: DEPENDENCY CHECKS
:: ===========================================================
echo [0/6] Checking dependencies...

where fastboot >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] 'fastboot' was not found on PATH.
    echo Install Android Platform Tools and add it to PATH.
    goto error
)

where python >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=python"
) else (
    where py >nul 2>&1
    if not errorlevel 1 set "PY_CMD=py -3"
)

if not defined PY_CMD (
    color 0C
    echo [ERROR] No Python interpreter found ^(tried 'python' and 'py'^).
    echo Install Python 3.x from python.org with "Add to PATH" checked.
    goto error
)

%PY_CMD% -c "import sys; sys.exit(0 if sys.version_info[0]>=3 else 1)" >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] %PY_CMD% resolves to Python 2, but avbtool needs Python 3.
    echo Install Python 3.x and make sure it comes first on PATH.
    goto error
)

if not exist "%AVB_SCRIPT%" (
    color 0C
    echo [ERROR] '%AVB_SCRIPT%' not found in:
    echo   %cd%
    echo Place avbtool.py next to this .bat file and retry.
    goto error
)
echo [OK] fastboot, %PY_CMD% (3.x) and %AVB_SCRIPT% found.
echo.

:: ===========================================================
:: STEP 1: BUILD THE PATCHED VBMETA IMAGE
:: ===========================================================
if exist "%IMG_NAME%" del /f /q "%IMG_NAME%" >nul 2>&1

echo [1/6] Building %IMG_NAME% (4KB padding, flags=2 = verification disabled)...
%PY_CMD% "%AVB_SCRIPT%" make_vbmeta_image --flags 2 --padding_size 4096 --output "%IMG_NAME%" >"%LOG_FILE%" 2>&1

if errorlevel 1 (
    color 0C
    echo.
    echo [ERROR] avbtool exited with an error:
    echo -------------------------------------------------
    type "%LOG_FILE%"
    echo -------------------------------------------------
    goto error
)

if not exist "%IMG_NAME%" (
    color 0C
    echo.
    echo [ERROR] avbtool reported success but %IMG_NAME% was not created.
    echo -------------------------------------------------
    type "%LOG_FILE%"
    echo -------------------------------------------------
    goto error
)
echo [SUCCESS] %IMG_NAME% generated.
echo.

:: ===========================================================
:: STEP 2: CONNECT DEVICE AND DETECT SLOTS
:: ===========================================================
echo =======================================================
echo   WAITING FOR DEVICE IN FASTBOOT MODE
echo =======================================================
echo Connect your MediaTek device in FASTBOOT mode now...
fastboot wait-for-device >nul 2>&1
echo [SUCCESS] Device detected. Connected devices:
fastboot devices
echo.

fastboot getvar slot-count 2>&1 | findstr /i "slot-count: 2" >nul 2>&1
if not errorlevel 1 (
    set "SLOT_ARG=--slot all"
    echo [INFO] A/B device detected - vbmeta will be flashed to BOTH slots.
) else (
    echo [INFO] Single-slot device - flashing without --slot.
)
echo.

:: ===========================================================
:: STEP 3: CONFIRM BEFORE TOUCHING THE DEVICE
:: ===========================================================
echo =======================================================
echo   WARNING: THE NEXT STEPS ARE IRREVERSIBLE
echo =======================================================
echo   - AVB / Verified Boot will be disabled on this device
echo   - The metadata partition will be erased
echo   - ALL user data will be wiped (fastboot -w)
echo.
echo   Double-check the device serial listed above is correct.
echo   Back up anything you need BEFORE continuing.
echo   The bootloader must already be OEM-unlocked.
echo =======================================================
set /p CONFIRM="Type YES to continue, anything else to abort: "
if /i not "%CONFIRM%"=="YES" (
    echo.
    echo Aborted. Nothing was flashed or erased.
    goto end
)
echo.

:: ===========================================================
:: STEP 4: FLASH VBMETA PARTITIONS
:: ===========================================================
echo [2/6] Flashing %IMG_NAME% to vbmeta (required)...
fastboot %SLOT_ARG% flash vbmeta "%IMG_NAME%"
if errorlevel 1 (
    color 0C
    echo.
    echo [ERROR] Flashing vbmeta failed - stopping here on purpose,
    echo so metadata/userdata are NOT touched on a half-patched device.
    goto error
)

echo [3/6] Flashing %IMG_NAME% to vbmeta_system (optional)...
fastboot %SLOT_ARG% flash vbmeta_system "%IMG_NAME%" 2>nul
if errorlevel 1 echo [INFO] vbmeta_system not present on this device - skipped.

echo [4/6] Flashing %IMG_NAME% to vbmeta_vendor (optional)...
fastboot %SLOT_ARG% flash vbmeta_vendor "%IMG_NAME%" 2>nul
if errorlevel 1 echo [INFO] vbmeta_vendor not present on this device - skipped.
echo.

:: ===========================================================
:: STEP 5: METADATA + USERDATA WIPE
:: ===========================================================
echo [5/6] Erasing metadata partition...
fastboot erase metadata >nul 2>&1
if errorlevel 1 (
    fastboot format:ext4 metadata >nul 2>&1
    if errorlevel 1 echo [INFO] metadata partition not present or not erasable - skipped.
)

echo [6/6] Wiping userdata (fastboot -w)...
fastboot -w
if errorlevel 1 echo [INFO] fastboot -w reported an error - wipe manually from recovery if needed.
echo.

:: ===========================================================
:: STEP 6: [BONUS] OPTIONAL AUTO-PATCH BOOT
:: ===========================================================
if exist "boot.img" (
    echo.
    echo =======================================================
    echo   [BONUS] PATCHED BOOT IMAGE DETECTED
    echo =======================================================
    echo A 'boot.img' file was found in this folder.
    echo This tool can flash it automatically to complete root.
    echo =======================================================
    
    set "CONFIRM_BOOT="
    set /p CONFIRM_BOOT="Type YES to flash boot.img now, or press ENTER to skip: "
    
    if "!CONFIRM_BOOT!"=="YES" (
        echo.
        echo [BOOT-PATCH] Flashing boot.img to boot partition...
        fastboot %SLOT_ARG% flash boot "boot.img"
        if errorlevel 1 (
            color 0C
            echo [ERROR] Failed to flash boot.img. Check device connection.
        ) else (
            echo [SUCCESS] boot.img successfully flashed.
        )
    ) else (
        echo [INFO] Flashing boot.img skipped by the user.
    )
)
echo.

echo =======================================================
echo   DONE
echo =======================================================
echo vbmeta patched (verification disabled) and flashed.
echo Rebooting device now.
echo =======================================================
fastboot reboot
goto end

:error
echo.
echo [FAILED - patcher stopped, see the message above for why]
echo.

:end
pause
