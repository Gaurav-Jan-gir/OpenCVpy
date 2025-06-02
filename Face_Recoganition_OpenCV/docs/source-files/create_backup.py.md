# create_backup.py - Backup and Recovery System

**File Path**: `create_backup.py`  
**Purpose**: Handles backup creation, restoration, and removal for data protection

## Overview

The `create_backup.py` module provides comprehensive backup functionality for the face recognition system, including automatic backup creation, restoration capabilities, and cleanup operations to ensure data integrity and recovery options.

## Dependencies

```python
import shutil
import os
import pandas as pd
```

## Core Functions

### Backup Creation

```python
def create_backup(data_dir, excel_file, backup_dir):
```
**Purpose**: Create comprehensive backup of system data

**Parameters**:
- `data_dir`: Path to data directory containing `.npy` files
- `excel_file`: Path to Excel attendance file
- `backup_dir`: Target backup directory path

**Process**:
1. Creates backup directory if it doesn't exist
2. Backs up Excel file to `excel/` subdirectory
3. Backs up all `.npy` files to `npy/` subdirectory  
4. Exports Excel data to CSV format for additional safety

**Directory Structure Created**:
```
backup_dir/
├── excel/
│   └── data.xlsx
├── npy/
│   ├── John_Doe_EMP001_0.npy
│   ├── Jane_Smith_EMP002_0.npy
│   └── ...
└── data_backup.csv
```

### Backup Removal

```python
def remove_backup(backup_dir):
```
**Purpose**: Clean up backup directory after successful operation

**Parameters**:
- `backup_dir`: Path to backup directory to remove

**Behavior**:
- Completely removes backup directory and all contents
- Provides confirmation message on successful removal
- Handles case where backup directory doesn't exist

### Backup Restoration

```python
def restore_backup(backup_dir, data_dir, excel_file):
```
**Purpose**: Restore system data from backup

**Parameters**:
- `backup_dir`: Path to backup directory
- `data_dir`: Target data directory for restoration
- `excel_file`: Target Excel file path for restoration

**Process**:
1. Validates backup directory existence
2. Restores Excel file from backup
3. Restores all `.npy` face encoding files
4. Provides detailed restoration feedback

## Specialized Backup Functions

### Excel File Backup

```python
def backup_excel(excel_file, backup_dir):
```
**Purpose**: Create backup of Excel attendance file

**Process**:
- Creates `excel/` subdirectory in backup location
- Copies Excel file with original filename preserved
- Handles missing source file gracefully

### NPY Files Backup

```python
def backup_npy(data_dir, backup_dir):
```
**Purpose**: Backup all face encoding files

**Process**:
- Creates `npy/` subdirectory in backup location
- Copies all `.npy` files from data directory
- Preserves original filenames and structure

### CSV Export

```python
def export_csv(excel_file, csv_file):
```
**Purpose**: Export Excel data to CSV format for additional backup

**Features**:
- Creates human-readable backup format
- Handles Excel file reading errors
- Provides alternative access to attendance data

## Restoration Functions

### Excel File Restoration

```python
def restore_excel(excel_file, backup_dir):
```
**Purpose**: Restore Excel file from backup

**Process**:
1. Looks for Excel file in `backup_dir/excel/` directory
2. Matches filename with target Excel file
3. Copies backup file to target location
4. Provides restoration confirmation

### NPY Files Restoration

```python
def restore_npy(data_dir, backup_dir):
```
**Purpose**: Restore face encoding files from backup

**Process**:
1. Scans `backup_dir/npy/` directory for `.npy` files
2. Copies all found files to target data directory
3. Preserves original filename structure
4. Provides restoration feedback for each file

## Error Handling

### File Operations
- **Missing source files**: Graceful handling with informative messages
- **Permission errors**: Reports access issues during backup/restore
- **Corrupt files**: Skips problematic files and continues operation

### Directory Management
- **Missing directories**: Automatic creation as needed
- **Access permissions**: Validates read/write access
- **Space availability**: Assumes sufficient disk space

### Backup Validation
- **Backup existence**: Validates backup directory before restoration
- **File integrity**: Basic existence checking for backup files
- **Path validation**: Ensures valid file and directory paths

## Usage Patterns

### Pre-Operation Backup
```python
try:
    create_backup(data_dir, excel_path, backup_dir)
    # Perform risky operation
    remove_backup(backup_dir)  # Cleanup on success
except Exception as e:
    # Offer restoration on failure
    restore_backup(backup_dir, data_dir, excel_path)
```

### Manual Restoration
```python
if user_wants_restore:
    restore_backup(backup_dir, data_dir, excel_path)
```

### Cleanup After Success
```python
if operation_successful:
    remove_backup(backup_dir)
```

## Integration Points

### With run.py
- Called before main application launch
- Provides safety net for application execution
- Handles cleanup and restoration logic

### With Data Modules
- Protects face encoding files (`.npy`)
- Safeguards Excel attendance data
- Ensures data consistency across operations

## Safety Features

### Data Integrity
- Multiple backup formats (Excel + CSV)
- Complete directory structure preservation
- Filename and path consistency maintenance

### Recovery Options
- Granular restoration (Excel or NPY files separately)
- Complete system restoration capability
- User confirmation and feedback throughout process

### Cleanup Management
- Automatic backup removal on success
- Space-efficient operation
- No orphaned backup directories

## Performance Considerations

### File Operations
- Uses `shutil` for efficient file copying
- Batch operations for multiple files
- Minimal memory footprint for large files

### Directory Handling
- Recursive directory operations
- Efficient traversal of data structures
- Optimized for typical face recognition data sizes

## Notes

- Designed for automatic integration with main application flow
- Provides both programmatic and manual recovery options
- Handles edge cases gracefully without stopping system operation
- Creates timestamped backup directories for organization
- Supports both Windows and Unix file systems
- No compression used - direct file copying for reliability
