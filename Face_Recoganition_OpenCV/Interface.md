# Interface.py Documentation

## Overview

`Interface.py` is the main interface script for the **Face Recognition System**. It provides a command-line menu for registering and recognizing users using a webcam or an image. It interacts with three supporting modules:

- `SaveData.py` – Handles encoding and saving face data.
- `LoadData.py` – Loads previously stored face data.
- `MatchData.py` – Matches input face data against saved data.

---

## Features

### 1. Register a New User via Camera
- Activates the webcam and warms it up.
- Prompts user to press `s` to save the current frame as an image.
- Asks for user's name and ID.
- Saves encoded face data as a `.npy` file using `SaveData`.

### 2. Register a New User via Image
- User provides the path to an existing image.
- Asks for user's name and ID.
- Saves encoded face data via `SaveData`.

### 3. Recognize a User
- Opens the webcam and captures a frame on pressing `s`.
- Encodes the face and compares it with stored data using `MatchData`.
- Displays the name and ID of the matched user if a match is found.

### 4. Exit
- Exits the application safely.

---

## How It Works

1. Launch the script:
   ```bash
   python Interface.py
