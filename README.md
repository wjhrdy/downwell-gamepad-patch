# Downwell Gamepad Patch

Add comprehensive gamepad/controller support to the Downwell Android game.

## Overview

This patch adds full gamepad controller support to Downwell, allowing you to play with Xbox, PlayStation, or other compatible controllers on Android devices. The patch converts controller inputs into touch events that the game can understand.

**⚠️ Screen Size Compatibility Note:**
This patch was specifically designed and tested for the **480x800 screen resolution** on the **[Magicx Zero 40](https://shop.magicx.team/products/magicx-zero-40)** device. The touch coordinates are hardcoded for this screen size. While the patch may work on other devices, button positions might not align correctly on different screen resolutions.

**🤝 Contributions Welcome:**
We would appreciate contributions to make this patch work across different screen sizes! If you'd like to help improve device compatibility, please consider contributing dynamic screen size detection and coordinate scaling.

## Features

**Controller Support:**
- **D-pad:** Left/Right movement, Up→Left, Down→Right
- **Face buttons (A,B,X,Y):** Jump
- **Shoulder buttons (L1,L2):** Left movement  
- **Shoulder buttons (R1,R2):** Right movement

**Technical Details:**
- Uses exact diff patching to preserve bytecode integrity
- No bytecode verification errors
- Works with Android 10.0+ devices
- Maintains original game performance

## Requirements

- **Python 3.x** installed on your system
- **apktool** for APK decompilation/compilation
- **Java JDK** for APK signing (keytool, jarsigner)
- **ADB** for device installation (optional)
- **Original Downwell APK** file

## Installation

### 1. Install Dependencies

**macOS (with Homebrew):**
```bash
brew install apktool
brew install --cask temurin
```

**Windows:**
- Download apktool from https://ibotpeaches.github.io/Apktool/
- Install Temurin from https://adoptium.net/installation

**Linux (Ubuntu/Debian):**
```bash
sudo apt install apktool default-jdk
```

### 2. Get Original APK

You need the original Downwell APK file. This patch was designed for:

**Target APK Version:**
- **File:** `Downwell_v1.1.11001001_optimized_sign1.apk`
- **MD5:** `8c8c56037b764a9ea9806e29af582ac8`
- **Version:** 1.1.11001001

This can be obtained from:
- Google Play Store (using APK extractors)
- Your existing Downwell installation
- APK download sites (ensure MD5 matches for compatibility)

### 3. Apply Patch

Run the patcher script:
```bash
python3 apply_diff_patch.py input.apk output.apk
```

**Example:**
```bash
python3 apply_diff_patch.py Downwell_v1.1.11001001.apk Downwell_Gamepad.apk
```

### 4. Install on Device

**Via ADB:**
```bash
adb install Downwell_Gamepad.apk
```

**Via File Manager:**
- Copy the patched APK to your device
- Enable "Unknown Sources" in Settings > Security
- Install the APK file

## Usage

1. **Connect Controller:** Pair your gamepad with your Android device via Bluetooth
2. **Launch Game:** Start the patched Downwell app
3. **Play:** Use controller inputs as described in Features section

## How It Works

The patch modifies the `GamepadHandler_API12.smali` file to:

1. **Intercept controller inputs** before normal processing
2. **Convert to touch events** at specific screen coordinates
3. **Handle button conflicts** (e.g., cancel left when right is pressed)
4. **Maintain game compatibility** with original touch controls

## Files

- `apply_diff_patch.py` - Main patcher script
- `gamepad_handler_diff.patch` - Unified diff patch file
- `README.md` - This documentation

## Troubleshooting

**"apktool command not found":**
- Install apktool following the installation instructions above

**"keytool command not found":**
- Install Java JDK following the installation instructions above

**"Patch failed to apply":**
- Ensure you're using the original, unmodified Downwell APK
- Check that the APK version matches the patch expectations
- Verify MD5 hash matches: `8c8c56037b764a9ea9806e29af582ac8`

**"App won't install":**
- Uninstall existing Downwell app first: `adb uninstall com.devolver.downwell_rerelease`
- Enable "Unknown Sources" in device settings

**"Controller not working":**
- Ensure controller is properly paired and connected
- Test controller with other apps to verify it's working
- Some controllers may need additional mapping software

**"Buttons not responsive/misaligned":**
- This patch was designed for 480x800 screen resolution (Magicx Zero 40)
- Different screen sizes may have misaligned touch coordinates
- Try adjusting your device's display settings or scaling
- Consider contributing dynamic screen size support

## Technical Notes

- The patch preserves original bytecode structure to avoid verification errors
- Uses reference counting for directional inputs to handle multiple sources
- Implements priority logic to prevent conflicting movement commands
- Touch events use specific pointer IDs to avoid conflicts with finger touches
- **Screen size dependency:** Touch coordinates are hardcoded for 480x800 resolution
- **Potential improvements:** Dynamic coordinate scaling based on device screen size

## License

This patch is for educational and personal use only. Downwell is owned by Ojiro Fumoto and published by Devolver Digital.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Verify all dependencies are correctly installed
3. Ensure you're using a compatible APK version