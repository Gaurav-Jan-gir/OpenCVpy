# camera.py - Camera Operations and Image Processing

**File Path**: `camera.py`  
**Purpose**: Handles camera operations, face detection, image processing, and face encoding

## Overview

The `camera.py` module provides comprehensive camera and image processing functionality for the face recognition system. It handles camera capture, face detection, cropping, encoding, and visualization operations.

## Dependencies

```python
import cv2 as cv
from face_recognition import face_locations, face_encodings
from interFace_msg import message
import os
```

## Class: Camera

### Constructor
```python
def __init__(self):
```

**Initialization**:
- Sets up data directory path: `data/`
- Initializes save status flag: `isSaved = False`
- Opens default camera (index 0): `cv.VideoCapture(0)`

### Camera Management

#### Camera Cleanup
```python
def destroy(self):
```
**Purpose**: Properly close camera and cleanup resources

**Operations**:
- Destroys all OpenCV windows
- Releases camera resource if still open
- Displays confirmation message
- Ensures clean shutdown

#### Live Camera Capture
```python
def capture(self):
```
**Purpose**: Interactive camera capture with live preview

**Features**:
- **Camera Validation**: Checks camera availability
- **Live Preview**: Real-time camera feed display
- **Interactive Control**: Keyboard-based capture control
- **File Management**: Saves captured images with proper naming

**Controls**:
- **'s' Key**: Save current frame as `temp.jpg`
- **'q' Key**: Quit capture mode
- Sets `isSaved = True` flag on successful save

**Error Handling**:
- Validates camera connection
- Handles frame read failures
- Creates data directory if needed

## Static Image Processing Methods

### Face Detection and Cropping
```python
@staticmethod
def crop_face(image_path):
```
**Purpose**: Detect and crop faces from image

**Parameters**:
- `image_path`: Path to source image file

**Returns**:
- `tuple`: (cropped_faces, cropped_faces_locations) or None on error

**Process**:
1. **Image Loading**: Loads image using OpenCV
2. **Color Conversion**: BGR to RGB for face_recognition library
3. **Face Detection**: Uses `face_locations()` to find faces
4. **Margin Addition**: Adds 10-pixel margin around detected faces
5. **Boundary Checking**: Ensures crop doesn't exceed image bounds
6. **Face Extraction**: Crops each detected face

**Face Location Format**:
```python
(top, right, bottom, left)  # face_recognition format
```

**Margin Calculation**:
```python
margin = 10
top = max(0, top - margin)
left = max(0, left - margin)
bottom = min(image_bgr.shape[0], bottom + margin)
right = min(image_bgr.shape[1], right + margin)
```

### Face Encoding Generation
```python
@staticmethod
def get_face_encodings(image_path, face_locations, convert_to_bgr=False):
```
**Purpose**: Generate 128-dimensional face encodings

**Parameters**:
- `image_path`: Path to image file
- `face_locations`: List of face location tuples
- `convert_to_bgr`: Optional color space conversion

**Returns**:
- List of 128-dimensional numpy arrays (face encodings)
- None if no encodings found

**Process**:
1. **Image Loading**: Loads image from file path
2. **Color Conversion**: Optional BGR conversion
3. **Encoding Generation**: Uses face_recognition library
4. **Validation**: Ensures encodings were successfully created

### Image Writing Operations
```python
@staticmethod
def img_write(image, path, convert_to_bgr=False):
```
**Purpose**: Save image to file with optional color conversion

**Parameters**:
- `image`: Image array to save
- `path`: Target file path
- `convert_to_bgr`: Convert RGB to BGR before saving

**Features**:
- **Directory Creation**: Automatically creates directories if needed
- **Color Conversion**: Optional RGB to BGR conversion for OpenCV compatibility
- **Path Handling**: Handles nested directory structures

### Face Recognition Visualization
```python
@staticmethod
def put_rectangle(image_path, location, name, id, convert_to_bgr=False):
```
**Purpose**: Draw recognition results on image

**Parameters**:
- `image_path`: Path to image file
- `location`: Face location tuple (top, right, bottom, left)
- `name`: Recognized person's name
- `id`: Recognized person's ID
- `convert_to_bgr`: Optional color conversion

**Visualization Elements**:
- **Green Rectangle**: Drawn around detected face
- **Text Label**: Name and ID displayed above face
- **Interactive Display**: Shows result in window until key press

**Drawing Specifications**:
```python
cv.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)  # Green, 2px width
cv.putText(image, f"{name} (ID: {id})", (left, top - 10), 
           cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
```

## Error Handling

### Camera Errors
- **Connection Issues**: Validates camera availability before operations
- **Frame Read Failures**: Handles dropped frames gracefully
- **Resource Management**: Ensures proper cleanup on errors

### Image Processing Errors
- **File Access**: Validates image file existence and readability
- **Format Issues**: Handles unsupported image formats
- **Memory Issues**: Manages large image processing

### Face Detection Errors
- **No Faces Found**: Provides clear error messages
- **Invalid Crops**: Validates cropped face dimensions
- **Encoding Failures**: Handles face encoding generation errors

## Integration Points

### With SaveData Module
- Provides cropped faces for registration
- Generates face encodings for storage
- Handles image preprocessing

### With Recognition System
- Supplies face detection capabilities
- Provides encoding generation
- Handles result visualization

### With File System
- Manages temporary image storage
- Creates necessary directories
- Handles file path operations

## File Management

### Temporary Files
- **temp.jpg**: Temporary capture storage in data directory
- **Automatic Cleanup**: Temporary files managed by calling modules
- **Directory Structure**: Maintains organized file storage

### Image Formats
- **Input Formats**: JPG, PNG, BMP, TIFF supported
- **Output Format**: JPG for captures, preserves format for processing
- **Color Spaces**: Handles RGB/BGR conversion automatically

## Performance Considerations

### Camera Operations
- **Resource Management**: Efficient camera resource usage
- **Frame Processing**: Real-time frame handling
- **Memory Usage**: Minimal memory footprint for live operations

### Image Processing
- **Batch Processing**: Efficient multiple face handling
- **Memory Optimization**: Processes images without excessive memory usage
- **Speed Optimization**: Fast face detection and cropping

## Notes

- **Static Methods**: Most functionality provided as static methods for flexibility
- **OpenCV Integration**: Seamless integration with OpenCV library
- **Face Recognition**: Compatible with face_recognition library standards
- **Error Resilience**: Comprehensive error handling throughout
- **Cross-platform**: Compatible with Windows and Unix systems
- **Resource Safety**: Proper cleanup and resource management