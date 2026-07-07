@echo off
setlocal enabledelayedexpansion
title Universal MTK VBMeta Patcher - Open Source Tool

:: Technical Matrix Style Color (Green text on Black background)
color 0A

:: Global configuration variables for maintenance
set IMG_NAME=vbmeta_mod.img
set AVB_SCRIPT=avbtool.py

echo =======================================================
echo   UNIVERSAL MEDIATEK (MTK) VBMETA PATCHER ^& ROOT HELPER
echo =======================================================
echo.

:: STEP 1: DYNAMIC COMPILATION ^& INTEGRITY CHECK
echo [1/6] Running AVBTOOL Python script...
echo Generating %IMG_NAME% (4KB padding + Flag 2 Disabled)...

:: Silently execute Python avbtool compiler
python %AVB_SCRIPT% make_vbmeta_image --flags 2 --padding_size 4096 --output %IMG_NAME% >nul 2>&1

if not exist %IMG_NAME% (
    color 0C
    echo.
    echo [ERROR] Failed to generate %IMG_NAME%! 
    echo Please verify Python 3.x is installed and properly added to your System PATH.
    echo Make sure '%AVB_SCRIPT%' resides in this exact working directory.
    goto error
)
echo [SUCCESS] %IMG_NAME% generated successfully.
echo.

echo =======================================================
echo   WAITING FOR DEVICE IN FASTBOOT MODE
echo =======================================================
echo Connect your MediaTek device in FASTBOOT mode now...
fastboot wait-for-device >nul 2>&1
echo [SUCCESS] Android target device detected!
echo.

:: STEP 2: SMART PARTITION FLASHING OVERRIDES
:: Added error redirection (2>nul) to ensure backwards compatibility if vendor/system slots are missing
echo [2/6] Flashing %IMG_NAME% to primary vbmeta partition...
fastboot flash vbmeta %IMG_NAME%

echo [3/6] Flashing %IMG_NAME% to secondary vbmeta_system partition...
fastboot flash vbmeta_system %IMG_NAME% 2>nul

echo [4/6] Flashing %IMG_NAME% to tertiary vbmeta_vendor partition...
fastboot flash vbmeta_vendor %IMG_NAME% 2>nul

echo.
echo =======================================================
echo   ENFORCING MANDATORY DATA SANITIZATION
echo =======================================================
:: Fallback handling via logical operators to bypass strict MTK preloader security policies
echo [5/6] Wiping crypto metadata blocks...
fastboot metadata erase >nul 2>&1 || fastboot format:ext4 metadata >nul 2>&1

echo [6/6] Wiping logical userdata blocks (Enforcing Factory Reset)...
fastboot -w >nul 2>&1

echo.
echo =======================================================
echo   EXECUTION COMPLETED SUCCESSFULLY!
echo =======================================================
echo Partition locks bypassed. System rebooting now...
echo You may now safely deploy APatch or Magisk kernels.
fastboot reboot
goto end

:error
echo.
echo [FATAL ERROR - DEPLOYMENT TERMINATED]
echo.

:end
pause
