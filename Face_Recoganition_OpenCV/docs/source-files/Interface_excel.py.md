# Interface_excel.py - Main Application Interface

**File Path**: `Interface_excel.py`  
**Purpose**: Main application interface with Excel integration for attendance tracking

## Overview

The `Interface_excel.py` file contains the primary interface class that handles all user interactions, face recognition operations, and Excel-based attendance logging. This is the core module that coordinates all system functions.

## Dependencies

```python
from multiprocessing import Process, Queue
import os
from MatchData import matchData
from SaveData import saveData
from LoadData import loadData
from camera import Camera
from interFace_msg import message
from excel_handle import Excel_handle
import json
from capture_camera_frames import Capture_camera_frames as ccf
```

## Class: interFace

### Constructor
```python
def __init__(self, excel_path, config_path):
```

**Parameters**:
- `excel_path`: Path to Excel file for attendance logging
- `config_path`: Path to JSON configuration file

**Initialization**:
- Loads configuration from JSON file
- Sets up data directory path
- Initializes data loader
- Configures confidence thresholds
- Creates Excel handler instance

### Configuration Management

**Default Configuration Structure**:
```json
{
    "confidence_match": 0.6,
    "confidence_save": 0.6, 
    "show_confidence": true
}
```

**Configuration Loading**:
```python
def load_config(self, config_path):
    # Creates default config if file doesn't exist
    # Returns loaded configuration dictionary
```

## Main Menu System

### Menu Options

```
Welcome to the face recognition system
1. Register a new user via Camera
2. Register a new user via Image  
3. Start Recognition
4. Check if User Data exist or not.
5. Configure Confidence Levels (Default 60%)
6. Operate on data in Excel.
7. Exit
```

### Menu Flow Control

**Input Validation**:
- Handles invalid numeric input
- Provides error messages and continuation prompts
- Clears screen between operations

**Navigation**:
- Number-based menu selection
- Continuous loop until exit selected
- Exception handling for user input errors

## Core Features

### 1. User Registration

#### Via Camera (Option 1)
```python
def registerViaCamera(self):
```
- Opens camera interface for live capture
- Captures face image using Camera class
- Processes registration through SaveData class
- Handles success/failure feedback

#### Via Image File (Option 2)  
```python
def registerViaImage(self, image_path):
```
- Accepts image file path from user
- Validates file existence and format
- Processes registration through SaveData class
- Supports multiple image formats

### 2. Face Recognition (Option 3)
```python
def recognize(self):
```

**Recognition Submenu**:
```
Select Recognition Mode:
1. Real-time Recognition (Continuous)
2. Manual Capture Recognition  
3. Back to Main Menu
```

**Real-time Mode**: Continuous face detection and recognition with automatic Excel logging
**Manual Mode**: Press-to-capture recognition with optional manual logging

### 3. User Data Verification (Option 4)
```python
def checkUserData(self):
```
- Prompts for user name and ID
- Checks if corresponding `.npy` file exists
- Provides confirmation of data existence

### 4. Configuration Management (Option 5)
```python
def configureConfidence(self, config_path):
```

**Configuration Submenu**:
```
Select the item you want to configure:
1. Change Whether to Show Confidence or not
2. Change Confidence for Recognition (Matching)
3. Change Confidence for Saving (Registering)  
4. Go Back to Main Menu
```

### 5. Excel Operations (Option 6)
```python
def excelOperations(self):
```

**Excel Operations Menu**:
```
1. Check user entry on a specific date
2. Check user entries in a time range
3. Get all entries of a user
4. Manually create user entry with current date/time
5. Manually create user entry with manual date/time
6. Back to Main Menu
```

## Multiprocessing Architecture

### Process Management
```python
# Camera capture process
camera_process = Process(target=ccf().run, args=(fps, q))

# Recognition process  
recognition_process = Process(target=self.recognition_process, args=(q, excel_queue))

# Excel logging process
excel_process = Process(target=self.excel_process, args=(excel_queue,))
```

**Process Communication**:
- Uses `Queue` objects for inter-process communication
- Separate processes for camera, recognition, and Excel operations
- Non-blocking operation for real-time performance

## Integration Points

### Data Flow
1. **Camera/Image Input** → **SaveData/MatchData** → **LoadData**
2. **Recognition Results** → **Excel_handle** → **Attendance Logging**
3. **Configuration Changes** → **JSON File Update** → **Runtime Application**

### Error Handling
- File path validation for images
- Camera availability checking
- Excel file access permissions
- Configuration file corruption recovery

## Key Methods

### Utility Methods
```python
def clear_screen(self):          # Clear console display
def is_valid_path(self, path):   # Validate file/directory paths
def save_config(self, config, config_path):  # Save configuration to JSON
```

### Recognition Processing
```python
def recognition_process(self, q, excel_queue):  # Handle recognition logic
def excel_process(self, excel_queue):           # Handle Excel logging
```

## Configuration Options

### Confidence Thresholds
- **Recognition Confidence**: Controls matching strictness (default: 60%)
- **Save Confidence**: Controls duplicate detection during registration (default: 60%)
- **Show Confidence**: Display confidence percentages (default: True)

### Runtime Settings
- Configurable during application execution
- Persistent storage in JSON format
- Immediate application of changes

## Error Recovery

### Graceful Degradation
- Continues operation if Excel file is temporarily locked
- Provides fallback options for configuration errors
- Maintains system state during process failures

### User Feedback
- Clear error messages with suggested actions
- Interactive prompts for error resolution
- Automatic retry mechanisms where applicable

## Notes

- Main orchestration point for all system functions
- Handles both real-time and batch processing modes
- Integrates camera, recognition, and data storage subsystems
- Provides comprehensive user interface for all operations
- Supports multiprocessing for performance optimization
