#!/usr/bin/env python3
"""
Universal MTK VBMeta Patcher & Root Helper
===========================================
Builds a vbmeta image with AVB (Android Verified Boot) verification
disabled, flashes it to a MediaTek device over fastboot, wipes the
metadata/userdata partitions, and optionally flashes a pre-patched
boot.img (e.g. patched with Magisk/APatch) to finish rooting.

Requirements:
  - Bootloader already OEM-unlocked
  - fastboot on PATH (Android Platform Tools)
  - avbtool.py (AOSP tool) present in this folder

WARNING: this performs irreversible, destructive actions on the
connected device (disables verified boot, wipes userdata). Read every
prompt before confirming.
"""

import ctypes
import os
import shutil
import subprocess
import sys

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------
IMG_NAME = "vbmeta_mod.img"
AVB_SCRIPT = "avbtool.py"
LOG_FILE = "avbtool_log.txt"
BOOT_IMG_NAME = "boot.img"
TOTAL_STEPS = 6


# ------------------------------------------------------------------
# Console helpers (colors degrade silently if unsupported)
# ------------------------------------------------------------------
class Color:
    RED = GREEN = YELLOW = CYAN = RESET = ""


def enable_colors():
    """Best-effort ANSI color support. Never raises."""
    try:
        if os.name == "nt":
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            mode = ctypes.c_uint32()
            if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                return
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)  # VT processing
        elif not sys.stdout.isatty():
            return
        Color.RED, Color.GREEN, Color.YELLOW, Color.CYAN, Color.RESET = (
            "\033[91m", "\033[92m", "\033[93m", "\033[96m", "\033[0m"
        )
    except Exception:
        pass


def step(n, msg):
    print(f"[{n}/{TOTAL_STEPS}] {msg}")


def ok(msg):
    print(f"{Color.GREEN}[OK]{Color.RESET} {msg}")


def info(msg):
    print(f"{Color.CYAN}[INFO]{Color.RESET} {msg}")


def success(msg):
    print(f"{Color.GREEN}[SUCCESS]{Color.RESET} {msg}")


def warn(msg):
    print(f"{Color.YELLOW}[WARN]{Color.RESET} {msg}")


def error(msg):
    print(f"{Color.RED}[ERROR]{Color.RESET} {msg}")


def ask_yes(prompt):
    """Case-insensitive confirmation. Returns True only for 'yes'."""
    try:
        return input(prompt).strip().upper() == "YES"
    except (KeyboardInterrupt, EOFError):
        print()
        return False


# ------------------------------------------------------------------
# Steps
# ------------------------------------------------------------------
def check_dependencies():
    step(0, "Checking dependencies...")

    if shutil.which("fastboot") is None:
        error("'fastboot' was not found on PATH. Install Android Platform Tools.")
        sys.exit(1)

    if not os.path.exists(AVB_SCRIPT):
        error(f"'{AVB_SCRIPT}' not found in: {os.getcwd()}")
        sys.exit(1)

    ok(f"fastboot and {AVB_SCRIPT} found.\n")


def build_patched_image():
    if os.path.exists(IMG_NAME):
        try:
            os.remove(IMG_NAME)
        except OSError as exc:
            error(f"Could not remove old {IMG_NAME}: {exc}")
            error("Close any program that might have it open and retry.")
            sys.exit(1)

    step(1, f"Building {IMG_NAME} (4KB padding, flags=2 = verification disabled)...")

    cmd = [sys.executable, AVB_SCRIPT, "make_vbmeta_image",
           "--flags", "2", "--padding_size", "4096", "--output", IMG_NAME]

    with open(LOG_FILE, "w") as log:
        result = subprocess.run(cmd, stdout=log, stderr=log)

    if result.returncode != 0 or not os.path.exists(IMG_NAME):
        log_text = ""
        print()
        error("avbtool failed to generate the image. Output:")
        print("-" * 51)
        try:
            with open(LOG_FILE, "r") as log:
                log_text = log.read()
                print(log_text)
        except OSError:
            pass
        print("-" * 51)
        if "ModuleNotFoundError" in log_text or "ImportError" in log_text:
            warn("avbtool needs a Python package that isn't installed.")
            warn("Try: pip install cryptography")
        sys.exit(1)

    success(f"{IMG_NAME} generated.\n")


def detect_slot_arg():
    proc = subprocess.run(["fastboot", "getvar", "slot-count"], capture_output=True, text=True)
    if "slot-count: 2" in proc.stdout or "slot-count: 2" in proc.stderr:
        info("A/B device detected - vbmeta will be flashed to BOTH slots.")
        return ["--slot", "all"]
    info("Single-slot device - flashing without --slot.")
    return []


def flash_optional_partition(step_n, partition, slot_arg):
    step(step_n, f"Flashing {IMG_NAME} to {partition} (optional)...")
    res = subprocess.run(["fastboot"] + slot_arg + ["flash", partition, IMG_NAME],
                          capture_output=True, text=True)
    if res.returncode != 0:
        info(f"{partition} not present on this device - skipped.")
        with open(LOG_FILE, "a") as log:
            log.write(f"\n--- flash {partition} (non-fatal) ---\n{res.stdout}\n{res.stderr}\n")


def erase_metadata():
    step(5, "Erasing metadata partition...")
    res = subprocess.run(["fastboot", "erase", "metadata"], capture_output=True, text=True)
    if res.returncode != 0:
        with open(LOG_FILE, "a") as log:
            log.write(f"\n--- erase metadata (non-fatal) ---\n{res.stdout}\n{res.stderr}\n")
        res2 = subprocess.run(["fastboot", "format:ext4", "metadata"], capture_output=True, text=True)
        if res2.returncode != 0:
            with open(LOG_FILE, "a") as log:
                log.write(f"\n--- format:ext4 metadata (non-fatal) ---\n{res2.stdout}\n{res2.stderr}\n")
            info("metadata partition not present or not erasable - skipped.")


def wipe_userdata():
    step(6, "Wiping userdata (fastboot -w)...")
    res = subprocess.run(["fastboot", "-w"])
    if res.returncode != 0:
        info("fastboot -w reported an error - wipe manually from recovery if needed.")


def check_and_flash_boot(slot_arg):
    """Bonus: offer to flash a pre-patched boot.img (Magisk/APatch) to finish root.

    Returns one of: 'flashed', 'failed', 'skipped', 'not_found'.
    """
    if not os.path.exists(BOOT_IMG_NAME):
        return "not_found"

    print("\n=======================================================")
    print("  [BONUS] PATCHED BOOT IMAGE DETECTED")
    print("=======================================================")
    print(f"A '{BOOT_IMG_NAME}' file was found in this folder.")
    print("This tool can flash it automatically to complete root.")
    print("=======================================================")

    if not ask_yes("Type YES to flash boot.img now, or press ENTER to skip: "):
        info("Flashing boot.img skipped by the user.")
        return "skipped"

    print("\n[BOOT-PATCH] Flashing boot.img to boot partition...")
    res = subprocess.run(["fastboot"] + slot_arg + ["flash", "boot", BOOT_IMG_NAME])
    if res.returncode != 0:
        error("Failed to flash boot.img. Check device connection.")
        return "failed"

    success("boot.img successfully flashed.")
    return "flashed"


def print_summary(boot_status):
    print("\n=======================================================")
    print("  DONE")
    print("=======================================================")
    print("vbmeta patched (verification disabled) and flashed.")
    if boot_status == "flashed":
        print("boot.img was flashed - root should be active after reboot.")
    elif boot_status == "failed":
        print("boot.img flashing failed - once the device is back in")
        print("fastboot mode, retry manually: fastboot flash boot boot.img")
    elif boot_status == "skipped":
        print("boot.img was found but not flashed. Flash it manually when")
        print("ready: fastboot flash boot boot.img")
    else:
        print("Place a patched boot.img (Magisk/APatch) next to this tool")
        print("and flash it to finish rooting: fastboot flash boot boot.img")
    print("Rebooting device now.")
    print("=======================================================")


def flash_device():
    print("=======================================================")
    print("  WAITING FOR DEVICE IN FASTBOOT MODE")
    print("=======================================================")
    print("Connect your MediaTek device in FASTBOOT mode now...")

    subprocess.run(["fastboot", "wait-for-device"])
    success("Device detected. Connected devices:")
    subprocess.run(["fastboot", "devices"])
    print()

    slot_arg = detect_slot_arg()

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

    if not ask_yes("Type YES to continue, anything else to abort: "):
        print("\nAborted. Nothing was flashed or erased.")
        return

    step(2, f"Flashing {IMG_NAME} to vbmeta (required)...")
    res = subprocess.run(["fastboot"] + slot_arg + ["flash", "vbmeta", IMG_NAME])
    if res.returncode != 0:
        error("Flashing vbmeta failed - stopping here on purpose,")
        print("so metadata/userdata are NOT touched on a half-patched device.")
        sys.exit(1)

    flash_optional_partition(3, "vbmeta_system", slot_arg)
    flash_optional_partition(4, "vbmeta_vendor", slot_arg)
    print()

    erase_metadata()
    wipe_userdata()

    boot_status = check_and_flash_boot(slot_arg)
    print_summary(boot_status)
    subprocess.run(["fastboot", "reboot"])


def main():
    enable_colors()
    check_dependencies()
    build_patched_image()
    flash_device()


if __name__ == "__main__":
    try:
        main()
    finally:
        # Keep the console window open on Windows if launched by double-click,
        # including on early exits/errors so the message is readable.
        if os.name == "nt":
            try:
                input("\nPress ENTER to exit...")
            except (KeyboardInterrupt, EOFError):
                pass
