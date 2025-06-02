# Quick Start Guide

Get your Face Recognition System up and running in under 5 minutes!

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.7+ installed
- ✅ Required dependencies installed ([Installation Guide](./installation.md))
- ✅ Working webcam
- ✅ Project files downloaded

## 5-Minute Setup

### Step 1: Navigate to Project Directory
```bash
cd Face_Recoganition_OpenCV
```

### Step 2: Check Installation
```bash
# Quick verification
python -c "import cv2, face_recognition, openpyxl; print('✅ All dependencies ready!')"
```

### Step 3: Run the Application
```bash
python run.py
```

### Step 4: First Time Setup
When you run the application for the first time:

1. **Data directory** will be created automatically
2. **Config file** will be generated with default settings
3. **Excel file** will be created for attendance tracking

## Your First Recognition

### Register a New User (Option 1 - Camera)

1. **Launch the application**: `python run.py`
2. **Main Menu appears**:
   ```
   Welcome to the face recognition system
   1. Register a new user via Camera
   2. Register a new user via Image
   3. Recognize a user
   4. Check if User Data exist or not.
   5. Configure Confidence Levels (Default 60%)
   6. Excel Operations Menu
   7. Exit
   ```

3. **Choose Option 1** (Register via Camera)
4. **Camera window opens** - position your face in the frame
5. **Press SPACE** to capture your face
6. **Enter your details**:
   - Name: `John Doe`
   - ID: `001`
7. **Data saved** automatically to `data/` folder

### Register via Image (Option 2)

1. **Choose Option 2** from main menu
2. **Enter image path**: `C:\path\to\your\photo.jpg`
3. **Enter your details** when prompted
4. **Registration complete**

### Recognize a User (Option 3)

1. **Choose Option 3** from main menu
2. **Select recognition mode**:
   ```
   1. Real-time Recognition (Continuous)
   2. Manual Capture Recognition
   3. Back to Main Menu
   ```

3. **For Real-time** (Option 1):
   - Camera starts automatically
   - Recognition happens continuously
   - Results logged to Excel
   - Press 'q' to exit

4. **For Manual Capture** (Option 2):
   - Camera opens
   - Press SPACE to capture and recognize
   - Press 'q' to exit

## Quick Configuration

### Adjust Confidence Levels
```
Main Menu → Option 5 → Configure Confidence Levels
```

**Confidence Settings**:
- **Recognition Confidence**: How strict recognition matching is (default: 40%)
- **Saving Confidence**: How strict registration matching is (default: 40%)
- **Show Confidence**: Display confidence percentages (default: Yes)

### Excel Operations
```
Main Menu → Option 6 → Excel Operations Menu
```

**Available Operations**:
1. Check user entry on specific date
2. Check user entries in time range
3. Get all entries of a user
4. Create manual entry with current time
5. Create manual entry with custom time

## Quick Commands

### Command Line Usage
```bash
# Basic usage
python run.py

# Custom Excel file
python run.py "C:\custom\path\attendance.xlsx"

# Custom Excel file and config
python run.py "C:\custom\path\attendance.xlsx" "custom_config.json"
```

### File Structure After Setup
```
Face_Recoganition_OpenCV/
├── data/
│   ├── data.xlsx           # Attendance records
│   ├── John_Doe_001_0.npy  # User face encodings
│   └── ...
├── backup/
│   ├── backup_YYYYMMDD_HHMMSS/
│   └── ...
├── config.json             # System configuration
└── ...
```

## Basic Usage Examples

### Example 1: Employee Check-in System
1. Register all employees using Option 1 (Camera)
2. Use Option 3 → Real-time Recognition for daily check-ins
3. Check attendance using Option 6 → Excel Operations

### Example 2: Access Control
1. Register authorized users
2. Use Manual Capture Recognition for entry verification
3. Monitor access logs through Excel operations

### Example 3: Attendance Tracking
1. Register students/employees
2. Set up continuous recognition mode
3. Export attendance data from Excel file

## Quick Troubleshooting

### Camera Not Working
```bash
# Test camera access
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera Failed'); cap.release()"
```

### Face Not Detected
- **Ensure good lighting**
- **Face clearly visible in camera frame**
- **Adjust confidence levels** (Option 5)

### Recognition Not Working
- **Check if user is registered**: Option 4
- **Lower recognition confidence**: Option 5 → Option 2
- **Re-register user** if needed

### Excel Issues
- **Check file permissions** on data.xlsx
- **Ensure Excel file not open** in other applications
- **Check backup folder** for recent backups

## Next Steps

Once you're comfortable with basic operations:

1. **[User Manual](./user-manual.md)** - Complete feature documentation
2. **[Configuration](./configuration.md)** - Advanced customization
3. **[API Reference](./api-reference.md)** - Technical documentation
4. **[Development](./development.md)** - Extend the system

## Sample Workflow

### Daily Attendance Scenario
```
Morning Setup:
python run.py → Option 3 → Option 1 (Real-time Recognition)

Throughout Day:
- Employees walk by camera
- Automatic recognition and logging
- Real-time attendance tracking

End of Day:
Option 6 → Option 2 (Check time range entries)
Export Excel data for payroll/reporting
```

## Performance Tips

### For Better Recognition
- **Consistent lighting** conditions
- **Clear, front-facing** photos during registration
- **Multiple registration** photos per person (recommended)
- **Regular re-registration** for significant appearance changes

### For Faster Processing
- **Close unnecessary applications** during use
- **Ensure adequate RAM** available
- **Use appropriate confidence levels** (too low = false positives)

## Quick Reference Commands

| Action | Menu Path | Shortcut |
|--------|-----------|----------|
| Register User | Main → 1 | Camera registration |
| Quick Recognition | Main → 3 → 2 | Manual capture |
| Check User Exists | Main → 4 | User verification |
| Adjust Settings | Main → 5 | Confidence config |
| View Attendance | Main → 6 → 3 | User entries |
| Exit Application | Main → 7 | Close program |

Ready to get started? Run `python run.py` and follow this guide!
