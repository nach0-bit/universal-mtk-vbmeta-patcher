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
1. Clone this repository or download the latest **v3.1.0** release.
2. Extract the files to a local directory.
3. *(Optional)* Place your patched `boot.img` (via APatch or Magisk) in the same folder if you want the tool to flash root automatically.
4. Connect your device to your PC and boot into **Fastboot / Bootloader mode**.
5. Run the universal Python script:
   ```bash
   python mtk_vbmeta_patcher.py
   
---
   
## ⚠️ Disclaimer

**USE AT YOUR OWN RISK.** 

Modifying device partitions, disabling Android Verified Boot (AVB), and rooting carry inherent risks. While this tool is heavily tested and designed to be as safe as possible, every device and firmware version is different. 

* **The authors and contributors of this project are NOT responsible** for bricked devices, dead SD cards, lost data, bootloops, voided warranties, or thermonuclear war. 
* Please ensure you understand what `fastboot` and `vbmeta` do before using this script. 
* **Always have a backup** of your stock firmware (scatter file/ROM) ready to flash via SP Flash Tool or Fastboot in case something goes wrong. 

By using this tool, you acknowledge that you are solely responsible for any modifications made to your device.

---

## 📄 License

This project is open-source and distributed under the **MIT License**.

```text
MIT License

Copyright (c) 2026 nach0-bit

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
