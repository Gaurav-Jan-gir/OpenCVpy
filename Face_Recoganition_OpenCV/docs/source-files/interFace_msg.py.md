# interFace_msg.py - User Interface Message Handler

**File Path**: `interFace_msg.py`  
**Purpose**: Provides user interface messaging functions and input handling utilities

## Overview

The `interFace_msg.py` module contains utility functions for handling user messages, prompts, and data input throughout the face recognition system. It provides a consistent interface for user communication and screen management.

## Dependencies

```python
import os
```

## Functions

### Message Display

```python
def message(message, input_key=False):
```
**Purpose**: Display messages to user with optional pause

**Parameters**:
- `message`: Text message to display
- `input_key`: Boolean flag to wait for user input (default: False)

**Behavior**:
- Prints the provided message to console
- If `input_key=True`:
  - Displays "Press any key to continue..." prompt
  - Waits for user input
  - Clears screen after input (Windows: `cls`, Unix: `clear`)

**Usage Examples**:
```python
# Simple message
message("Operation completed successfully")

# Message with pause and screen clear
message("Error occurred", input_key=True)
```

### Save Data Interface

```python
def interfaceSaveData(name, id, conf, showConfidence=False):
```
**Purpose**: Handle user decisions during face registration when duplicate is detected

**Parameters**:
- `name`: Existing user's name
- `id`: Existing user's ID  
- `conf`: Confidence score of match (0.0 to 1.0)
- `showConfidence`: Whether to display confidence percentage (default: False)

**Display Options**:

**Without Confidence Display**:
```
User already exists with
Name: John Doe and ID: EMP001
Press 1 to Save Current data with existing Name and ID
Press 2 to Save current data with new Name and ID
Press 3 to Update existing data with new Name and ID
Press any other key to abort saving current data
```

**With Confidence Display**:
```
User already exists with
Name: John Doe and ID: EMP001 with confidence 85.50%
Press 1 to Save Current data with existing Name and ID
Press 2 to Save current data with new Name and ID  
Press 3 to Update existing data with new Name and ID
Press any other key to abort saving current data
```

**Return Values**:
- `1`: Save with existing name and ID
- `2`: Save with new name and ID
- `3`: Update existing data with new name and ID
- `0`: Abort operation (any other key)

**Confidence Calculation**:
- Converts distance score to percentage: `(1-conf)*100`
- Displays with 2 decimal precision

### User Data Input

```python
def input_data():
```
**Purpose**: Collect user name and ID for face registration

**Prompts**:
- "Enter User Name for the face detected: "
- "Enter User ID for the face detected: "

**Returns**:
- `tuple`: (name, id) as strings

**Usage**:
```python
name, user_id = input_data()
print(f"Registered: {name} with ID: {user_id}")
```

## Cross-Platform Support

### Screen Clearing
```python
os.system('cls' if os.name == 'nt' else 'clear')
```
- **Windows**: Uses `cls` command
- **Unix/Linux/Mac**: Uses `clear` command
- **Detection**: Based on `os.name` value

## Integration Points

### With SaveData Module
- Called during registration process
- Handles duplicate user detection decisions
- Provides user input for name and ID

### With Interface Modules
- Used throughout application for user feedback
- Consistent message formatting
- Screen management between operations

### With Error Handling
- Standard error message display
- User acknowledgment for error conditions
- Clean screen transitions

## Usage Patterns

### Simple Notification
```python
message("Face registration completed successfully")
```

### Error with User Acknowledgment  
```python
message("Camera not found. Please check connection.", input_key=True)
```

### Duplicate Detection Workflow
```python
choice = interfaceSaveData("John Doe", "EMP001", 0.15, showConfidence=True)
if choice == 1:
    # Use existing data
elif choice == 2:
    # Get new name and ID
    name, user_id = input_data()
elif choice == 3:
    # Update existing
    name, user_id = input_data()
else:
    # Abort operation
```

## Design Principles

### Consistency
- Uniform message formatting across application
- Standardized user input patterns
- Consistent screen management

### User Experience
- Clear prompts and instructions
- Intuitive option numbering
- Visual separation between operations

### Flexibility
- Optional confidence display
- Configurable pause behavior
- Cross-platform compatibility

## Error Handling

### Input Validation
- Accepts any string input for names and IDs
- No length restrictions or format validation
- User responsible for appropriate input

### System Commands
- Handles both Windows and Unix screen clearing
- Graceful degradation if system commands fail

## Notes

- All functions are standalone utilities
- No class structure - function-based module
- Minimal dependencies for maximum portability
- Designed for console-based interaction
- Thread-safe for multiprocessing environments
