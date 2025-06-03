# LoadData.py - Face Encoding Data Loader

**File Path**: `LoadData.py`  
**Purpose**: Loads and manages face encoding data from storage files

## Overview

The `LoadData.py` module handles loading face encoding data from `.npy` files stored in the data directory. It validates data integrity and organizes face encodings with their corresponding user information for use in recognition operations.

## Dependencies

```python
import os
import numpy as np
from interFace_msg import message
```

## Class: loadData

### Constructor
```python
def __init__(self):
```

**Initialization**:
- Creates empty data list: `self.data = []`
- Creates empty labels list: `self.labels = []`
- Automatically calls `load()` method to populate data

**Data Structure**:
- `self.data`: List of 128-dimensional numpy arrays (face encodings)
- `self.labels`: List of tuples containing (name, id, sequence_number)

### Data Loading Process

```python
def load(self):
```
**Purpose**: Load all face encoding files from data directory

**Process**:
1. **Directory Scanning**: Iterates through all files in `data/` directory
2. **File Filtering**: Processes only `.npy` files
3. **Data Loading**: Loads numpy arrays from files
4. **Validation**: Checks encoding format and dimensions
5. **Parsing**: Extracts user information from filenames
6. **Storage**: Adds valid data to internal lists

### File Processing Logic

#### Filename Convention
```
{name}_{id}_{sequence_number}.npy
```

**Examples**:
- `John_Doe_EMP001_0.npy` → ("John_Doe", "EMP001", "0")
- `Jane_Smith_EMP002_1.npy` → ("Jane_Smith", "EMP002", "1")

#### Data Validation
```python
if isinstance(encoding, np.ndarray) and encoding.shape == (128,):
    # Valid face encoding - add to data
else:
    # Invalid format - skip with message
```

**Validation Criteria**:
- **Data Type**: Must be numpy ndarray
- **Shape**: Must be exactly (128,) dimensions
- **Format**: Must match face_recognition library standard

### Error Handling

#### File Processing Errors
```python
try:
    encoding = np.load(path)
    # Process encoding
except Exception as e:
    message(f"Skipping corrupted file: {filename}")
```

**Handled Scenarios**:
- **Corrupted Files**: Files that cannot be loaded
- **Invalid Format**: Files with wrong data structure
- **Permission Errors**: Files that cannot be accessed
- **Memory Errors**: Files too large to load

#### Data Validation Errors
```python
if isinstance(encoding, np.ndarray) and encoding.shape == (128,):
    # Valid data processing
else:
    message(f"Skipping invalid file (wrong shape): {filename}")
```

**Invalid Data Handling**:
- **Wrong Dimensions**: Arrays not matching 128-element requirement
- **Wrong Type**: Non-array data in files
- **Empty Arrays**: Zero-length or malformed arrays

### Data Organization

#### Parallel Arrays
- **Index Synchronization**: `data[i]` corresponds to `labels[i]`
- **Consistent Ordering**: Maintains relationship between encodings and labels
- **Memory Efficiency**: Separate arrays for different data types

#### Label Structure
```python
(name, id, sequence_number)
```
- **name**: User's name as string
- **id**: User ID as string  
- **sequence_number**: File sequence number as string

### Integration Points

#### With SaveData Module
- Provides existing data for duplicate detection
- Enables comparison during registration
- Maintains data consistency

#### With MatchData Module
- Supplies face encodings for comparison
- Provides user labels for recognition results
- Enables batch recognition operations

#### With Interface Modules
- Loaded once at application startup
- Provides data for all recognition operations
- Reduces file I/O during recognition

## Usage Patterns

### Application Startup
```python
load_data = loadData()
# All face encodings now loaded and ready
```

### Recognition Operations
```python
# Data is available as:
encodings = load_data.data      # List of 128D arrays
user_info = load_data.labels    # List of (name, id, seq) tuples
```

### Duplicate Detection
```python
# Compare new encoding against loaded data
for i, existing_encoding in enumerate(load_data.data):
    name, id, seq = load_data.labels[i]
    # Perform comparison logic
```

## Performance Considerations

### Loading Efficiency
- **Single Load**: Data loaded once at startup
- **Memory Resident**: All encodings kept in memory for fast access
- **Batch Processing**: Processes all files in single operation

### Memory Usage
- **Efficient Storage**: Uses numpy arrays for optimal memory usage
- **Minimal Overhead**: Simple list structure for organization
- **Scalable**: Handles variable numbers of users efficiently

### File I/O Optimization
- **Sequential Access**: Reads files in directory order
- **Error Recovery**: Continues processing despite individual file errors
- **Minimal Disk Access**: Loads data once, keeps in memory

## Error Recovery

### Graceful Degradation
- **Partial Loading**: Continues operation even if some files fail
- **Clear Reporting**: Reports which files had issues
- **No Fatal Errors**: Application continues with available data

### Data Integrity
- **Validation**: Ensures only valid face encodings are loaded
- **Consistency**: Maintains parallel array relationships
- **Recovery**: Skips problematic files without affecting others

## Notes

- **Automatic Loading**: Data loaded immediately upon object creation
- **Memory Resident**: All data kept in memory for performance
- **Validation Focus**: Strict validation ensures data quality
- **Error Resilient**: Continues operation despite individual file failures
- **Simple Interface**: Easy integration with other modules
- **Scalable Design**: Handles growing numbers of users efficiently