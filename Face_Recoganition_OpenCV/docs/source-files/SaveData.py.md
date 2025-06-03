# SaveData.py - User Registration and Data Storage

**File Path**: `SaveData.py`  
**Purpose**: Handles user registration process including duplicate detection and face encoding storage

## Overview

The `SaveData.py` module manages the complete user registration workflow, from face detection and encoding to duplicate checking and final data storage. It ensures data integrity and provides user interaction for handling duplicate registrations.

## Dependencies

```python
import os
from numpy import save as np_save
from MatchData import matchData
import interFace_msg as interFace
from camera import Camera
```

## Class: saveData

### Constructor
```python
def __init__(self, imag, load_data=None, showConfidence=False, threshold_confidence=0.7):
```

**Parameters**:
- `imag`: Path to image file for registration
- `load_data`: LoadData object for duplicate checking (optional)
- `showConfidence`: Whether to display confidence percentages (default: False)
- `threshold_confidence`: Confidence threshold for duplicate detection (default: 0.7)

**Initialization**:
- Sets up registration parameters and flags
- Automatically initiates encoding and registration process
- Configures duplicate detection settings

**Instance Variables**:
```python
self.name = ""                    # User name
self.id = ""                      # User ID
self.flag = False                 # Registration success flag
self.load_data = load_data        # Reference to existing data
self.dno = 0                      # Data sequence number
self.path = ""                    # Final file path
self.imag = imag                  # Source image path
self.showConfidence = showConfidence
self.threshold_confidence = threshold_confidence
```

### Registration Process

```python
def encode(self):
```
**Purpose**: Main registration workflow handling face detection, duplicate checking, and user interaction

**Process Flow**:

#### 1. Face Detection and Cropping
```python
cropped_faces, face_locations = Camera.crop_face(self.imag)
encodings = Camera.get_face_encodings(self.imag, face_locations)
```
- Detects faces in source image
- Crops each detected face with margin
- Generates face encodings for each face

#### 2. Face Processing Loop
```python
for i, (cropped_face, face_location, encoding) in enumerate(zip(cropped_faces, face_locations, encodings)):
```
- Processes each detected face individually
- Handles multiple faces in single image
- Creates temporary cropped face file

#### 3. Duplicate Detection
```python
matcher = matchData(cropped_face_path, load_data=self.load_data)
if matcher.result is not None and matcher.result[3] < self.threshold_confidence:
    # Handle duplicate scenario
```
- Compares new face against existing database
- Uses confidence threshold to determine duplicates
- Initiates user interaction for duplicate resolution

#### 4. User Interaction for Duplicates
```python
choice = interFace.interfaceSaveData(matcher.result[0], matcher.result[1], matcher.result[3], showConfidence=self.showConfidence)
```

**User Options**:
- **Option 1**: Save with existing name and ID
- **Option 2**: Save with new name and ID  
- **Option 3**: Update existing data
- **Other**: Abort registration

#### 5. Data Collection and Storage
Based on user choice, collects necessary information and saves face encoding.

### File Storage Management

```python
def save_img(self, encoding):
```
**Purpose**: Save face encoding to uniquely named file

**Features**:
- **Directory Creation**: Ensures data directory exists
- **Unique Naming**: Increments sequence number to avoid conflicts
- **File Format**: Saves as `.npy` numpy array format

**Naming Convention**:
```
{name}_{id}_{sequence_number}.npy
```

**Example Files**:
```
John_Doe_EMP001_0.npy
John_Doe_EMP001_1.npy  # If multiple registrations
Jane_Smith_EMP002_0.npy
```

**Collision Avoidance**:
```python
while True:
    self.path = os.path.join(data_dir, f'{self.name}_{self.id}_{self.dno}.npy')
    if not os.path.exists(self.path):
        break
    self.dno += 1
```

## Duplicate Handling Workflow

### Detection Logic
```python
if matcher.result[3] < self.threshold_confidence:
    # Potential duplicate detected
```
- Uses distance-based confidence scoring
- Lower scores indicate higher similarity
- Configurable threshold for sensitivity adjustment

### User Decision Processing

#### Option 1: Use Existing Data
```python
if choice == 1:
    self.name = matcher.result[0]
    self.id = matcher.result[1]
    self.save_img(encoding)
    self.flag = True
```
- Keeps existing user information
- Saves new encoding with same name/ID
- Adds to existing user's face data

#### Option 2: New User Data
```python
elif choice == 2:
    self.name, self.id = interFace.input_data()
    self.save_img(encoding)
    self.flag = True
```
- Prompts for new name and ID
- Treats as completely new user
- Creates separate user entry

#### Option 3: Update Existing
```python
elif choice == 3:
    self.name, self.id = interFace.input_data()
    # Remove old file and save with new info
    self.save_img(encoding)
    self.flag = True
```
- Prompts for new name and ID
- Updates existing user with new information
- Replaces old data with new

#### Option 4: Abort
```python
else:
    self.flag = False
```
- Cancels registration process
- No data saved
- User can retry if desired

## Error Handling

### Image Processing Errors
```python
if face_locations is None or encodings is None:
    self.flag = False
    return
```

**Handled Scenarios**:
- **No faces detected**: Image contains no recognizable faces
- **Encoding failure**: Face encoding generation failure
- **File access issues**: Cannot read source image

### File System Errors
- **Directory creation**: Automatic data directory creation
- **File permissions**: Handles write permission issues
- **Disk space**: Assumes sufficient storage available

### Data Validation
- **Valid encodings**: Ensures face encodings are properly formatted
- **User input**: Accepts any string input for names and IDs
- **File naming**: Handles special characters in filenames

## Integration Points

### With Camera Module
```python
# Face detection and processing
cropped_faces, face_locations = Camera.crop_face(self.imag)
encodings = Camera.get_face_encodings(self.imag, face_locations)
```

### With MatchData Module
```python
# Duplicate detection
matcher = matchData(cropped_face_path, load_data=self.load_data)
```

### With Interface Module
```python
# User interaction
choice = interFace.interfaceSaveData(...)
name, id = interFace.input_data()
```

## Configuration Options

### Confidence Threshold
- **Purpose**: Controls duplicate detection sensitivity
- **Range**: 0.0 (very strict) to 1.0 (very lenient)
- **Default**: 0.7
- **Effect**: Lower values detect more duplicates

### Display Settings
- **showConfidence**: Controls confidence percentage display
- **User feedback**: Provides detailed similarity information
- **Decision support**: Helps users make informed choices

## Usage Patterns

### Basic Registration
```python
save_data = saveData("path/to/image.jpg", load_data_instance)
if save_data.flag:
    print(f"Registration successful: {save_data.name} ({save_data.id})")
```

### Registration with Custom Settings
```python
save_data = saveData(
    image_path, 
    load_data_instance, 
    showConfidence=True, 
    threshold_confidence=0.5
)
```

### Batch Registration
```python
for image_path in image_list:
    save_data = saveData(image_path, load_data_instance)
    if save_data.flag:
        registered_users.append((save_data.name, save_data.id))
```

## Notes

- **Interactive Process**: Requires user input for duplicate resolution
- **Data Integrity**: Ensures consistent file naming and storage
- **Multiple Faces**: Processes all faces found in source image
- **Flexible Thresholds**: Configurable sensitivity for duplicate detection
- **Safe Operations**: Non-destructive processing with user confirmation
- **Cross-platform**: Compatible file operations across operating systems