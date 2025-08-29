# Building the Documentation

This directory contains the Sphinx project for the TurboGears website.

## Prerequisites
- Python 3.8+ recommended
- Make (for running `make html`)

## Quick Start

1. Create and activate a virtual environment (recommended):
   
   ```bash
   cd src
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -U pip
   ```

2. Install build dependencies:
   
   ```bash
   pip install -r requirements.txt
   ```

3. Build the HTML site:
   
   ```bash
   make html
   ```

4. Open the result:
   
   - `_build/html/index.html`

## Useful Commands
- Clean build artifacts: `make clean`
- Rebuild after changes: `make html`

## Notes
- The build uses local extensions in `youtube.py` and `cogbin.py`.
- If your environment has restricted network access, the CogBin page will skip fetching live data from PyPI but the build will still complete.
