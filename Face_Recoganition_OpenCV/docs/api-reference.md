# API Reference

Complete technical documentation for the Face Recognition System modules and APIs.

## Table of Contents
- [System Architecture](#system-architecture)
- [Core Modules](#core-modules)
- [Interface Classes](#interface-classes)
- [Data Management](#data-management)
- [Excel Operations](#excel-operations)
- [Configuration System](#configuration-system)
- [Error Handling](#error-handling)

## System Architecture

### Overview
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Interface     │────│  Core Modules   │────│  Data Storage   │
│                 │    │                 │    │                 │
│ • Interface.py  │    │ • SaveData.py   │    │ • .npy files    │
│ • Interface_    │    │ • LoadData.py   │    │ • Excel files   │
│   excel.py      │    │ • MatchData.py  │    │ • config.json   │
│ • interFace_    │    │ • camera.py     │    │ • Backups       │
│   msg.py        │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Process Flow
```
1. Application Start (run.py)
   ↓
2. Backup Creation (create_backup.py)
   ↓
3. Interface Initialization (Interface_excel.py)
   ↓
4. User Operations (Camera, Recognition, Excel)
   ↓
5. Data Processing (SaveData, LoadData, MatchData)
   ↓
6. Storage Operations (Excel, NumPy files)
```

## Core Modules

### SaveData.py

#### Class: `saveData`

**Purpose**: Handles face encoding and data saving operations

```python
class saveData:
    def __init__(self, imag, load_data=None, showConfidence=False, threshold_confidence=0.7)
```

**Parameters**:
- `imag`: Input image (numpy array)
- `load_data`: LoadData instance for existing data
- `showConfidence`: Boolean to show confidence levels
- `threshold_confidence`: Confidence threshold for saving

**Methods**:

##### `save_encoding(name, id)`
```python
def save_encoding(self, name, id)
```
**Purpose**: Save face encoding to .npy file
**Parameters**:
- `name` (str): User name
- `id` (str): User ID
**Returns**: Boolean indicating success

##### `get_encoding()`
```python
def get_encoding(self)
```
**Purpose**: Extract face encoding from image
**Returns**: numpy array of face encoding or None

**Example Usage**:
```python
from SaveData import saveData
import cv2

# Load image
image = cv2.imread("user_photo.jpg")

# Initialize SaveData
save_data = saveData(image, showConfidence=True, threshold_confidence=0.3)

# Save encoding
success = save_data.save_encoding("John Doe", "EMP001")
print(f"Saved: {success}")
```

### LoadData.py

#### Class: `loadData`

**Purpose**: Loads and manages existing face encodings

```python
class loadData:
    def __init__(self)
```

**Attributes**:
- `data`: List of face encodings
- `labels`: List of corresponding user labels

**Methods**:

##### `load()`
```python
def load(self)
```
**Purpose**: Load all face encodings from data directory
**Returns**: None (populates internal attributes)

##### `get_data()`
```python
def get_data(self)
```
**Purpose**: Get loaded face encodings
**Returns**: Tuple (data_list, labels_list)

**Example Usage**:
```python
from LoadData import loadData

# Initialize and load data
load_data = loadData()

# Get all encodings
encodings, labels = load_data.get_data()
print(f"Loaded {len(encodings)} face encodings")
```

### MatchData.py

#### Class: `matchData`

**Purpose**: Handles face recognition and matching operations

```python
class matchData:
    def __init__(self, imag, load_data, showConfidence=False, confidence_threshold=0.4)
```

**Parameters**:
- `imag`: Input image for recognition
- `load_data`: LoadData instance with existing data
- `showConfidence`: Show confidence percentages
- `confidence_threshold`: Recognition threshold

**Methods**:

##### `match()`
```python
def match(self)
```
**Purpose**: Match input face against known encodings
**Returns**: Tuple (is_match, name, id, confidence)

##### `get_best_match()`
```python
def get_best_match(self)
```
**Purpose**: Get best matching result with details
**Returns**: Dict with match information

**Example Usage**:
```python
from MatchData import matchData
from LoadData import loadData
import cv2

# Load existing data
load_data = loadData()

# Load test image
test_image = cv2.imread("test_face.jpg")

# Initialize matcher
matcher = matchData(test_image, load_data, showConfidence=True, confidence_threshold=0.4)

# Perform recognition
is_match, name, user_id, confidence = matcher.match()

if is_match:
    print(f"Recognized: {name} (ID: {user_id}) - Confidence: {confidence:.2f}%")
else:
    print("User not recognized")
```

### camera.py

#### Class: `Camera`

**Purpose**: Handles camera operations and image capture

```python
class Camera:
    def __init__(self)
```

**Attributes**:
- `path`: Data directory path
- `isSaved`: Boolean indicating if data was saved
- `cam`: OpenCV VideoCapture object

**Methods**:

##### `open_camera_for_registration(save_data)`
```python
def open_camera_for_registration(self, save_data)
```
**Purpose**: Open camera for user registration
**Parameters**: 
- `save_data`: SaveData instance
**Returns**: None

##### `open_camera_for_recognition(load_data, match_data)`
```python
def open_camera_for_recognition(self, load_data, match_data)
```
**Purpose**: Open camera for face recognition
**Parameters**:
- `load_data`: LoadData instance
- `match_data`: MatchData instance
**Returns**: None

##### `release_camera()`
```python
def release_camera(self)
```
**Purpose**: Release camera resources
**Returns**: None

**Example Usage**:
```python
from camera import Camera
from SaveData import saveData

# Initialize camera
camera = Camera()

# For registration
save_data = saveData(None)
camera.open_camera_for_registration(save_data)

# Clean up
camera.release_camera()
```

## Interface Classes

### Interface_excel.py

#### Class: `interFace`

**Purpose**: Main interface with Excel integration

```python
class interFace:
    def __init__(self, excel_path, config_path='config.json')
```

**Parameters**:
- `excel_path`: Path to Excel attendance file
- `config_path`: Path to configuration file

**Key Methods**:

##### `run(config_path)`
```python
def run(self, config_path)
```
**Purpose**: Main application loop
**Parameters**: 
- `config_path`: Configuration file path

##### `registerViaCamera()`
```python
def registerViaCamera(self)
```
**Purpose**: Register user through camera capture

##### `registerViaImage(imag)`
```python
def registerViaImage(self, imag)
```
**Purpose**: Register user from image file
**Parameters**:
- `imag`: Image file path

##### `recognize()`
```python
def recognize(self)
```
**Purpose**: Start face recognition process

##### `operate_excel()`
```python
def operate_excel(self)
```
**Purpose**: Excel operations menu

##### `configureConfidence()`
```python
def configureConfidence(self)
```
**Purpose**: Configure confidence thresholds

### interFace_msg.py

#### Functions

##### `message(message, input_key=False)`
```python
def message(message, input_key=False)
```
**Purpose**: Display formatted messages
**Parameters**:
- `message`: Message to display
- `input_key`: Wait for key press if True

##### `interfaceSaveData(name, id, conf, showConfidence=False)`
```python
def interfaceSaveData(name, id, conf, showConfidence=False)
```
**Purpose**: Handle duplicate user registration interface
**Parameters**:
- `name`: User name
- `id`: User ID  
- `conf`: Confidence level
- `showConfidence`: Show confidence value
**Returns**: Integer choice (0-3)

##### `input_data()`
```python
def input_data()
```
**Purpose**: Get user name and ID input
**Returns**: Tuple (name, id)

## Data Management

### Excel Operations

#### Class: `Excel_handle` (excel_handle.py)

**Purpose**: Excel file operations and data logging

```python
class Excel_handle:
    def __init__(self, file_path)
```

**Methods**:

##### `create_excel_file()`
```python
def create_excel_file(self)
```
**Purpose**: Create new Excel file with headers
**Returns**: Boolean indicating success

##### `write_to_excel(name, id)`
```python
def write_to_excel(self, name, id)
```
**Purpose**: Write attendance entry to Excel
**Parameters**:
- `name`: User name
- `id`: User ID
**Returns**: Boolean indicating success

##### `get_row_number(id)`
```python
def get_row_number(self, id)
```
**Purpose**: Find user row in Excel by ID
**Parameters**:
- `id`: User ID
**Returns**: Row number or None

##### `query_entry_by_date(row_number, date)`
```python
def query_entry_by_date(self, row_number, date)
```
**Purpose**: Get entries for specific date
**Parameters**:
- `row_number`: User row number
- `date`: Target date (YYYY-MM-DD)
**Returns**: List of entries

##### `query_entry_by_time_range(row_number, start_date, end_date)`
```python
def query_entry_by_time_range(self, row_number, start_date, end_date)
```
**Purpose**: Get entries in date range
**Parameters**:
- `row_number`: User row number  
- `start_date`: Start date
- `end_date`: End date
**Returns**: List of entries

##### `manual_entry(name, id, custom_datetime=None)`
```python
def manual_entry(self, name, id, custom_datetime=None)
```
**Purpose**: Create manual attendance entry
**Parameters**:
- `name`: User name
- `id`: User ID
- `custom_datetime`: Custom timestamp (optional)

**Example Usage**:
```python
from excel_handle import Excel_handle

# Initialize Excel handler
excel = Excel_handle("attendance.xlsx")

# Create new file
excel.create_excel_file()

# Write entry
success = excel.write_to_excel("John Doe", "EMP001")

# Query entries
row = excel.get_row_number("EMP001")
entries = excel.query_entry_by_date(row, "2025-06-02")
```

### Backup System

#### Module: `create_backup.py`

##### `create_backup(data_dir, excel_path, backup_dir)`
```python
def create_backup(data_dir, excel_path, backup_dir)
```
**Purpose**: Create timestamped backup of data
**Parameters**:
- `data_dir`: Source data directory
- `excel_path`: Excel file path
- `backup_dir`: Backup destination directory
**Returns**: Boolean indicating success

**Example Usage**:
```python
import create_backup as backup
import os

data_dir = os.path.join(os.getcwd(), 'data')
excel_path = os.path.join(data_dir, 'data.xlsx')
backup_dir = os.path.join(os.getcwd(), 'backup')

success = backup.create_backup(data_dir, excel_path, backup_dir)
print(f"Backup created: {success}")
```

## Configuration System

### Configuration Structure

```json
{
    "confidence_match": 0.4,
    "confidence_save": 0.4,
    "show_confidence": true
}
```

### Configuration Methods

##### `load_config(config_path='config.json')`
```python
def load_config(self, config_path='config.json')
```
**Purpose**: Load configuration from JSON file
**Parameters**:
- `config_path`: Path to config file
**Returns**: Dictionary with configuration

##### `save_config(config, config_path='config.json')`
```python
def save_config(self, config, config_path='config.json')
```
**Purpose**: Save configuration to JSON file
**Parameters**:
- `config`: Configuration dictionary
- `config_path`: Path to config file

## Error Handling

### Common Exceptions

#### `FileNotFoundError`
**Cause**: Missing data files or configuration
**Handling**: Automatic file creation or backup restoration

#### `PermissionError`
**Cause**: Insufficient file permissions
**Handling**: Error message with suggested fixes

#### `cv2.error`
**Cause**: Camera access issues
**Handling**: Graceful fallback and user notification

#### `ValueError`
**Cause**: Invalid input data or configuration
**Handling**: Input validation and error messages

### Error Recovery

#### Automatic Recovery
```python
try:
    # Operation that might fail
    operation()
except Exception as e:
    # Log error
    print(f"Error: {e}")
    # Attempt recovery
    recover_from_backup()
```

#### Manual Recovery
- Backup restoration from `backup/` directory
- Configuration reset to defaults
- Data file regeneration

## Performance Considerations

### Memory Management
- Face encodings cached in memory
- Automatic cleanup of large objects
- Efficient NumPy array operations

### Processing Speed
- Optimized face detection algorithms
- Parallel processing for multiple faces
- Efficient file I/O operations

### Resource Usage
- Camera resource management
- Excel file locking prevention
- CPU usage optimization

## Integration Examples

### Custom Recognition Script
```python
import cv2
from LoadData import loadData
from MatchData import matchData

# Load existing data
load_data = loadData()

# Capture from camera
cap = cv2.VideoCapture(0)
ret, frame = cap.read()

if ret:
    # Initialize matcher
    matcher = matchData(frame, load_data, confidence_threshold=0.4)
    
    # Perform recognition
    is_match, name, user_id, confidence = matcher.match()
    
    if is_match:
        print(f"User: {name}, ID: {user_id}, Confidence: {confidence:.2f}")
    else:
        print("Unknown user")

cap.release()
```

### Batch Registration
```python
import os
import cv2
from SaveData import saveData
from LoadData import loadData

# Load existing data
load_data = loadData()

# Process directory of images
image_dir = "user_photos/"
for filename in os.listdir(image_dir):
    if filename.endswith(('.jpg', '.png')):
        # Extract name and ID from filename
        name, user_id = filename.split('_')[:2]
        
        # Load image
        image_path = os.path.join(image_dir, filename)
        image = cv2.imread(image_path)
        
        # Save encoding
        save_data = saveData(image, load_data)
        success = save_data.save_encoding(name, user_id)
        print(f"Processed {filename}: {success}")
```

### Custom Excel Integration
```python
from excel_handle import Excel_handle
from datetime import datetime

# Initialize Excel handler
excel = Excel_handle("custom_attendance.xlsx")

# Create custom headers
excel.create_excel_file()

# Add entries with custom timestamps
entries = [
    ("John Doe", "EMP001", "2025-06-02 09:00:00"),
    ("Jane Smith", "EMP002", "2025-06-02 09:15:00"),
]

for name, user_id, timestamp in entries:
    custom_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    excel.manual_entry(name, user_id, custom_time)
```

This API reference provides comprehensive technical documentation for integrating with and extending the Face Recognition System.
