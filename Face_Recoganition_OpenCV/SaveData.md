# SaveData & LoadData Module Documentation

## Overview

This module contains two key classes used in a face recognition system:

- **`saveData`**: Encodes and stores facial features from an image to a `.npy` file.
- **`loadData`**: Loads all saved encodings and their corresponding labels from the data directory.

These classes use the `face_recognition` library to extract and compare face encodings.

---

## Class: `saveData`

### Purpose

Encodes a face from a provided image and saves the encoding to disk in a `.npy` file for later recognition.

### Constructor

```python
saveData(name, id, imag)
