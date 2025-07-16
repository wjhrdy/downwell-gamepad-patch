#!/usr/bin/env python3
"""
Downwell Gamepad Patcher - Direct Diff Application
Applies the exact gamepad_handler_diff.patch using the patch command
"""

import os
import sys
import subprocess
import tempfile
import shutil

def run_command(cmd, cwd=None):
    """Run a shell command and return output"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Error running command: {cmd}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        return False
    return True

def apply_gamepad_patch(apk_path, output_path):
    """Apply gamepad patch using direct diff application"""
    
    # Create temp directory
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"[+] Using temp directory: {temp_dir}")
        
        # Step 1: Decompile APK
        print(f"[+] Decompiling APK...")
        if not run_command(f"apktool d -f '{apk_path}' -o '{temp_dir}/decompiled'"):
            return False
        
        # Step 2: Copy patch file to temp directory
        patch_file = "gamepad_handler_diff.patch"
        if not os.path.exists(patch_file):
            print(f"[-] Patch file not found: {patch_file}")
            return False
        
        temp_patch = os.path.join(temp_dir, "gamepad_handler_diff.patch")
        shutil.copy2(patch_file, temp_patch)
        
        # Step 3: Apply patch using the patch command
        print(f"[+] Applying gamepad patch...")
        # The patch expects the directory structure to have downwell_orig/smali/...
        # But we have decompiled/smali/..., so we need to create the expected structure
        
        # Create the expected directory structure
        os.makedirs(f"{temp_dir}/downwell_orig/smali/com/devolver/downwell_rerelease", exist_ok=True)
        
        # Copy the target file to the expected location
        source_file = f"{temp_dir}/decompiled/smali/com/devolver/downwell_rerelease/GamepadHandler_API12.smali"
        target_file = f"{temp_dir}/downwell_orig/smali/com/devolver/downwell_rerelease/GamepadHandler_API12.smali"
        
        if not os.path.exists(source_file):
            print(f"[-] Source file not found: {source_file}")
            return False
        
        shutil.copy2(source_file, target_file)
        
        # Apply the patch
        if not run_command(f"patch -p0 < '{temp_patch}'", cwd=temp_dir):
            print("[-] Failed to apply patch")
            return False
        
        # Copy the patched file back
        if os.path.exists(target_file):
            shutil.copy2(target_file, source_file)
            print("[+] Patch applied successfully")
        else:
            print("[-] Patched file not found")
            return False
        
        # Step 4: Rebuild APK
        print(f"[+] Rebuilding APK...")
        if not run_command(f"apktool b '{temp_dir}/decompiled' -o '{output_path}'"):
            return False
        
        # Step 5: Sign APK
        print(f"[+] Signing APK...")
        keystore_path = os.path.join(os.path.dirname(output_path), "gamepad-keystore.jks")
        
        if not os.path.exists(keystore_path):
            print("[+] Creating keystore...")
            if not run_command(f"keytool -genkey -v -keystore '{keystore_path}' -alias gamepad -keyalg RSA -keysize 2048 -validity 10000 -storepass gamepad123 -keypass gamepad123 -dname 'CN=Gamepad, OU=Gamepad, O=Gamepad, L=Gamepad, S=Gamepad, C=US'"):
                return False
        
        if not run_command(f"jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore '{keystore_path}' -storepass gamepad123 -keypass gamepad123 '{output_path}' gamepad"):
            return False
        
        print(f"[+] Success! Gamepad patch applied to: {output_path}")
        print(f"[+] Controller support added:")
        print(f"    • D-pad: Left/Right movement, Up→Left, Down→Right")
        print(f"    • Face buttons (A,B,X,Y): Jump")
        print(f"    • Shoulder buttons (L1,L2): Left movement")
        print(f"    • Shoulder buttons (R1,R2): Right movement")
        
        return True

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python apply_diff_patch.py <input.apk> <output.apk>")
        print("Example: python apply_diff_patch.py Downwell.apk Downwell_Gamepad.apk")
        sys.exit(1)
    
    input_apk = sys.argv[1]
    output_apk = sys.argv[2]
    
    if not os.path.exists(input_apk):
        print(f"Error: Input APK not found: {input_apk}")
        sys.exit(1)
    
    if apply_gamepad_patch(input_apk, output_apk):
        print(f"\n✅ Successfully created: {output_apk}")
        print(f"📱 Install with: adb install {output_apk}")
    else:
        print(f"\n❌ Failed to apply patch")
        sys.exit(1)