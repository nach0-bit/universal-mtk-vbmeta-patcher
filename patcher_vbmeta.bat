@echo off
title Universal MTK VBMeta Patcher - Open Source Tool
echo =======================================================
echo   UNIVERSAL MEDIATEK (MTK) VBMETA PATCHER & ROOT HELPER
echo =======================================================
echo.

:: STEP 1: GENERATE MODIFIED VBMETA VIA AVBTOOL
echo [1/6] Running AVBTOOL Python script...
echo Generating vbmeta_mod.img (4KB padding + Flag 2 Disabled)...
python avbtool.py make_vbmeta_image --flags 2 --padding_size 4096 --output vbmeta_mod.img

if not exist vbmeta_mod.img (
    echo.
    echo [ERROR] Failed to generate vbmeta_mod.img! 
    echo Please ensure Python is installed and avbtool.py is in this directory.
    goto error
)
echo [SUCCESS] vbmeta_mod.img generated perfectly.
echo.
echo =======================================================
echo   WAITING FOR DEVICE IN FASTBOOT MODE
echo =======================================================
echo Connect your MTK device in FASTBOOT mode now...
fastboot wait-for-device
echo [SUCCESS] Device detected!
echo.

:: STEP 2: FLASH IMAGES TO TARGET PARTITIONS
echo [2/6] Flashing vbmeta_mod.img to vbmeta...
fastboot flash vbmeta vbmeta_mod.img

echo [3/6] Flashing vbmeta_mod.img to vbmeta_system...
fastboot flash vbmeta_system vbmeta_mod.img

echo [4/6] Flashing vbmeta_mod.img to vbmeta_vendor...
fastboot flash vbmeta_vendor vbmeta_mod.img

echo.
echo =======================================================
echo   PERFORMING MANDATORY FACTORY RESET
echo =======================================================
echo [5/6] Wiping metadata...
fastboot metadata erase

echo [6/6] Wiping userdata (Factory Reset)...
fastboot -w

echo.
echo =======================================================
echo   PROCESS COMPLETED SUCCESSFULLY!
echo =======================================================
echo Your phone will now reboot. You can proceed with APatch / Magisk.
fastboot reboot
goto end

:error
echo.
echo [PROCESS TERMINATED WITH ERRORS]
echo.

:end
pause
