# Troubleshooting Guide

Comprehensive troubleshooting guide for the Face Recognition System.

## Table of Contents
- [Quick Diagnostics](#quick-diagnostics)
- [Installation Issues](#installation-issues)
- [Camera Problems](#camera-problems)
- [Recognition Issues](#recognition-issues)
- [Excel Operations Issues](#excel-operations-issues)
- [Performance Problems](#performance-problems)
- [File and Permission Issues](#file-and-permission-issues)
- [Error Messages](#error-messages)
- [Recovery Procedures](#recovery-procedures)

## Quick Diagnostics

### System Health Check
Run this diagnostic script to quickly identify common issues:

```python
# diagnostic.py
import cv2
import os
import json
import sys

def run_diagnostics():
    print("=== Face Recognition System Diagnostics ===\n")
    
    # Check Python version
    print(f"Python version: {sys.version}")
    if sys.version_info < (3, 7):
        print("❌ Warning: Python 3.7+ recommended")
    else:
        print("✅ Python version OK")
    
    # Check dependencies
    dependencies = ['cv2', 'face_recognition', 'openpyxl', 'numpy', 'pandas']
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep} installed")
        except ImportError:
            print(f"❌ {dep} missing")
    
    # Check camera
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print("✅ Camera accessible")
        cap.release()
    else:
        print("❌ Camera not accessible")
    
    # Check directories
    directories = ['data', 'backup', 'docs']
    for directory in directories:
        if os.path.exists(directory):
            print(f"✅ {directory}/ directory exists")
        else:
            print(f"❌ {directory}/ directory missing")
    
    # Check config file
    if os.path.exists('config.json'):
        try:
            with open('config.json', 'r') as f:
                json.load(f)
            print("✅ config.json valid")
        except json.JSONDecodeError:
            print("❌ config.json corrupted")
    else:
        print("⚠️ config.json missing (will be created)")
    
    print("\n=== Diagnostics Complete ===")

if __name__ == "__main__":
    run_diagnostics()
```

### Quick Fixes Checklist
Before diving into detailed troubleshooting:

- [ ] Restart the application
- [ ] Check camera is not used by other applications
- [ ] Ensure Excel files are not open in other programs
- [ ] Verify write permissions to project directory
- [ ] Check available disk space
- [ ] Update dependencies: `pip install --upgrade opencv-python face-recognition openpyxl`

## Installation Issues

### Dependency Installation Failures

#### Problem: face_recognition fails to install
```
ERROR: Failed building wheel for dlib
```

**Solutions**:
```bash
# Solution 1: Update pip and setuptools
pip install --upgrade pip setuptools wheel

# Solution 2: Install Visual C++ Build Tools (Windows)
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Solution 3: Use conda instead of pip
conda install -c conda-forge dlib
conda install -c conda-forge face_recognition

# Solution 4: Install pre-compiled wheel
pip install https://github.com/ageitgey/face_recognition/releases/latest/download/face_recognition-1.3.0-py2.py3-none-any.whl
```

#### Problem: OpenCV installation issues
```
ImportError: No module named 'cv2'
```

**Solutions**:
```bash
# Uninstall all OpenCV packages
pip uninstall opencv-python opencv-contrib-python opencv-python-headless

# Reinstall specific version
pip install opencv-python==4.5.5.64

# Alternative: Install headless version
pip install opencv-python-headless
```

#### Problem: openpyxl import errors
```
ImportError: No module named 'openpyxl'
```

**Solutions**:
```bash
# Install openpyxl
pip install openpyxl

# If still failing, install dependencies
pip install et_xmlfile jdcal
```

### Platform-Specific Issues

#### Windows
**Problem**: Permission denied errors
```bash
# Run as Administrator
# Or install for user only
pip install --user opencv-python face-recognition openpyxl
```

**Problem**: Camera access denied
- Check Windows Privacy Settings → Camera
- Allow desktop apps to access camera
- Ensure antivirus isn't blocking camera access

#### Linux
**Problem**: Missing system dependencies
```bash
sudo apt-get update
sudo apt-get install python3-dev cmake libopenblas-dev liblapack-dev
sudo apt-get install libx11-dev libgtk-3-dev
```

**Problem**: Camera permission issues
```bash
# Add user to video group
sudo usermod -a -G video $USER

# Check camera devices
ls -la /dev/video*

# Test camera access
v4l2-ctl --list-devices
```

#### macOS
**Problem**: Camera permission denied
- System Preferences → Security & Privacy → Camera
- Grant permission to Terminal/Python

**Problem**: Missing build tools
```bash
# Install Xcode command line tools
xcode-select --install

# Install Homebrew dependencies
brew install cmake
```

## Camera Problems

### Camera Not Detected

#### Problem: "Camera not accessible" error

**Diagnostic Steps**:
```python
import cv2

# Test different camera indices
for i in range(10):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera {i}: Available")
        cap.release()
    else:
        print(f"Camera {i}: Not available")
```

**Solutions**:
1. **Check camera connections**
   - USB cameras: Try different USB ports
   - Built-in cameras: Ensure drivers are installed

2. **Update camera drivers**
   - Device Manager → Cameras → Update driver

3. **Change camera index in config**
   ```json
   {
       "camera_index": 1  // Try different values: 0, 1, 2...
   }
   ```

4. **Close other camera applications**
   - Check if Skype, Teams, or other apps are using camera
   - Close all camera applications before running system

### Camera Quality Issues

#### Problem: Poor image quality, blurry images

**Solutions**:
1. **Adjust camera settings**
   ```python
   # In camera.py, add these settings
   cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
   cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
   cap.set(cv2.CAP_PROP_BRIGHTNESS, 50)
   ```

2. **Improve lighting conditions**
   - Ensure adequate lighting on face
   - Avoid backlighting
   - Use consistent lighting for registration and recognition

3. **Clean camera lens**
   - Physical cleaning of camera lens
   - Check for obstructions

### Camera Freezing/Hanging

#### Problem: Camera feed freezes or application hangs

**Solutions**:
1. **Add timeout handling**
   ```python
   import cv2
   import time
   
   cap = cv2.VideoCapture(0)
   cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer
   
   start_time = time.time()
   while True:
       ret, frame = cap.read()
       if not ret:
           if time.time() - start_time > 5:  # 5 second timeout
               print("Camera timeout")
               break
       # Process frame
   ```

2. **Restart camera connection**
   ```python
   def restart_camera(self):
       if hasattr(self, 'cam'):
           self.cam.release()
       time.sleep(1)
       self.cam = cv2.VideoCapture(self.camera_index)
   ```

3. **Check USB power management**
   - Disable USB selective suspend (Windows)
   - Use powered USB hubs for external cameras

## Recognition Issues

### Users Not Being Recognized

#### Problem: Registered users not recognized

**Diagnostic Steps**:
1. **Check if user data exists**
   ```
   Main Menu → Option 4 → Check if User Data exist
   ```

2. **Verify confidence settings**
   ```
   Main Menu → Option 5 → Configure Confidence Levels
   ```

3. **Test with different confidence levels**
   - Start with higher values (60-70%)
   - Gradually decrease until recognition works

**Solutions**:
1. **Lower recognition confidence**
   ```json
   {
       "confidence_match": 0.6  // Increase from default 0.4
   }
   ```

2. **Re-register problematic users**
   - Use better lighting conditions
   - Register multiple angles
   - Ensure clear, front-facing photos

3. **Check face encoding quality**
   ```python
   # Verify face encoding exists and is valid
   import numpy as np
   
   try:
       encoding = np.load("data/John_Doe_001_0.npy")
       print(f"Encoding shape: {encoding.shape}")
       print(f"Encoding valid: {encoding.size > 0}")
   except Exception as e:
       print(f"Error loading encoding: {e}")
   ```

### False Positive Recognition

#### Problem: Wrong users being recognized

**Solutions**:
1. **Increase recognition strictness**
   ```json
   {
       "confidence_match": 0.2  // Decrease from default 0.4
   }
   ```

2. **Improve registration quality**
   - Use high-quality, clear photos
   - Ensure consistent lighting
   - Register multiple photos per person

3. **Check for duplicate registrations**
   - Review data directory for duplicate files
   - Remove conflicting face encodings

### No Face Detected

#### Problem: "No face detected in image" error

**Solutions**:
1. **Improve image quality**
   - Ensure face is clearly visible
   - Use adequate lighting
   - Face should occupy significant portion of image

2. **Adjust face detection model**
   ```json
   {
       "face_detection_model": "cnn"  // More accurate but slower
   }
   ```

3. **Check image format**
   - Use supported formats: JPG, PNG, BMP
   - Ensure image is not corrupted

## Excel Operations Issues

### Excel File Access Problems

#### Problem: "Permission denied" when accessing Excel file

**Solutions**:
1. **Close Excel application**
   - Ensure data.xlsx is not open in Excel
   - Close all Excel instances

2. **Check file permissions**
   ```bash
   # Windows
   icacls data.xlsx /grant Users:F
   
   # Linux/macOS
   chmod 666 data/data.xlsx
   ```

3. **Use different Excel file location**
   ```bash
   python run.py "C:/temp/attendance.xlsx"
   ```

#### Problem: Excel file corruption

**Solutions**:
1. **Restore from backup**
   ```
   backup/backup_YYYYMMDD_HHMMSS/data.xlsx
   ```

2. **Create new Excel file**
   - Delete corrupted data.xlsx
   - System will create new file automatically

3. **Repair Excel file**
   - Open in Excel → File → Info → Check for Issues

### Excel Data Issues

#### Problem: Incorrect data in Excel file

**Solutions**:
1. **Check column mapping**
   ```python
   # Verify Excel structure
   import openpyxl
   
   wb = openpyxl.load_workbook("data/data.xlsx")
   ws = wb.active
   
   # Check headers
   for col in range(1, 10):
       cell_value = ws.cell(row=1, column=col).value
       print(f"Column {col}: {cell_value}")
   ```

2. **Rebuild Excel file**
   - Backup current data
   - Delete data.xlsx
   - Re-run application to create fresh file

#### Problem: Timestamp formatting issues

**Solutions**:
1. **Check system date/time format**
   - Ensure system date/time is correct
   - Check regional settings

2. **Update Excel datetime handling**
   ```python
   # In excel_handle.py
   from datetime import datetime
   
   # Ensure consistent datetime format
   timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   ```

## Performance Problems

### Slow Recognition Speed

#### Problem: Recognition takes too long

**Solutions**:
1. **Enable fast mode**
   ```json
   {
       "recognition_speed": {
           "skip_frames": 3,
           "resize_factor": 0.5,
           "fast_mode": true
       }
   }
   ```

2. **Reduce face detection frequency**
   ```json
   {
       "detection_frequency": 10  // Process every 10th frame
   }
   ```

3. **Use HOG model instead of CNN**
   ```json
   {
       "face_detection_model": "hog"
   }
   ```

4. **Enable multithreading**
   ```json
   {
       "enable_multithreading": true,
       "max_threads": 4
   }
   ```

### High Memory Usage

#### Problem: Application uses too much memory

**Solutions**:
1. **Enable memory management**
   ```json
   {
       "memory_settings": {
           "cache_encodings": true,
           "max_cache_size": 500,
           "garbage_collection": true
       }
   }
   ```

2. **Restart application periodically**
   - Schedule regular restarts for long-running systems

3. **Monitor memory usage**
   ```python
   import psutil
   import os
   
   process = psutil.Process(os.getpid())
   memory_usage = process.memory_info().rss / 1024 / 1024  # MB
   print(f"Memory usage: {memory_usage:.2f} MB")
   ```

### CPU Usage Issues

#### Problem: High CPU usage

**Solutions**:
1. **Optimize frame processing**
   - Reduce camera FPS
   - Skip frames during processing
   - Lower camera resolution

2. **Adjust processing parameters**
   ```json
   {
       "camera_fps": 15,
       "recognition_speed": {
           "skip_frames": 5,
           "resize_factor": 0.25
       }
   }
   ```

## File and Permission Issues

### Data Directory Problems

#### Problem: "Cannot create data directory" error

**Solutions**:
1. **Check write permissions**
   ```bash
   # Windows
   mkdir data
   echo test > data\test.txt
   
   # Linux/macOS
   mkdir -p data
   touch data/test.txt
   ```

2. **Run with elevated permissions**
   - Run command prompt as Administrator (Windows)
   - Use sudo if necessary (Linux/macOS)

3. **Change data directory location**
   ```json
   {
       "data_directory": "C:/Users/Username/Documents/FaceRecognition/data"
   }
   ```

### Backup Issues

#### Problem: Backup creation fails

**Solutions**:
1. **Check backup directory permissions**
   ```bash
   # Create backup directory manually
   mkdir backup
   ```

2. **Verify disk space**
   ```python
   import shutil
   
   # Check available disk space
   total, used, free = shutil.disk_usage(".")
   print(f"Free space: {free // (2**30)} GB")
   ```

3. **Disable backup temporarily**
   ```json
   {
       "backup_enabled": false
   }
   ```

## Error Messages

### Common Error Messages and Solutions

#### "face_recognition module not found"
```bash
pip install face_recognition
```

#### "No module named 'cv2'"
```bash
pip install opencv-python
```

#### "Permission denied: 'data.xlsx'"
- Close Excel application
- Check file permissions
- Run as administrator

#### "Camera index out of range"
```json
{
    "camera_index": 0  // Try different values
}
```

#### "No face detected in image"
- Improve lighting conditions
- Ensure face is clearly visible
- Use higher resolution image

#### "Configuration file corrupted"
```bash
# Reset configuration
rm config.json
# Restart application to create new config
```

#### "Backup directory not found"
```bash
mkdir backup
```

#### "Excel file format not supported"
- Ensure file has .xlsx extension
- Use Excel 2007+ format

## Recovery Procedures

### Data Recovery

#### Restore from Backup
```python
import shutil
import os
from datetime import datetime

def restore_from_backup(backup_date=None):
    """Restore data from backup"""
    backup_dir = "backup"
    
    if backup_date:
        backup_path = f"{backup_dir}/backup_{backup_date}"
    else:
        # Find latest backup
        backups = [d for d in os.listdir(backup_dir) if d.startswith("backup_")]
        if not backups:
            print("No backups found")
            return False
        
        backup_path = f"{backup_dir}/{sorted(backups)[-1]}"
    
    if not os.path.exists(backup_path):
        print(f"Backup not found: {backup_path}")
        return False
    
    # Restore data directory
    if os.path.exists("data"):
        shutil.rmtree("data")
    
    shutil.copytree(f"{backup_path}/data", "data")
    print(f"Data restored from {backup_path}")
    return True

# Usage
restore_from_backup()  # Restore latest backup
restore_from_backup("20250602_143015")  # Restore specific backup
```

### Configuration Recovery

#### Reset to Default Configuration
```python
import json

def reset_configuration():
    """Reset configuration to defaults"""
    default_config = {
        "confidence_match": 0.4,
        "confidence_save": 0.4,
        "show_confidence": True,
        "camera_index": 0,
        "excel_auto_save": True,
        "backup_enabled": True
    }
    
    with open("config.json", "w") as f:
        json.dump(default_config, f, indent=4)
    
    print("Configuration reset to defaults")

reset_configuration()
```

### System Recovery

#### Complete System Reset
```python
import os
import shutil

def reset_system():
    """Complete system reset (WARNING: Deletes all data)"""
    print("WARNING: This will delete all user data and settings!")
    confirm = input("Type 'RESET' to confirm: ")
    
    if confirm == "RESET":
        # Remove data directory
        if os.path.exists("data"):
            shutil.rmtree("data")
        
        # Reset configuration
        if os.path.exists("config.json"):
            os.remove("config.json")
        
        # Keep backups but can remove if needed
        # if os.path.exists("backup"):
        #     shutil.rmtree("backup")
        
        print("System reset complete. Restart application to initialize.")
    else:
        print("Reset cancelled")

# Use with extreme caution
# reset_system()
```

## Getting Help

### Log Analysis
Enable detailed logging to help diagnose issues:

```json
{
    "logging": {
        "enabled": true,
        "level": "DEBUG",
        "file": "face_recognition.log"
    }
}
```

### Support Information
When seeking help, include:
1. Operating system and version
2. Python version
3. Full error message
4. Steps to reproduce the issue
5. Configuration file contents
6. Diagnostic script output

### Emergency Contacts
- Check documentation: `docs/` folder
- Review error logs: `face_recognition.log`
- Backup data: `backup/` directory
- Configuration: `config.json`

Remember: Most issues can be resolved by checking dependencies, permissions, and configuration settings. Always backup data before making significant changes.
