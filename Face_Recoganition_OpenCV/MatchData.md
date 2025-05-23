# MatchData.py Documentation

## Overview

The `MatchData.py` module provides functionality to identify a face from a given image by comparing it against a database of known faces. It defines the `matchData` class, which loads known face encodings and attempts to find a match for a new image using the `face_recognition` library.

---

## Class: `matchData`

### Attributes

- `imag` – Path to the input image (JPEG/PNG) to be recognized.
- `load_data` – An instance of `loadData` from `LoadData.py`, which provides access to known face encodings and their labels.
- `result` – A tuple `(name, id)` of the matched individual if a match is found; otherwise, `None`.

---

### Methods

#### `__init__(self, imag)`
- Initializes with the image path.
- Loads known data using `loadData`.
- Calls `self.match()` to find and store the result.

#### `match(self)`
- Loads the image using `face_recognition`.
- Extracts face encodings from the image.
- Compares the encodings against known data using `face_recognition.compare_faces`.
- If a match is found, returns the corresponding `(name, id)` tuple.
- Prints the result and returns `None` if no match is found or if no face is detected.

---

## Usage Example

```python
from MatchData import matchData

matcher = matchData("path/to/image.jpg")
if matcher.result:
    name, id = matcher.result
    print(f"User recognized: {name} (ID: {id})")
else:
    print("No match found.")
