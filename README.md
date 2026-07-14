# Universal MTK VBMeta Patcher & Root Helper 🛠️

[![Version](https://img.shields.io/badge/version-3.1.0-blue.svg)]()
[![Telegram](https://img.shields.io/badge/Telegram-Join%20Group-2CA5E0?style=flat&logo=telegram)](https://t.me/VbmetaUniversalMTK)

An open-source, fully automated script designed to streamline the process of disabling **Android Verified Boot (AVB)** on modern **MediaTek (MTK)** devices. 

This tool prepares your device for rooting (APatch, Magisk) or flashing Custom ROMs/GSIs without facing bootloops caused by verified boot restrictions. Built around Google's official `avbtool`, it safely builds the custom partition and **automatically flashes it to your device**, wiping necessary metadata and offering to complete your root process automatically.

---

## 🛑 Infrastructure Update: Windows Batch (`.bat`) Deprecated
As of version **3.1.0+**, the legacy `.bat` wrapper has been **officially discontinued**. 
Due to limitations in the Windows command line regarding complex conditional logic, dynamic partition detection, and safe error handling, the project has transitioned entirely to **Python 3**. This ensures a reliable, universal, and enterprise-grade execution across both Windows and GNU/Linux environments.

---

## 🚀 Features
* **100% Fully Automated:** Generates and flashes the AVB-disabled image directly. No manual fastboot commands required!
* **Smart A/B Slot Detection:** Automatically queries your device's architecture and flashes both slots (`--slot all`) if an A/B partition scheme is detected.
* **Deep Wipe Mechanisms:** Safely executes `fastboot erase metadata` (with an automatic `format:ext4` fallback) to prevent MTK dm-verity bootloops.
* **Bonus Root Helper:** Automatically detects a patched `boot.img` (Magisk/APatch) in the folder and offers to flash it for you to finish the root process in one go.
* **Color-Coded UI & Safe Logging:** Terminal outputs let you know exactly what the script is doing step-by-step, generating an `avbtool_log.txt` for easy debugging without cluttering your screen.

## 📦 Requirements
* **Unlocked Bootloader** (Critical!)
* **Python 3** installed on your system.
* Python `cryptography` module (`pip install cryptography`).
* Basic ADB & Fastboot tools added to your system PATH.
* USB debugging enabled and device connected.

## 🛠️ Usage
1. Clone this repository or download the latest **v3.1.2** release.
2. Extract the files to a local directory.
3. *(Optional)* Place your patched `boot.img` (via APatch or Magisk) in the same folder if you want the tool to flash root automatically.
4. Connect your device to your PC and boot into **Fastboot / Bootloader mode**.
5. Run the universal Python script:
   ```bash
   python mtk_vbmeta_patcher.py
   
