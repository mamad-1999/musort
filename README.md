<h4 align="center">Musort & Muedit Music Metadata Toolkit.</h4>
<p align="center">
  <a href="#installation"><img src="https://img.shields.io/badge/Install-blue?style=for-the-badge" alt="Install"></a>
  <a href="#usage"><img src="https://img.shields.io/badge/Usage-green?style=for-the-badge" alt="Usage"></a>
  <a href="#contributing"><img src="https://img.shields.io/badge/Contributing-yellow?style=for-the-badge" alt="Contributing"></a>
</p> 

## Overview

**Musort** and **Muedit** are Python-based scripts designed to streamline music file organization and metadata management. `muedit.py` enables interactive editing of music file metadata, while `musort.py` renames files based on metadata fields, helping to keep your music library organized.

---

## Installation

Ensure Python 3 is installed, then install the required packages:

```bash
pip install mutagen colorama
```

For metadata editing, make sure **ffmpeg** is installed:
```bash
# Install ffmpeg on Ubuntu
sudo apt install ffmpeg
# Install ffmpeg on MacOS
brew install ffmpeg
```

---

## Usage

### Muedit.py
Use `muedit.py` to view and edit metadata for a single music file or an entire folder interactively.

#### Command
```bash
python muedit.py /path/to/music_or_folder --sort
```

#### Example
```bash
python muedit.py /music/collection --sort
```

#### Explanation
- **`--sort`**: After editing metadata, this option triggers `musort.py` to rename the files based on chosen metadata fields.

> **Note:** `--sort` assumes that `musort.py` is in the same directory as `muedit.py`.

---

### Musort.py
Use `musort.py` to rename music files based on specific metadata fields.

#### Command
```bash
python musort.py /path/to/music_or_folder -f artist.title -s "-"
```

#### Example
```bash
python musort.py /music/collection -f album.artist -s "_"
```

#### Explanation
- **`-f`**: Sets the renaming format, e.g., `artist.title`.
- **`-s`**: Defines a separator between fields (default: "-").

---

## Contributing

Contributions to `musort` and `muedit` are welcome! Please fork the repository and submit a pull request. Make sure to follow standard code formatting and add appropriate comments to new functionality.
