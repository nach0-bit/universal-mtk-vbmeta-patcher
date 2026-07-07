# Universal MTK VBMeta Patcher & Root Helper

An open-source, automated script designed to streamline the process of disabling Android Verified Boot (AVB) on modern **MediaTek (MTK)** devices. This tool prepares your device for rooting (APatch, Magisk) or flashing GSIs/Custom ROMs without facing bootloops caused by verified boot restrictions.

By utilizing Google's official `avbtool`, the script dynamically compiles a generic blank/modified `vbmeta` image aligned with standard MTK partition sizes (4KB padding) and flashes it across all critical verification points in a single click.

---

## 🚀 Features
* **Universal MTK Compatibility:** Works on almost any modern MediaTek device requiring AVB disabling.
* **Automated Generation:** Uses `avbtool` to dynamically create a `vbmeta_mod.img` with **Flag 2 disabled** and forced **4KB padding** (required by MTK preloaders).
* **Multi-Partition Flashing:** Automatically covers the standard triple-partition verification scheme (`vbmeta`, `vbmeta_system`, and `vbmeta_vendor`).
* **Fail-Safe Checks:** Verifies code compilation before running Fastboot commands to ensure device safety.
* **Automation:** Handles the mandatory post-flash factory reset and metadata wipe seamlessly.

---

## 📋 Prerequisites

1. **Unlocked Bootloader:** Your device's bootloader must be fully unlocked.
2. **Python Installed:** Python 3.x must be installed on your computer and added to your **System PATH**.
3. **USB Drivers:** MediaTek / Fastboot drivers must be properly installed on Windows.

---

## 📂 Repository Structure

Ensure the release folder maintains the following file structure for the automated script to execute correctly:
📂 Universal-MTK-Patcher
 ├── 📄 patcher_vbmeta.bat <- The main execution script
 ├── 📄 avbtool.py         <- Python dependency script
 ├── 📄 fastboot.exe       <- Android platform tool binary
 ├── 📄 AdbWinApi.dll      <- Windows ADB dependency
 └── 📄 AdbWinUsbApi.dll   <- Windows USB dependency

---

## 🛠️ How To Use

1. **Download** the latest release package and extract it to a single directory.
2. Boot your MediaTek phone into **Fastboot Mode** (usually Power + Volume Down) and connect it to your PC.
3. Double-click **`patcher_vbmeta.bat`** to start the automated process.
4. The script will generate the universal image, wait for your device, flash the required partitions, wipe metadata/userdata to prevent encryption bootloops, and reboot.
5. Once your device boots, you can safely proceed to patch your kernel/boot image using **APatch** or **Magisk**.

---

## 🤝 Contributing & Feedback
As this is an open-source tool aiming for universal MTK support, community feedback is highly appreciated. If your specific device requires additional partitions (e.g., `vbmeta_boot`), feel free to fork this repository, submit a pull request, or open an issue.

*Disclaimer: Modifying system partitions carries risks. Always back up your important data before flashing. The developers are not responsible for bricked devices.*
## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
