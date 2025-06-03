# Recover.py - Data Recovery Utility

**File Path**: `Recover.py`  
**Purpose**: Utility script for recovering and validating corrupted face encoding data files

## Overview

The `Recover.py` module is a standalone utility script designed to recover valid face encoding data from potentially corrupted `.npy` files. It validates the structure and format of face encoding files and creates clean copies of valid data.

## Dependencies

```python
import os
import numpy as np
```

## Core Functionality

### Data Recovery Process

**Source Directory**: `data/` (original data location)
**Target Directory**: `recovered_data/` (cleaned data location)

### Recovery Algorithm

```python
old_dir = 'data'
new_dir = 'recovered_data'
os.makedirs(new_dir, exist_ok=True)

for file in os.listdir(old_dir):
    if file.endswith('.npy'):
        old_path = os.path.join(old_dir, file)
        new_path = os.path.join(new_dir, file)
        try:
            arr = np.load(old_path, allow_pickle=True)
            # Only save if it's a valid face encoding
            if isinstance(arr, np.ndarray) and arr.shape == (128,):
                np.save(new_path, arr)
                print(f"Recovered: {file}")
            else:
                print(f"Invalid shape, skipping: {file}")
        except Exception as e:
            print(f"Failed to recover {file}: {e}")
```

## Validation Criteria

### Face Encoding Requirements
1. **Data Type**: Must be `numpy.ndarray`
2. **Shape**: Must be exactly `(128,)` - standard face encoding vector size
3. **Loadability**: File must be readable without corruption

### File Processing
- **File Extension**: Only processes `.npy` files
- **Error Handling**: Catches and reports loading errors
- **Validation**: Ensures data meets face encoding standards

## Recovery Operations

### Valid File Processing
**Criteria Met**:
- File loads successfully
- Data is numpy array
- Shape is (128,) - face_recognition library standard

**Action**:
- Copies file to `recovered_data/` directory
- Maintains original filename
- Reports successful recovery

### Invalid File Handling
**Common Issues**:
- **Wrong Shape**: Arrays with incorrect dimensions
- **Corrupt Data**: Files that cannot be loaded
- **Wrong Type**: Non-array data types

**Action**:
- Skips file (does not copy)
- Reports reason for skipping
- Continues with next file

### Error Scenarios
**File Access Errors**:
- Permission denied
- File in use by another process
- Disk read errors

**Data Corruption**:
- Partially written files
- Invalid numpy format
- Pickled objects instead of arrays

## Output Messages

### Success Messages
```
Recovered: John_Doe_EMP001_0.npy
Recovered: Jane_Smith_EMP002_0.npy
```

### Validation Failures
```
Invalid shape, skipping: corrupted_file.npy
```

### Error Messages
```
Failed to recover broken_file.npy: Invalid file format
Failed to recover locked_file.npy: Permission denied
```

## Use Cases

### Data Corruption Recovery
- **System Crashes**: Recover from unexpected shutdowns
- **File System Errors**: Handle disk corruption issues
- **Import Problems**: Clean up malformed data files

### Data Migration
- **System Upgrades**: Migrate data to new versions
- **Format Validation**: Ensure all files meet current standards
- **Cleanup Operations**: Remove invalid data files

### Quality Assurance
- **Data Integrity**: Validate face encoding consistency
- **Batch Processing**: Check multiple files simultaneously
- **Format Compliance**: Ensure standard compliance

## Directory Structure

### Before Recovery
```
data/
├── John_Doe_EMP001_0.npy          # Valid file
├── Jane_Smith_EMP002_0.npy        # Valid file
├── corrupted_user.npy             # Invalid shape
├── broken_file.npy                # Unreadable
└── temp_file.npy                  # Wrong format
```

### After Recovery
```
recovered_data/
├── John_Doe_EMP001_0.npy          # Recovered valid file
└── Jane_Smith_EMP002_0.npy        # Recovered valid file
```

## Integration with Main System

### Manual Recovery Process
1. **Stop Application**: Ensure no files are in use
2. **Run Recovery**: Execute `python Recover.py`
3. **Review Results**: Check recovery messages
4. **Replace Data**: Move recovered files back to `data/` directory
5. **Restart Application**: Resume normal operations

### Backup Restoration Alternative
- Recovery can be used instead of backup restoration
- Provides more granular control than full backup restore
- Allows selective recovery of valid data only

## Performance Considerations

### File Processing
- **Sequential Processing**: Processes files one by one
- **Memory Efficient**: Loads only one file at a time
- **Fast Validation**: Quick shape and type checking

### Disk Operations
- **Read Operations**: Original files remain unchanged
- **Write Operations**: Creates new copies only for valid files
- **Space Requirements**: Requires disk space for recovered files

## Safety Features

### Non-Destructive
- **Original Preservation**: Source files remain untouched
- **Copy-Based**: Creates new files rather than modifying originals
- **Reversible**: Can always return to original state

### Validation
- **Strict Checking**: Only accepts properly formatted face encodings
- **Error Reporting**: Clear feedback on processing results
- **Selective Recovery**: Recovers only valid data

## Limitations

### Processing Scope
- **NPY Files Only**: Only processes numpy array files
- **Face Encodings Only**: Validates specifically for 128-dimensional vectors
- **No Excel Recovery**: Does not handle Excel file corruption

### Error Recovery
- **Cannot Fix Corruption**: Cannot repair truly corrupted data
- **No Format Conversion**: Cannot convert between different formats
- **Limited Diagnostics**: Basic error reporting only

## Notes

- **Standalone Utility**: Runs independently of main application
- **Safe Operation**: Non-destructive data recovery process
- **Quick Validation**: Fast processing for data integrity checking
- **Standard Compliance**: Ensures face_recognition library compatibility
- **Simple Usage**: No command line arguments required
- **Clear Feedback**: Provides detailed status messages during processing
