import os
import sys
import shutil
import subprocess

# Configuración básica
IMG_NAME = "vbmeta_mod.img"
AVB_SCRIPT = "avbtool.py"
LOG_FILE = "avbtool_log.txt"


def check_dependencies():
    print("[0/6] Checking dependencies...")

    # Buscamos fastboot en el PATH de forma limpia
    if shutil.which("fastboot") is None:
        print("[ERROR] 'fastboot' was not found on PATH. Install Android Platform Tools.")
        sys.exit(1)

    if not os.path.exists(AVB_SCRIPT):
        print(f"[ERROR] '{AVB_SCRIPT}' not found in: {os.getcwd()}")
        sys.exit(1)

    print(f"[OK] fastboot and {AVB_SCRIPT} found.\n")


def build_patched_image():
    if os.path.exists(IMG_NAME):
        os.remove(IMG_NAME)

    print(f"[1/6] Building {IMG_NAME} (4KB padding, flags=2 = verification disabled)...")

    # Ejecutamos usando el intérprete actual para evitar conflictos de rutas
    cmd = [sys.executable, AVB_SCRIPT, "make_vbmeta_image",
           "--flags", "2", "--padding_size", "4096", "--output", IMG_NAME]

    with open(LOG_FILE, "w") as log:
        result = subprocess.run(cmd, stdout=log, stderr=log)

    if result.returncode != 0 or not os.path.exists(IMG_NAME):
        print("\n[ERROR] avbtool failed to generate the image. Output:")
        print("-" * 51)
        try:
            with open(LOG_FILE, "r") as log:
                print(log.read())
        except OSError:
            pass
        print("-" * 51)
        sys.exit(1)

    print(f"[SUCCESS] {IMG_NAME} generated.\n")


def check_and_flash_boot(slot_arg):
    # Lógica del Bonus Root Helper integrada en Python
    if os.path.exists("boot.img"):
        print("\n=======================================================")
        print("  [BONUS] PATCHED BOOT IMAGE DETECTED")
        print("=======================================================")
        print("A 'boot.img' file was found in this folder.")
        print("This tool can flash it automatically to complete root.")
        print("=======================================================")
        
        try:
            confirm_boot = input("Type YES to flash boot.img now, or press ENTER to skip: ")
        except KeyboardInterrupt:
            print("\n[INFO] Boot flashing skipped (interrupted).")
            return

        if confirm_boot.strip() == "YES":
            print("\n[BOOT-PATCH] Flashing boot.img to boot partition...")
            res = subprocess.run(["fastboot"] + slot_arg + ["flash", "boot", "boot.img"])
            if res.returncode != 0:
                print("[ERROR] Failed to flash boot.img. Check device connection.")
            else:
                print("[SUCCESS] boot.img successfully flashed.")
        else:
            print("\n[INFO] Flashing boot.img skipped by the user.")


def flash_device():
    print("=======================================================")
    print("  WAITING FOR DEVICE IN FASTBOOT MODE")
    print("=======================================================")
    print("Connect your MediaTek device in FASTBOOT mode now...")

    subprocess.run(["fastboot", "wait-for-device"])
    print("[SUCCESS] Device detected. Connected devices:")
    subprocess.run(["fastboot", "devices"])
    print()

    # Detectar Slots (A/B)
    slot_arg = []
    proc = subprocess.run(["fastboot", "getvar", "slot-count"], capture_output=True, text=True)
    if "slot-count: 2" in proc.stdout or "slot-count: 2" in proc.stderr:
        slot_arg = ["--slot", "all"]
        print("[INFO] A/B device detected - vbmeta will be flashed to BOTH slots.")
    else:
        print("[INFO] Single-slot device - flashing without --slot.")

    # Advertencias de confirmación completas
    print("\n=======================================================")
    print("  WARNING: THE NEXT STEPS ARE IRREVERSIBLE")
    print("=======================================================")
    print("  - AVB / Verified Boot will be disabled on this device")
    print("  - The metadata partition will be erased")
    print("  - ALL user data will be wiped (fastboot -w)")
    print()
    print("  Double-check the device serial listed above is correct.")
    print("  Back up anything you need BEFORE continuing.")
    print("  The bootloader must already be OEM-unlocked.")
    print("=======================================================")

    try:
        confirm = input("Type YES to continue, anything else to abort: ").strip().upper()
    except KeyboardInterrupt:
        print("\nAborted. Nothing was flashed or erased.")
        return

    if confirm != "YES":
        print("\nAborted. Nothing was flashed or erased.")
        return

    # Flasheo Core
    print(f"\n[2/6] Flashing {IMG_NAME} to vbmeta (required)...")
    res = subprocess.run(["fastboot"] + slot_arg + ["flash", "vbmeta", IMG_NAME])
    if res.returncode != 0:
        print("[ERROR] Flashing vbmeta failed - stopping here on purpose,")
        print("so metadata/userdata are NOT touched on a half-patched device.")
        sys.exit(1)

    print(f"[3/6] Flashing {IMG_NAME} to vbmeta_system (optional)...")
    res = subprocess.run(["fastboot"] + slot_arg + ["flash", "vbmeta_system", IMG_NAME],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode != 0:
        print("[INFO] vbmeta_system not present on this device - skipped.")

    print(f"[4/6] Flashing {IMG_NAME} to vbmeta_vendor (optional)...")
    res = subprocess.run(["fastboot"] + slot_arg + ["flash", "vbmeta_vendor", IMG_NAME],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode != 0:
        print("[INFO] vbmeta_vendor not present on this device - skipped.")
    print()

    # Erase metadata
    print("[5/6] Erasing metadata partition...")
    meta_res = subprocess.run(["fastboot", "erase", "metadata"],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if meta_res.returncode != 0:
        meta_res2 = subprocess.run(["fastboot", "format:ext4", "metadata"],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if meta_res2.returncode != 0:
            print("[INFO] metadata partition not present or not erasable - skipped.")

    # Wiping userdata (Visibilidad total)
    print("[6/6] Wiping userdata (fastboot -w)...")
    wipe_res = subprocess.run(["fastboot", "-w"])
    if wipe_res.returncode != 0:
        print("[INFO] fastboot -w reported an error - wipe manually from recovery if needed.")

    # Llamada al Bonus del Root Helper antes del reboot
    check_and_flash_boot(slot_arg)

    print("\n=======================================================")
    print("  DONE")
    print("=======================================================")
    print("vbmeta patched (verification disabled) and flashed.")
    print("Rebooting device now.")
    print("You can now flash a patched boot image (Magisk/APatch).")
    subprocess.run(["fastboot", "reboot"])


if __name__ == "__main__":
    check_dependencies()
    build_patched_image()
    flash_device()
