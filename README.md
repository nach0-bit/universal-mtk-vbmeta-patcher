# Universal MTK VBMeta Patcher 🛠️

[![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)]()
[![Telegram](https://img.shields.io/badge/Telegram-Join%20Group-2CA5E0?style=flat&logo=telegram)](https://t.me/VbmetaUniversalMTK)

An open-source, automated script designed to streamline the process of disabling **Android Verified Boot (AVB)** on modern **MediaTek (MTK)** devices. 

This tool prepares your device for rooting (APatch, Magisk) or flashing Custom ROMs/GSIs without facing bootloops caused by verified boot restrictions. Built around Google's official `avbtool`, it safely patches the partition to ensure a smooth modding experience.

---

## 🚀 Features
* **Automated Patching:** Bypasses AVB seamlessly without manual hex editing.
* **APatch & Magisk Ready:** Perfect for modern root solutions.
* **Powered by Google's avbtool:** Built on reliable, official foundations.
* **MTK Optimized:** Specially tailored for MediaTek storage layouts and partition structures.
* **Clear Logging:** Terminal outputs let you know exactly what the script is doing.

## 📦 Requirements
* **Unlocked Bootloader** (Critical!)
* Python 3.x installed on your system.
* Basic ADB & Fastboot drivers installed.
* Your stock `vbmeta.img` extracted from your device's firmware.

## 🛠️ Usage
1. Clone this repository or download the latest **v3.0.0** release.
2. Extract the files to a local directory.
3. Place your stock `vbmeta.img` in the designated input folder.
4. Run the script:
   ```bash
   python patcher.py
   ```
5. Follow the on-screen instructions. The script will generate a patched file.
6. Reboot your device to fastboot/bootloader and flash the patched image:
   ```bash
   fastboot flash vbmeta vbmeta_patched.img --disable-verity --disable-verification
   ```
7. Reboot and enjoy!

## 💬 Community & Support
Need help, want to report a bug, or just want to chat with other MTK modders? Join our official Telegram community!

👉 [**Join Universal MTK VBMeta on Telegram**](https://t.me/VbmetaUniversalMTK)

## ⚠️ Disclaimer
***Your warranty is now void.***
*I am not responsible for bricked devices, dead SD cards, thermonuclear war, or you getting fired because the alarm app failed. Please do some research if you have any concerns about features included in this tool before using it. YOU are choosing to make these modifications.*

---
**Developed with 💻 by N.dev ([nachit08899](https://github.com/nachit08899))**
