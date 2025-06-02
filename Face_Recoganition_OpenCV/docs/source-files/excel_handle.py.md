# excel_handle.py - Excel File Management for Attendance Logging

**File Path**: `excel_handle.py`  
**Purpose**: Manages Excel file operations for attendance tracking and user data logging

## Overview

The `excel_handle.py` module provides comprehensive Excel file management for the face recognition system, handling attendance logging, user data management, and Excel file operations with error recovery and data integrity features.

## Dependencies

```python
from openpyxl import Workbook, load_workbook, utils
from datetime import datetime
import time
import sys
import os
```

## Class: Excel_handle

### Constructor
```python
def __init__(self, path):
```

**Parameters**:
- `path`: Path to Excel file for attendance logging

**Initialization Process**:
1. Stores file path
2. Creates or loads Excel workbook
3. Sets active worksheet
4. Validates file integrity

**Error Handling**:
- Exits application if Excel file cannot be created or loaded
- Provides user option to recreate corrupted files

### Excel File Creation and Management

```python
def create_excel_file(self):
```
**Purpose**: Create new Excel file or load existing one with error recovery

**New File Creation**:
```python
if not os.path.exists(self.path):
    wb = Workbook()
    ws = wb.active
    ws.title = "User Data"
    ws.append(["ID", "Name", "Confidence", "Count"])
```

**Default Structure**:
| Column | Purpose | Width |
|--------|---------|--------|
| A (ID) | User identification | ID length + 3 |
| B (Name) | User name | Name length + 3 |
| C (Confidence) | Recognition confidence | Confidence length + 3 |
| D (Count) | Recognition count | Count length + 3 |

**Column Width Management**:
```python
ws.column_dimensions['A'].width = len("ID") + 3
ws.column_dimensions['B'].width = len("Name") + 3
ws.column_dimensions['C'].width = len("Confidence") + 3
ws.column_dimensions['D'].width = len("Count") + 3
```

### Error Recovery System

**Corruption Handling**:
```python
except Exception as e:
    print(f"Error loading Excel File: {e}")
    print("Do you want to delete the existing file and create a new one? (y/n)")
    choice = input().strip().lower()
    if choice == 'y':
        # Recreate file after deletion
```

**Recovery Process**:
1. **Detection**: Catches Excel file loading errors
2. **User Confirmation**: Asks permission to recreate file
3. **Safe Deletion**: Removes corrupted file after confirmation
4. **Recreation**: Creates new file with default structure
5. **Permission Handling**: Manages file access permission errors

**Permission Error Management**:
```python
except PermissionError as e:
    print(f"Permission Error: {e}. Please close the file and try again.")
    return None
```

### Data Access Methods

```python
def get_row_number(self, id):
```
**Purpose**: Find row number for specific user ID

**Process**:
- Iterates through rows starting from row 2 (skips header)
- Compares cell values in ID column (column 1)
- Returns row number if found, None if not found

**Usage Pattern**:
```python
row_num = excel_handle.get_row_number("EMP001")
if row_num:
    # User exists, update data
else:
    # New user, append new row
```

### Data Operations

#### Row Retrieval
```python
for rn in range(2, self.ws.max_row + 1):  # Start from row 2 (skip header)
    cell_value = self.ws.cell(row=rn, column=1).value  # ID is in column 1
    if cell_value == id:
        return rn
```

#### Data Reading
- **Cell Access**: `self.ws.cell(row=rn, column=col).value`
- **Range Operations**: Supports batch data operations
- **Header Handling**: Automatically skips header row in searches

#### Data Writing
- **Cell Updates**: Direct cell value modification
- **Row Appending**: Adding new user records
- **Batch Operations**: Multiple cell updates in single operation

### File System Integration

#### Path Management
- **Absolute Paths**: Handles full file paths
- **Directory Validation**: Ensures parent directories exist
- **Cross-platform**: Compatible with Windows and Unix paths

#### File Locking
- **Concurrent Access**: Handles Excel file being open in other applications
- **Permission Management**: Provides clear error messages for access issues
- **Recovery Options**: Offers solutions for common file access problems

### Worksheet Structure

#### Header Row (Row 1)
```
| ID | Name | Confidence | Count |
```

#### Data Rows (Row 2+)
```
| EMP001 | John Doe | 85.5 | 15 |
| EMP002 | Jane Smith | 92.3 | 8 |
```

#### Column Specifications
- **ID Column (A)**: Primary identifier for user lookup
- **Name Column (B)**: Human-readable user name
- **Confidence Column (C)**: Recognition confidence percentage
- **Count Column (D)**: Number of recognition events

### Integration Points

#### With Interface_excel Module
- Provides Excel operations for attendance logging
- Handles user data storage and retrieval
- Supports attendance tracking features

#### With Recognition System
- Logs recognition events automatically
- Updates user statistics
- Maintains recognition history

#### With Backup System
- Integrates with backup and restore operations
- Ensures data safety during operations
- Supports recovery from backup files

### Performance Considerations

#### Memory Management
- **Worksheet Caching**: Keeps active worksheet in memory
- **Efficient Access**: Direct cell addressing for fast operations
- **Minimal Loading**: Only loads necessary worksheet data

#### File Operations
- **Batch Updates**: Minimizes file save operations
- **Efficient Searching**: Linear search optimized for typical user counts
- **Resource Management**: Proper workbook closing and cleanup

### Error Handling Scenarios

#### Common Error Types
1. **File Access Errors**: Permission denied, file in use
2. **Corruption Errors**: Invalid Excel format, damaged files
3. **Data Errors**: Invalid cell values, format mismatches
4. **System Errors**: Disk full, network issues

#### Recovery Strategies
- **Automatic Retry**: For temporary access issues
- **User Confirmation**: For destructive operations
- **Graceful Degradation**: Continue operation with limited functionality
- **Clear Messaging**: Detailed error descriptions and solutions

### Usage Patterns

#### Basic File Operations
```python
excel_handle = Excel_handle("attendance.xlsx")
if excel_handle.wb is None:
    # Handle initialization failure
    sys.exit(1)
```

#### User Data Management
```python
# Check if user exists
row_num = excel_handle.get_row_number("EMP001")
if row_num:
    # Update existing user
    excel_handle.ws.cell(row=row_num, column=4).value += 1  # Increment count
else:
    # Add new user
    excel_handle.ws.append(["EMP001", "John Doe", "85.5", "1"])
```

#### File Recovery
```python
# Automatic recovery on corruption
excel_handle = Excel_handle("corrupted_file.xlsx")
# User prompted for recovery action
# File recreated if confirmed
```

## Notes

- **Data Integrity**: Ensures consistent Excel file structure
- **Error Resilience**: Comprehensive error handling and recovery
- **User Interaction**: Interactive recovery for corrupted files
- **Performance Optimized**: Efficient data access and manipulation
- **Cross-platform**: Compatible file operations across operating systems
- **Integration Ready**: Designed for seamless integration with recognition system