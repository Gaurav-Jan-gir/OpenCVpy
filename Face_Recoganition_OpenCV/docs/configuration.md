# Configuration Guide

Complete guide to configuring and customizing the Face Recognition System.

## Table of Contents
- [Configuration Overview](#configuration-overview)
- [Configuration File](#configuration-file)
- [Confidence Settings](#confidence-settings)
- [System Settings](#system-settings)
- [Excel Configuration](#excel-configuration)
- [Camera Settings](#camera-settings)
- [Performance Tuning](#performance-tuning)
- [Advanced Configuration](#advanced-configuration)

## Configuration Overview

The Face Recognition System uses a JSON-based configuration system that allows you to customize:
- Recognition accuracy thresholds
- User interface behavior
- Excel integration settings
- Camera parameters
- Performance options

### Configuration Hierarchy
1. **Default settings** (hardcoded fallbacks)
2. **config.json** (primary configuration file)
3. **Command line arguments** (runtime overrides)
4. **Runtime changes** (via application menu)

## Configuration File

### Default Location
```
Face_Recoganition_OpenCV/
├── config.json          # Main configuration file
├── data/
├── backup/
└── ...
```

### Basic Configuration Structure
```json
{
    "confidence_match": 0.4,
    "confidence_save": 0.4,
    "show_confidence": true,
    "camera_index": 0,
    "excel_auto_save": true,
    "backup_enabled": true,
    "backup_interval": 24
}
```

### Creating Custom Configuration
```bash
# Create custom config file
cp config.json my_config.json

# Use custom config
python run.py "data.xlsx" "my_config.json"
```

## Confidence Settings

### Recognition Confidence (`confidence_match`)

**Purpose**: Controls how strict face matching is during recognition

**Range**: 0.0 - 1.0 (0% - 100%)
- **Lower values** = More strict matching
- **Higher values** = More lenient matching

**Default**: 0.4 (60% similarity required)

**Examples**:
```json
{
    "confidence_match": 0.3,  // 70% similarity - High security
    "confidence_match": 0.4,  // 60% similarity - Balanced (default)
    "confidence_match": 0.6   // 40% similarity - Relaxed
}
```

**Use Cases**:
- **0.2-0.3**: High-security environments, access control
- **0.4-0.5**: General office attendance, balanced accuracy
- **0.6-0.7**: Public areas, relaxed matching

### Saving Confidence (`confidence_save`)

**Purpose**: Controls duplicate detection during user registration

**Range**: 0.0 - 1.0 (0% - 100%)
- **Lower values** = Strict duplicate detection
- **Higher values** = Lenient duplicate detection

**Default**: 0.4 (60% similarity for duplicate detection)

**Examples**:
```json
{
    "confidence_save": 0.3,   // Strict - Rarely allow duplicates
    "confidence_save": 0.4,   // Balanced - Standard duplicate detection
    "confidence_save": 0.6    // Lenient - Allow similar faces
}
```

### Show Confidence (`show_confidence`)

**Purpose**: Display confidence percentages during recognition

**Type**: Boolean (true/false)
**Default**: true

**Examples**:
```json
{
    "show_confidence": true,   // Show percentages
    "show_confidence": false   // Hide percentages
}
```

**Effects**:
- **true**: Display "John Doe (92.5%)" during recognition
- **false**: Display "John Doe" only

## System Settings

### Camera Configuration

#### Camera Index (`camera_index`)
```json
{
    "camera_index": 0        // Default camera (usually built-in)
    "camera_index": 1        // External USB camera
}
```

#### Camera Resolution (`camera_resolution`)
```json
{
    "camera_resolution": {
        "width": 640,
        "height": 480
    }
}
```

#### Camera FPS (`camera_fps`)
```json
{
    "camera_fps": 30         // Frames per second
}
```

### File Paths

#### Data Directory (`data_directory`)
```json
{
    "data_directory": "./data",           // Relative path
    "data_directory": "C:/FaceRecognition/data"  // Absolute path
}
```

#### Backup Directory (`backup_directory`)
```json
{
    "backup_directory": "./backup",
    "backup_directory": "D:/Backups/FaceRecognition"
}
```

## Excel Configuration

### Auto-Save Settings

#### Excel Auto-Save (`excel_auto_save`)
```json
{
    "excel_auto_save": true,    // Automatically save recognition events
    "excel_auto_save": false    // Manual save only
}
```

#### Auto-Save Interval (`excel_save_interval`)
```json
{
    "excel_save_interval": 10   // Save every 10 recognition events
}
```

### Excel File Settings

#### Default Excel Path (`default_excel_path`)
```json
{
    "default_excel_path": "./data/attendance.xlsx"
}
```

#### Excel Sheet Name (`excel_sheet_name`)
```json
{
    "excel_sheet_name": "Attendance"    // Default sheet name
}
```

### Column Configuration

#### Custom Column Headers (`excel_columns`)
```json
{
    "excel_columns": {
        "name": "Employee Name",
        "id": "Employee ID", 
        "timestamp": "Check-in Time",
        "confidence": "Recognition Confidence"
    }
}
```

## Camera Settings

### Detection Parameters

#### Face Detection Model (`face_detection_model`)
```json
{
    "face_detection_model": "hog",       // Faster, less accurate
    "face_detection_model": "cnn"       // Slower, more accurate
}
```

#### Detection Frequency (`detection_frequency`)
```json
{
    "detection_frequency": 5            // Process every 5th frame
}
```

### Image Processing

#### Image Quality (`image_quality`)
```json
{
    "image_quality": {
        "blur_threshold": 100,           // Minimum blur threshold
        "brightness_min": 50,            // Minimum brightness
        "brightness_max": 200            // Maximum brightness
    }
}
```

#### Face Size Requirements (`face_size`)
```json
{
    "face_size": {
        "min_width": 100,               // Minimum face width in pixels
        "min_height": 100,              // Minimum face height in pixels
        "max_faces": 5                  // Maximum faces to process
    }
}
```

## Performance Tuning

### Processing Options

#### Multi-Threading (`enable_multithreading`)
```json
{
    "enable_multithreading": true,      // Enable parallel processing
    "max_threads": 4                    // Maximum thread count
}
```

#### Memory Management (`memory_settings`)
```json
{
    "memory_settings": {
        "cache_encodings": true,        // Cache face encodings in memory
        "max_cache_size": 1000,         // Maximum cached encodings
        "garbage_collection": true      // Enable automatic cleanup
    }
}
```

### Recognition Optimization

#### Batch Processing (`batch_processing`)
```json
{
    "batch_processing": {
        "enabled": true,
        "batch_size": 10,               // Process faces in batches
        "timeout": 5000                 // Batch timeout in milliseconds
    }
}
```

#### Recognition Speed (`recognition_speed`)
```json
{
    "recognition_speed": {
        "skip_frames": 2,               // Skip frames for speed
        "resize_factor": 0.5,           // Resize images for speed
        "fast_mode": false              // Enable fast recognition mode
    }
}
```

## Advanced Configuration

### Backup Settings

#### Automatic Backup (`backup_settings`)
```json
{
    "backup_settings": {
        "enabled": true,
        "interval_hours": 24,           // Backup every 24 hours
        "max_backups": 30,              // Keep 30 most recent backups
        "compress": true,               // Compress backup files
        "include_excel": true,          // Include Excel files
        "include_images": false         // Include captured images
    }
}
```

### Logging Configuration

#### Application Logging (`logging`)
```json
{
    "logging": {
        "enabled": true,
        "level": "INFO",                // DEBUG, INFO, WARNING, ERROR
        "file": "face_recognition.log",
        "max_size_mb": 50,
        "backup_count": 5
    }
}
```

### Security Settings

#### Access Control (`security`)
```json
{
    "security": {
        "admin_mode": false,            // Require admin for config changes
        "encryption": false,            // Encrypt face encoding files
        "access_log": true,             // Log all access attempts
        "failed_attempts_limit": 5      // Max failed recognition attempts
    }
}
```

## Environment-Specific Configurations

### High-Security Environment
```json
{
    "confidence_match": 0.25,
    "confidence_save": 0.25,
    "show_confidence": true,
    "face_detection_model": "cnn",
    "security": {
        "admin_mode": true,
        "encryption": true,
        "access_log": true,
        "failed_attempts_limit": 3
    },
    "backup_settings": {
        "enabled": true,
        "interval_hours": 1,
        "max_backups": 168
    }
}
```

### Fast Processing Environment
```json
{
    "confidence_match": 0.5,
    "confidence_save": 0.5,
    "face_detection_model": "hog",
    "recognition_speed": {
        "skip_frames": 3,
        "resize_factor": 0.25,
        "fast_mode": true
    },
    "detection_frequency": 10,
    "enable_multithreading": true,
    "max_threads": 8
}
```

### Large-Scale Environment
```json
{
    "memory_settings": {
        "cache_encodings": true,
        "max_cache_size": 5000,
        "garbage_collection": true
    },
    "batch_processing": {
        "enabled": true,
        "batch_size": 50,
        "timeout": 10000
    },
    "excel_save_interval": 100,
    "backup_settings": {
        "enabled": true,
        "interval_hours": 6,
        "compress": true
    }
}
```

## Configuration Validation

### Validation Rules

#### Confidence Values
- Must be between 0.0 and 1.0
- `confidence_match` should typically be ≥ `confidence_save`

#### File Paths
- Must be valid directory paths
- Write permissions required for data directories

#### Camera Settings
- Camera index must be valid integer
- Resolution values must be positive

### Validation Script
```python
import json

def validate_config(config_path):
    """Validate configuration file"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Validate confidence values
        for key in ['confidence_match', 'confidence_save']:
            if key in config:
                value = config[key]
                if not (0.0 <= value <= 1.0):
                    print(f"Error: {key} must be between 0.0 and 1.0")
                    return False
        
        # Validate camera index
        if 'camera_index' in config:
            if not isinstance(config['camera_index'], int):
                print("Error: camera_index must be an integer")
                return False
        
        print("Configuration valid!")
        return True
        
    except json.JSONDecodeError:
        print("Error: Invalid JSON format")
        return False
    except FileNotFoundError:
        print("Error: Configuration file not found")
        return False

# Usage
validate_config("config.json")
```

## Configuration Best Practices

### 1. Start with Defaults
- Use default configuration initially
- Make incremental changes
- Test thoroughly after changes

### 2. Environment-Specific Configs
- Create separate configs for different environments
- Use version control for configuration files
- Document configuration changes

### 3. Performance Monitoring
- Monitor recognition accuracy after changes
- Track processing speed and resource usage
- Use logging to identify issues

### 4. Security Considerations
- Protect configuration files from unauthorized access
- Use encryption for sensitive settings
- Regular backup of configuration files

### 5. Testing Configuration
- Test configuration changes in controlled environment
- Validate all settings before production deployment
- Have rollback plan for configuration changes

## Troubleshooting Configuration Issues

### Common Problems

#### Recognition Too Strict
**Symptoms**: Users not being recognized
**Solution**: Increase `confidence_match` value (0.4 → 0.5)

#### Too Many False Positives
**Symptoms**: Wrong users being recognized
**Solution**: Decrease `confidence_match` value (0.5 → 0.3)

#### Duplicate Registration Issues
**Symptoms**: Same user registered multiple times
**Solution**: Decrease `confidence_save` value (0.5 → 0.3)

#### Performance Issues
**Symptoms**: Slow recognition, high CPU usage
**Solution**: Enable fast mode, reduce resolution, increase skip frames

### Configuration Reset
```python
# Reset to default configuration
default_config = {
    "confidence_match": 0.4,
    "confidence_save": 0.4,
    "show_confidence": True,
    "camera_index": 0,
    "excel_auto_save": True,
    "backup_enabled": True
}

with open("config.json", "w") as f:
    json.dump(default_config, f, indent=4)
```

This configuration guide provides comprehensive information for customizing the Face Recognition System to meet specific requirements and environments.
