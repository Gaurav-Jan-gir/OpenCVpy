# Recover.py Documentation

## Overview

This script attempts to **recover corrupted or unreadable `.npy` files** that may have been affected by:
- Partial writes
- NumPy version incompatibility
- Improper encoding (e.g., saving `None`)
- Changes in data structure or format

It reads files from the `data/` directory and, if valid, saves them into a new directory named `recovered_data/`.

---

## Features

- ✅ Attempts to load each `.npy` file using `allow_pickle=True`
- ✅ Validates that the content is a NumPy array with shape `(128,)` (as expected for face encodings)
- ✅ Copies valid files to a new directory (`recovered_data/`)
- ❌ Skips invalid or unreadable files and logs them

---

## Usage

1. Place this script in the root of your project (where `data/` exists).
2. Run it using Python:

```bash
python RecoverCorruptedNPY.py
