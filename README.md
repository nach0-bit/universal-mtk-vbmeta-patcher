# Universal MTK VBMeta Patcher 🛠️

[![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)]()
[![Telegram](https://img.shields.io/badge/Telegram-Join%20Group-2CA5E0?style=flat&logo=telegram)](https://t.me/VbmetaUniversalMTK)

An open-source, fully automated script designed to streamline the process of disabling **Android Verified Boot (AVB)** on modern **MediaTek (MTK)** devices. 

This tool prepares your device for rooting (APatch, Magisk) or flashing Custom ROMs/GSIs without facing bootloops caused by verified boot restrictions. Built around Google's official `avbtool`, it safely patches the partition and **automatically flashes it to your device**, ensuring a seamless modding experience without the need for manual fastboot commands.

---

## 🚀 Features
* **100% Fully Automated:** Patches AND flashes the image for you directly. No manual fastboot commands required!
* **APatch & Magisk Ready:** Perfect for modern root solutions.
* **Powered by Google's avbtool:** Built on reliable, official foundations.
* **MTK Optimized:** Specially tailored for MediaTek storage layouts and partition structures.
* **Clear Logging:** Terminal outputs let you know exactly what the script is doing at every step.

## 📦 Requirements
* **Unlocked Bootloader** (Critical!)
* Basic ADB & Fastboot drivers installed on your PC.
* USB debugging enabled and device connected.
* Your stock `vbmeta.img` extracted from your device's firmware.

## 🛠️ Usage
1. Clone this repository or download the latest **v3.0.0** release.
2. Extract the files to a local directory.
3. Place your stock `vbmeta.img` in the tool's designated folder.
4. Connect your device to your PC in **Fastboot / Bootloader mode**.
5. Run the script (e.g., via terminal or double-clicking the executable):
   ```bash
   python mtk_vbmeta_patcher.py
   ```
6. Sit back and watch! The tool will automatically patch the image and **flash it directly to your phone**.
7. Once finished, reboot your device and enjoy your unlocked system!

## 💬 Community & Support
Need help, want to report a bug, or just want to chat with other MTK modders? Join our official Telegram community!

👉 [**Join Universal MTK VBMeta on Telegram**](https://t.me/VbmetaUniversalMTK)

## ⚠️ Disclaimer
***Your warranty is now void.***
*I am not responsible for bricked devices, dead SD cards, thermonuclear war, or you getting fired because the alarm app failed. Please do some research if you have any concerns about features included in this tool before using it. YOU are choosing to make these modifications.*

---
**Developed with 💻 by N.dev ([nach0-bit](https://github.com/nach0-bit))**

