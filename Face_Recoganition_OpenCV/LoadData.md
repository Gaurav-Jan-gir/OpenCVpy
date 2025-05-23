# LoadData.py Documentation

## Overview

`LoadData.py` defines the `loadData` class, which is responsible for reading and loading all the previously stored face encoding data and their corresponding labels (name and ID) from the `data/` directory. This module is used by the face recognition system to retrieve known face encodings for comparison.

---

## Class: `loadData`

### Attributes

- `data` – A list that stores all loaded face encodings (`numpy.ndarray`).
- `labels` – A list that stores tuples in the format `(name, id)` associated with each encoding.

### Methods

#### `__init__(self)`
- Initializes the `data` and `labels` lists.
- Automatically calls the `load()` method to populate them.

#### `load(self)`
- Scans the `data/` directory for `.npy` files.
- Loads each `.npy` file into the `data` list using `numpy.load()`.
- Extracts the `name` and `id` from the filename (e.g., `Alice_123.npy` → `('Alice', '123')`) and stores them in the `labels` list.

---

## Usage

```python
from LoadData import loadData

ld = loadData()
print(ld.data)    # List of face encodings
print(ld.labels)  # List of (name, id) tuples
