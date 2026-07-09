 # Universal MTK VBMeta Patcher & Root Helper

An open-source, highly automated tool suite designed to seamlessly disable **Android Verified Boot (AVB)** and assist with root deployment on modern MediaTek (MTK) devices. 

To provide the most optimal user experience, this repository offers two native implementation flavors:
1. **`mtk_vbmeta_patcher.bat`** – A pure, zero-dependency native script optimized for Windows users.
2. **`mtk_vbmeta_patcher.py`** – A clean, robust Python 3 implementation tailored for Linux, macOS, and advanced terminal setups.

---

## 🚀 Key Features

* **Dual-Architecture Deployment:** Choose between a lightweight Windows Batch configuration or a completely cross-platform Python architecture.
* **Dynamic Slot Detection (A/B):** Automatically queries device properties via Fastboot variable tables (`slot-count`) and flashes both active slots simultaneously using `--slot all` when a dual structure is found.
* **[BONUS] Automated Boot Flashing:** Detects if a `boot.img` (stock or Magisk/APatch patched) is present in the working directory and offers a safe, one-click prompt to flash it automatically before rebooting.
* **Granular Crash Prevention:** Evaluates platform critical paths before pushing binaries. Main `vbmeta` failures safely halt execution instantly, shielding crypto blocks and metadata segments from asymmetric half-patched states.
* **Isolated Log Buffering:** Pipe operations output dynamically to `avbtool_log.txt` and echo back real-time dump blocks directly to the console if internal compilers trigger an unhandled fault.

---

## 📋 Requirements

Before executing either patcher variant, ensure the following steps are covered:

1. **Unlocked Bootloader:** Your MediaTek device's bootloader must already be fully OEM-unlocked.
2. **Fastboot Environment:** Android Platform Tools (`fastboot`) must be installed and properly configured inside your system's global environment variables (`PATH`).
3. **Python 3.x:** Installed globally on your machine (required by `avbtool.py` on all systems, and to run the `.py` script on Linux/macOS).
4. **AVB Tool Core:** The target executable `avbtool.py` must be manually placed inside the exact same directory alongside these scripts.

---

## 🛠️ Execution Pipeline (The 6-Step Array)

Both automated tools process the device layout through a structured execution loop:

* **`[0/6]` Dependency Verification:** Scans system binaries for `fastboot` accessibility and localized file states.
* **`[1/6]` Target Image Synthesis:** Automatically patches and builds a custom 4KB aligned `vbmeta_mod.img` file with structural AVB flags hardcoded to value `2` (Verification Overridden).
* **`[2/6]` Core Flash Cycle:** Pushes payload directly into the main `vbmeta` partition block.
* **`[3/6] & [4/6]` Component Override:** Broadly targets peripheral image arrays (`vbmeta_system` and `vbmeta_vendor`) and bypasses them gracefully if non-existent.
* **`[5/6]` Cryptographic Metadata Purge:** Erases block indexes or reformats system `metadata` layouts directly into ext4 maps.
* **`[6/6]` Full Structural Reset:** Triggers an authentic userdata cycle allocation (`fastboot -w`) to finalize data partition un-encryption and triggers an automatic device restart.

---

## 💻 Usage Instructions

### On Windows (Recommended Fast-Track)
1. Drop `avbtool.py` and your optional target `boot.img` inside the script folder.
2. Boot your device into **Fastboot Mode** and link it via USB.
3. Simply double-click **`mtk_vbmeta_patcher.bat`** (No terminal navigation required).

### On Linux / macOS (Or Advanced Windows Shells)
1. Open up your native terminal emulator inside the downloaded repository directory.
2. Set your device into **Fastboot Mode** and verify connectivity.
3. Run the cross-platform script using Python 3:
   ```bash
   python mtk_vbmeta_patcher.py
4.Confirm user checks by passing strict YES validations on screen when prompted.
⚠️ Disclaimer
Warning: This utility executes advanced partitions updates, low-level system wipes, and structural resets (fastboot -w). The software is provided "as-is". I am not responsible for soft-bricks, hardware malfunctions, dead memory blocks, or unexpected user data destruction. Always backup vital user storage units before triggering compilation loops.
🤝 Contributing & Feedback
This project is 100% open-source and powered by the modding community. Pull requests, issue trackers, and hardware validation compatibility reports are always highly encouraged!
If this automated dual-suite saved your MediaTek device from a bootloop or simplified your custom ROM setup, please take a brief second to drop a 🌟 star on the repository to boost project discovery!