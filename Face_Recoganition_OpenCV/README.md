# Face Recognition System Documentation

Welcome to the **Face Recognition System** - a comprehensive Python-based solution for face detection, recognition, and attendance tracking using OpenCV and advanced computer vision techniques.

## 📚 Documentation Index

- [**Installation Guide**](./installation.md) - Setup and dependencies
- [**Quick Start Guide**](./quick-start.md) - Get started in 5 minutes
- [**User Manual**](./user-manual.md) - Complete feature guide
- [**API Reference**](./api-reference.md) - Technical documentation
- [**Configuration**](./configuration.md) - Settings and customization
- [**Troubleshooting**](./troubleshooting.md) - Common issues and solutions
- [**Development Guide**](./development.md) - For developers and contributors

## 🎯 What This System Does

### Core Features
- **👤 Face Registration**: Register users via webcam or image files
- **🔍 Face Recognition**: Real-time and manual face detection
- **📊 Excel Integration**: Automatic attendance logging to Excel files
- **⚙️ Configurable Settings**: Adjustable confidence levels and parameters
- **🔄 Backup System**: Automatic data backup and recovery
- **🎥 Multi-Mode Capture**: Real-time continuous or manual capture modes

### Recognition Modes
1. **Real-time Recognition**: Continuous camera feed processing
2. **Manual Capture**: Press-to-capture recognition
3. **Image-based Registration**: Upload existing photos for registration

## 🏗️ System Architecture

```
Face Recognition System
├── Core Components
│   ├── Face Detection (OpenCV)
│   ├── Face Encoding (face_recognition)
│   ├── Data Storage (.npy files)
│   └── Excel Integration (openpyxl)
├── User Interface
│   ├── Command Line Interface
│   ├── Camera Controls
│   └── Excel Operations Menu
└── Data Management
    ├── Automatic Backup
    ├── Configuration Management
    └── Error Recovery
```

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install face_recognition opencv-python openpyxl numpy

# 2. Run with default settings
python run.py

# 3. Run with custom Excel file
python run.py "path/to/your/attendance.xlsx"

# 4. Run with custom Excel and config
python run.py "attendance.xlsx" "config.json"
```

## 📋 Menu Options

When you run the system, you'll see:

```
Welcome to the face recognition system
1. Register a new user via Camera
2. Register a new user via Image  
3. Start Recognition
4. Check if User Data exist or not
5. Configure Confidence Levels (Default 60%)
6. Operate on data in Excel
7. Exit
```

## 🔧 Key Components

| Component | Purpose | Documentation |
|-----------|---------|---------------|
| `run.py` | Main entry point | [User Manual](./user-manual.md) |
| `Interface_excel.py` | Core interface logic | [API Reference](./api-reference.md) |
| `camera.py` | Camera operations | [API Reference](./api-reference.md) |
| `excel_handle.py` | Excel file management | [API Reference](./api-reference.md) |
| `MatchData.py` | Face matching algorithms | [API Reference](./api-reference.md) |
| `SaveData.py` | Data storage operations | [API Reference](./api-reference.md) |
| `LoadData.py` | Data loading operations | [API Reference](./api-reference.md) |

## 📁 Project Structure

```
Face_Recoganition_OpenCV/
├── docs/                    # Documentation (this folder)
├── data/                    # User face data (.npy files)
├── backup/                  # Automatic backups
├── capture_frames/          # Temporary camera captures
├── config.json             # System configuration
├── run.py                  # Main application entry
├── Interface_excel.py      # Core interface
├── camera.py               # Camera operations
├── excel_handle.py         # Excel management
├── MatchData.py            # Face matching
├── SaveData.py             # Data saving
├── LoadData.py             # Data loading
└── create_backup.py        # Backup utilities
```

## 🤝 Getting Help

- **Installation Issues**: See [Installation Guide](./installation.md)
- **Usage Questions**: Check [User Manual](./user-manual.md)
- **Technical Problems**: Visit [Troubleshooting](./troubleshooting.md)
- **Development**: Read [Development Guide](./development.md)

## 📄 License

This project is open-source and available for educational and research purposes.

---

**Last Updated**: June 2, 2025
**Version**: 2.0
**Python**: 3.7+
**Dependencies**: OpenCV, face_recognition, openpyxl, numpy
