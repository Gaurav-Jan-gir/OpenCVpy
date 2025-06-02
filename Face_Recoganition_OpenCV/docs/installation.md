# Installation Guide

## System Requirements

### Operating System
- **Windows 10/11** (Primary support)
- **Linux** (Ubuntu 18.04+, CentOS 7+)
- **macOS** (10.14+)

### Hardware Requirements
- **CPU**: Intel i5 or AMD Ryzen 5 (minimum)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **Camera**: USB webcam or built-in camera
- **GPU**: Optional (CUDA-compatible for acceleration)

## Prerequisites

### Python Installation
```bash
# Check Python version (3.7+ required)
python --version

# If Python not installed, download from:
# https://www.python.org/downloads/
```

### Required Python Version
- **Python 3.7** or higher
- **pip** package manager

## Installation Steps

### 1. Clone or Download the Project
```bash
# If using Git
git clone <repository-url>
cd Face_Recoganition_OpenCV

# Or download and extract the ZIP file
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv face_recognition_env

# Activate virtual environment
# Windows
face_recognition_env\Scripts\activate

# Linux/macOS
source face_recognition_env/bin/activate
```

### 3. Install Dependencies

#### Core Dependencies
```bash
# Install all required packages
pip install opencv-python
pip install face-recognition
pip install openpyxl
pip install numpy
pip install pandas
```

#### Alternative: Install from requirements.txt
Create a `requirements.txt` file with:
```text
opencv-python>=4.5.0
face-recognition>=1.3.0
openpyxl>=3.0.0
numpy>=1.19.0
pandas>=1.3.0
```

Then install:
```bash
pip install -r requirements.txt
```

## Dependency Details

### Core Libraries

#### OpenCV (cv2)
- **Purpose**: Computer vision and image processing
- **Version**: 4.5.0+
- **Installation**: `pip install opencv-python`

#### face_recognition
- **Purpose**: Face detection and encoding
- **Version**: 1.3.0+
- **Installation**: `pip install face-recognition`
- **Note**: Requires dlib (automatically installed)

#### openpyxl
- **Purpose**: Excel file operations
- **Version**: 3.0.0+
- **Installation**: `pip install openpyxl`

#### NumPy
- **Purpose**: Numerical operations and array handling
- **Version**: 1.19.0+
- **Installation**: `pip install numpy`

#### Pandas
- **Purpose**: Data manipulation and backup operations
- **Version**: 1.3.0+
- **Installation**: `pip install pandas`

### System Dependencies

#### Windows
```bash
# Visual C++ Redistributable (for dlib)
# Download from Microsoft official site
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3-dev
sudo apt-get install cmake
sudo apt-get install libopenblas-dev
sudo apt-get install liblapack-dev
sudo apt-get install libx11-dev
sudo apt-get install libgtk-3-dev
```

#### macOS
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install cmake
brew install python3
```

## Verification

### 1. Test Python Installation
```python
# test_installation.py
import sys
print(f"Python version: {sys.version}")

try:
    import cv2
    print(f"OpenCV version: {cv2.__version__}")
except ImportError:
    print("❌ OpenCV not installed")

try:
    import face_recognition
    print("✅ face_recognition installed")
except ImportError:
    print("❌ face_recognition not installed")

try:
    import openpyxl
    print("✅ openpyxl installed")
except ImportError:
    print("❌ openpyxl not installed")

try:
    import numpy as np
    print(f"✅ NumPy version: {np.__version__}")
except ImportError:
    print("❌ NumPy not installed")

try:
    import pandas as pd
    print(f"✅ Pandas version: {pd.__version__}")
except ImportError:
    print("❌ Pandas not installed")
```

### 2. Test Camera Access
```python
# test_camera.py
import cv2

cap = cv2.VideoCapture(0)
if cap.isOpened():
    print("✅ Camera access successful")
    cap.release()
else:
    print("❌ Camera access failed")
```

### 3. Run the Application
```bash
# Navigate to project directory
cd Face_Recoganition_OpenCV

# Run the main application
python run.py
```

## Troubleshooting Installation

### Common Issues

#### 1. face_recognition Installation Fails
```bash
# Solution 1: Update pip and setuptools
pip install --upgrade pip setuptools

# Solution 2: Install with specific flags
pip install --upgrade face_recognition

# Solution 3: Install dlib separately
pip install dlib
pip install face_recognition
```

#### 2. OpenCV Import Error
```bash
# Uninstall all OpenCV packages
pip uninstall opencv-python opencv-contrib-python opencv-python-headless

# Reinstall specific version
pip install opencv-python==4.5.5.64
```

#### 3. Permission Errors (Windows)
```bash
# Run command prompt as Administrator
# Then install packages

# Or use --user flag
pip install --user opencv-python face_recognition openpyxl numpy pandas
```

#### 4. Camera Not Detected
- Check camera permissions in system settings
- Ensure camera is not being used by other applications
- Try different camera indices (0, 1, 2, etc.)

### Platform-Specific Issues

#### Windows
- Install Microsoft Visual C++ 14.0 if dlib fails
- Ensure Windows camera privacy settings allow application access

#### Linux
- Install additional development packages if compilation fails
- Check camera device permissions: `ls -la /dev/video*`

#### macOS
- Grant camera permissions in System Preferences > Security & Privacy
- Install Xcode command line tools: `xcode-select --install`

## Next Steps

After successful installation, proceed to:
1. [Quick Start Guide](./quick-start.md) - Get started in 5 minutes
2. [Configuration](./configuration.md) - Customize system settings
3. [User Manual](./user-manual.md) - Complete feature documentation

## Support

If you encounter installation issues:
1. Check the [Troubleshooting Guide](./troubleshooting.md)
2. Verify system requirements
3. Ensure all dependencies are correctly installed
4. Test with the verification scripts above
