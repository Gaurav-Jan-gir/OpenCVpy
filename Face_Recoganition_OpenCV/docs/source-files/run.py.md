# run.py - Main Application Entry Point

**File Path**: `run.py`  
**Purpose**: Main entry point for the Face Recognition system with backup management

## Overview

The `run.py` file serves as the primary entry point for the Face Recognition application. It handles command-line arguments, manages backup operations, and initializes the main interface.

## Dependencies

```python
import Interface_excel as Interface
import sys
import create_backup as backup
import os
```

## Command Line Usage

```bash
# Basic usage with default files
python run.py

# With custom Excel file
python run.py "path/to/custom_file.xlsx"

# With custom Excel and config files  
python run.py "path/to/custom_file.xlsx" "path/to/config.json"
```

## Key Features

### 1. Command Line Argument Processing

**Excel File Path (argv[1])**:
- Validates file existence
- Checks for `.xlsx` extension
- Provides fallback to default path on error
- Interactive user confirmation for invalid paths

**Config File Path (argv[2])**:
- Optional configuration file specification
- Defaults to `config.json` if not provided

### 2. Directory Setup

**Default Paths**:
```python
backup_dir = os.path.join(os.getcwd(), 'backup')    # Backup directory
data_dir = os.path.join(os.getcwd(), 'data')        # Data directory
excel_path = os.path.join(os.getcwd(),'data', 'data.xlsx')  # Default Excel file
```

### 3. Backup Management

**Pre-execution Backup**:
- Creates backup before running the main application
- Backs up both data directory and Excel file
- Handles backup creation errors gracefully

**Post-execution Cleanup**:
- Removes backup on successful completion
- Provides restore option on application failure

## Error Handling

### File Validation
- **Non-existent Excel file**: Prompts user to continue with default
- **Invalid file format**: Validates `.xlsx` extension
- **User choice**: Interactive confirmation for proceeding

### Backup Operations
- **Backup creation failure**: Option to continue without backup
- **Application failure**: Automatic backup restoration offer

### Exception Management
```python
try:
    Interface.interFace(excel_path , config_path)
    backup.remove_backup(backup_dir)
except Exception as e:
    print(f"An error occurred: {e}")
    # Restore backup option provided
```

## Application Flow

1. **Parse command line arguments**
2. **Validate Excel file path and format**
3. **Set configuration file path**
4. **Create system backup**
5. **Launch main interface**
6. **Clean up backup on success**
7. **Offer backup restoration on failure**

## Integration Points

- **Interface_excel.interFace()**: Main application interface
- **create_backup module**: Backup and restore operations
- **System directories**: Automatic creation of required folders

## Exit Conditions

- Invalid file paths (user chooses not to continue)
- Backup creation failure (user chooses not to continue)
- Application exceptions (after backup restoration option)

## Notes

- All file paths are converted to absolute paths using `os.path.join()`
- Interactive prompts ensure user consent for fallback operations
- Backup system provides data safety during application execution
- Error messages include specific details for troubleshooting
