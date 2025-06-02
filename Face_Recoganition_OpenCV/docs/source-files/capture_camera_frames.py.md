# capture_camera_frames.py - Camera Frame Capture System

**File Path**: `capture_camera_frames.py`  
**Purpose**: Handles continuous camera frame capture for multiprocessing face recognition

## Overview

The `capture_camera_frames.py` module provides camera frame capture functionality designed for multiprocessing environments. It captures camera frames at specified intervals and stores them for processing by recognition systems.

## Dependencies

```python
import cv2 as cv
import os
import datetime
```

## Class: Capture_camera_frames

### Constructor
```python
def __init__(self):
```

**Initialization**:
- Sets up capture frames directory path: `capture_frames/`
- Configures default FPS: 30 frames per second
- Creates capture directory if it doesn't exist

**Directory Structure**:
```
capture_frames/
├── img_20250602_143015_0.jpg
├── img_20250602_143015_1.jpg
├── img_20250602_143015_2.jpg
└── ...
```

### Main Processing Method

```python
def run(self, fps, q):
```
**Purpose**: Main entry point for frame capture process

**Parameters**:
- `fps`: Frames per second for capture rate
- `q`: Queue object for inter-process communication

**Process**:
1. Adjusts frame rate using `adjust_frame_perseconds(fps)`
2. Initiates camera capture with `capture_camera_frames(q)`

### Frame Capture Core

```python
def capture_camera_frames(self, q):
```
**Purpose**: Continuous camera frame capture with queue communication

**Features**:
- **Camera Initialization**: Opens default camera (index 0)
- **Error Handling**: Validates camera availability
- **Continuous Capture**: Runs in infinite loop for real-time processing
- **Frame Storage**: Saves frames to timestamped image files
- **Queue Communication**: Sends frame data to recognition processes

**Camera Setup**:
```python
cam = cv.VideoCapture(0)
if not cam.isOpened():
    print("Could not open camera. Please check your camera connection.")
    return
```

**Capture Loop**:
```python
i = 0
while True:
    ret, frame = cam.read()
    if not ret:
        # Handle frame read failure
        break
    # Process and save frame
    # Send to queue for recognition
    i += 1
```

### Frame Rate Management

```python
def adjust_frame_perseconds(self, fps):
```
**Purpose**: Adjust capture frame rate for optimal performance

**Parameters**:
- `fps`: Target frames per second

**Returns**:
- Adjusted FPS value optimized for system performance

**Considerations**:
- System processing capability
- Camera hardware limitations
- Recognition processing speed
- Storage space management

## File Naming Convention

### Timestamp-Based Naming
```
img_YYYYMMDD_HHMMSS_INDEX.jpg
```

**Components**:
- `YYYYMMDD`: Date in year-month-day format
- `HHMMSS`: Time in hour-minute-second format  
- `INDEX`: Sequential frame number within the second

**Examples**:
```
img_20250602_143015_0.jpg    # First frame at 14:30:15
img_20250602_143015_1.jpg    # Second frame at 14:30:15
img_20250602_143016_0.jpg    # First frame at 14:30:16
```

## Integration with Multiprocessing

### Process Communication
- **Queue Interface**: Receives queue object for frame data transmission
- **Non-blocking Operation**: Continuous capture without blocking main thread
- **Frame Metadata**: Includes timestamp and frame index information

### Usage in Recognition System
```python
from multiprocessing import Process, Queue
from capture_camera_frames import Capture_camera_frames as ccf

# Create queue for communication
frame_queue = Queue()

# Start capture process
capture_process = Process(target=ccf().run, args=(30, frame_queue))
capture_process.start()

# Recognition process reads from queue
while True:
    frame_data = frame_queue.get()
    # Process frame for recognition
```

## Performance Optimization

### Frame Rate Adjustment
- Dynamic FPS adaptation based on system load
- Balances capture quality with processing speed
- Prevents frame buffer overflow

### Storage Management
- Automatic directory creation
- Organized file structure by timestamp
- Sequential numbering prevents conflicts

### Memory Efficiency
- Frame-by-frame processing
- No large buffer accumulation
- Efficient OpenCV memory usage

## Error Handling

### Camera Errors
- **Camera Unavailable**: Graceful error message and exit
- **Frame Read Failure**: Handles dropped frames
- **Permission Issues**: Reports camera access problems

### File System Errors
- **Directory Creation**: Automatic directory setup
- **Write Permissions**: Validates file write access
- **Storage Space**: Assumes sufficient disk space

### Process Communication
- **Queue Errors**: Handles inter-process communication failures
- **Process Termination**: Clean shutdown procedures

## Configuration Options

### Frame Rate Settings
- **Default FPS**: 30 frames per second
- **Adjustable Rate**: Configurable through `adjust_frame_perseconds()`
- **Dynamic Adaptation**: Runtime FPS modification

### Storage Settings
- **Directory Path**: Configurable capture frames location
- **File Format**: JPEG format for balance of quality and size
- **Naming Convention**: Timestamp-based systematic naming

## Use Cases

### Real-time Recognition
- Continuous frame supply for recognition algorithms
- Multi-process architecture support
- High-frequency capture for accuracy

### Frame Analysis
- Systematic frame storage for analysis
- Timestamp correlation with recognition events
- Historical frame review capability

### Performance Testing
- Capture rate benchmarking
- System load assessment
- Recognition accuracy evaluation

## Notes

- Designed specifically for multiprocessing environments
- Optimized for real-time face recognition applications
- Handles camera resource management automatically
- Provides reliable frame delivery through queue system
- Supports various frame rates depending on system capability
- Creates organized storage structure for captured frames
- Integrates seamlessly with recognition processing pipeline
