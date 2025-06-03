# User Manual

Complete guide to using the Face Recognition System for attendance tracking and access control.

## Table of Contents
- [Getting Started](#getting-started)
- [Main Menu Overview](#main-menu-overview)
- [User Registration](#user-registration)
- [Face Recognition](#face-recognition)
- [Excel Operations](#excel-operations)
- [Configuration](#configuration)
- [Data Management](#data-management)
- [Advanced Features](#advanced-features)

## Getting Started

### Launching the Application
```bash
# Basic launch
python run.py

# With custom Excel file
python run.py "path/to/attendance.xlsx"

# With custom Excel and config files
python run.py "path/to/attendance.xlsx" "path/to/config.json"
```

### First Launch
On first launch, the system automatically:
1. Creates `data/` directory for face encodings
2. Creates `backup/` directory for automatic backups
3. Generates `config.json` with default settings
4. Creates `data.xlsx` for attendance logging

## Main Menu Overview

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

### Menu Navigation
- **Enter numbers** to select options
- **Follow prompts** for each operation
- **Press any key to continue** when prompted
- **Use 'q'** to exit camera operations

## User Registration

### Option 1: Register via Camera

**Best for**: Live registration with real-time feedback

**Steps**:
1. Select **Option 1** from main menu
2. **Camera window opens** automatically
3. **Position face** in the camera frame
   - Ensure good lighting
   - Face clearly visible
   - Look directly at camera
4. **Press SPACE** to capture image
5. **Enter user details**:
   ```
   Enter User Name for the face detected: John Doe
   Enter User ID for the face detected: EMP001
   ```
6. **Confirmation** appears if successful

**Tips**:
- Use consistent lighting conditions
- Avoid shadows on face
- Ensure face occupies good portion of frame
- Multiple registrations improve accuracy

### Option 2: Register via Image

**Best for**: Bulk registration from existing photos

**Steps**:
1. Select **Option 2** from main menu
2. **Enter image path**:
   ```
   Enter the path of the image: C:\photos\john_doe.jpg
   ```
3. **System processes** the image
4. **Enter user details** when prompted
5. **Registration confirmation**

**Supported Formats**:
- JPG/JPEG
- PNG
- BMP
- TIFF

**Image Requirements**:
- Clear, front-facing photo
- Single person per image
- Good resolution (minimum 300x300 pixels)
- Adequate lighting

### Registration Data Handling

**Duplicate Detection**:
If a similar face exists during registration:
```
User already exists with
Name: John Doe and ID: EMP001 with confidence 85.5%
Press 1 to Save Current data with existing Name and ID
Press 2 to Save current data with new Name and ID
Press 3 to Update existing data with new Name and ID
Press any other key to abort saving current data
```

**Options Explained**:
- **Option 1**: Keep existing user, don't save new data
- **Option 2**: Save as new user with different name/ID
- **Option 3**: Update existing user's face data
- **Other**: Cancel registration

## Face Recognition

### Option 3: Recognize a User

**Recognition Menu**:
```
Select Recognition Mode:
1. Real-time Recognition (Continuous)
2. Manual Capture Recognition
3. Back to Main Menu
```

### Real-time Recognition (Option 1)

**Best for**: Continuous monitoring, attendance systems

**Features**:
- **Automatic detection** of faces in camera feed
- **Real-time recognition** with confidence display
- **Automatic Excel logging** of recognized users
- **Timestamp recording** for each recognition

**Operation**:
1. Camera opens with live feed
2. Green rectangles highlight detected faces
3. Names and confidence levels displayed
4. Recognition events automatically logged
5. Press **'q'** to exit

**Display Information**:
```
[Live Camera Feed]
┌─────────────────┐
│  John Doe       │ ← Name appears above face
│  Confidence: 92%│ ← Confidence level
└─────────────────┘
```

### Manual Capture Recognition (Option 2)

**Best for**: Individual verification, access control

**Features**:
- **Press-to-capture** recognition
- **Detailed confidence information**
- **Manual Excel logging** option

**Operation**:
1. Camera opens in preview mode
2. Position face in frame
3. Press **SPACE** to capture and recognize
4. Recognition results displayed
5. Option to log to Excel
6. Press **'q'** to exit

### Recognition Results

**Successful Recognition**:
```
✅ User Recognized: John Doe (ID: EMP001)
🎯 Confidence: 92.5%
📅 Timestamp: 2025-06-02 14:30:15
📊 Automatically logged to Excel
```

**Unknown User**:
```
❌ Unknown user detected
🎯 Best match: Jane Smith (67.2%) - Below threshold
💡 Tip: Adjust confidence levels or register this user
```

## Excel Operations

### Option 6: Excel Operations Menu

**Excel Menu**:
```
📄 Excel Operations Menu
------------------------
1. Check user entry on a specific date
2. Check user entries in a time range
3. Get all entries of a user
4. Manually create user entry with current date/time
5. Manually create user entry with manual date/time
6. Back to Main Menu
```

### Option 1: Check Entry by Date

**Use case**: Verify attendance for specific date

**Steps**:
1. Enter user ID: `EMP001`
2. Enter date in format: `2025-06-02`
3. System displays all entries for that date

**Sample Output**:
```
📅 Entries for John Doe (EMP001) on 2025-06-02:
⏰ 09:15:30 - Check-in
⏰ 12:30:45 - Lunch break
⏰ 13:25:10 - Return from lunch
⏰ 17:45:20 - Check-out
Total entries: 4
```

### Option 2: Time Range Query

**Use case**: Weekly/monthly attendance reports

**Steps**:
1. Enter user ID: `EMP001`
2. Enter start date: `2025-06-01`
3. Enter end date: `2025-06-07`
4. View comprehensive report

### Option 3: All User Entries

**Use case**: Complete attendance history

**Steps**:
1. Enter user ID: `EMP001`
2. System displays complete attendance record
3. Sorted by date and time

### Option 4: Manual Entry (Current Time)

**Use case**: Manual check-in/out, corrections

**Steps**:
1. Enter user name: `John Doe`
2. Enter user ID: `EMP001`
3. Entry created with current timestamp

### Option 5: Manual Entry (Custom Time)

**Use case**: Backdated entries, corrections

**Steps**:
1. Enter user name: `John Doe`
2. Enter user ID: `EMP001`
3. Enter custom date: `2025-06-01`
4. Enter custom time: `14:30:00`

## Configuration

### Option 5: Configure Confidence Levels

**Configuration Menu**:
```
Select the item you want to configure:
1. Change Whether to Show Confidence or not
2. Change Confidence for Recognition (Matching)
3. Change Confidence for Saving (Registering)
4. Go Back to Main Menu
```

### Confidence Settings Explained

#### Recognition Confidence (Option 2)
- **Purpose**: Controls how strict face matching is
- **Range**: 0-100% (lower = more strict)
- **Default**: 40%
- **Effect**: Higher values = easier recognition, more false positives

#### Saving Confidence (Option 3)
- **Purpose**: Controls duplicate detection during registration
- **Range**: 0-100% (lower = more strict)
- **Default**: 40%
- **Effect**: Higher values = easier to detect duplicates

#### Show Confidence (Option 1)
- **Purpose**: Display confidence percentages
- **Options**: True/False
- **Default**: True
- **Effect**: Shows/hides confidence values during recognition

### Recommended Settings

**High Security Environment**:
- Recognition: 30%
- Saving: 30%
- Show Confidence: True

**General Use**:
- Recognition: 40%
- Saving: 40%
- Show Confidence: True

**Relaxed Environment**:
- Recognition: 60%
- Saving: 50%
- Show Confidence: False

## Data Management

### Option 4: Check User Data

**Purpose**: Verify if user is registered in system

**Steps**:
1. Enter user name: `John Doe`
2. Enter user ID: `EMP001`
3. System confirms existence

**Sample Output**:
```
✅ The User Data Exists
📁 File: John_Doe_EMP001_0.npy
📊 Face encoding data available
```

### File Structure

**Data Directory** (`data/`):
```
data/
├── data.xlsx                 # Excel attendance log
├── John_Doe_EMP001_0.npy    # Face encoding for John Doe
├── Jane_Smith_EMP002_0.npy  # Face encoding for Jane Smith
└── ...
```

**Backup Directory** (`backup/`):
```
backup/
├── backup_20250602_143015/
│   ├── data.xlsx
│   ├── John_Doe_EMP001_0.npy
│   └── ...
└── ...
```

### Automatic Backup System

**When Backups Occur**:
- Before each application launch
- Before major data operations
- Configurable intervals

**Backup Contents**:
- All `.npy` face encoding files
- Excel attendance file
- Configuration files

## Advanced Features

### Multi-Process Architecture

The system uses advanced multi-processing for:
- **Real-time camera capture**
- **Parallel face recognition**
- **Non-blocking Excel operations**

### Error Recovery

**Automatic Recovery**:
- Data corruption detection
- Backup restoration
- Configuration reset

### Performance Optimization

**Recognition Speed**:
- Optimized face encoding algorithms
- Efficient data loading
- Memory management

**Accuracy Improvements**:
- Multiple face encodings per user
- Confidence-based matching
- Adaptive thresholds

## Keyboard Shortcuts

### Camera Operations
- **SPACE**: Capture image
- **'q'**: Exit camera mode
- **ESC**: Emergency exit

### Menu Navigation
- **Number keys**: Select menu options
- **Enter**: Confirm selection
- **Any key**: Continue prompts

## Best Practices

### Registration
1. **Multiple angles**: Register users from different angles
2. **Consistent lighting**: Use similar lighting conditions
3. **Clear images**: Ensure high-quality, clear photos
4. **Regular updates**: Re-register users periodically

### Recognition
1. **Optimal distance**: 2-4 feet from camera
2. **Good lighting**: Avoid backlighting and shadows
3. **Clear view**: Ensure face is not obscured
4. **Patience**: Allow time for processing

### Data Management
1. **Regular backups**: Monitor backup directory
2. **File permissions**: Ensure write access to data directory
3. **Disk space**: Monitor available storage
4. **Configuration**: Keep configuration files secure

## Troubleshooting Common Issues

### Recognition Problems
- **Lower confidence thresholds**
- **Re-register problematic users**
- **Check lighting conditions**
- **Verify camera functionality**

### Excel Issues
- **Close Excel application**
- **Check file permissions**
- **Verify backup integrity**
- **Restart application**

### Performance Issues
- **Close unnecessary applications**
- **Restart application**
- **Check system resources**
- **Update dependencies**

For more detailed troubleshooting, see the [Troubleshooting Guide](./troubleshooting.md).
