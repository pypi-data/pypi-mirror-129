# BookListen 🎧

AudioBooker is a command-line tool to convert text files to mp3 files. The mp3 files are stored in `~/booklisten`.

## Installation
Install with pip: `pip install booklisten`

Install from source:
* Clone from github: `git clone https://github.com/mordy-python/booklisten`
* Install dependencies: `pip install -r requirements.txt`
* Install with `setup.py`: `python setup.py install`

## Usage

```
Usage: booklisten [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  convert      Convert FILENAME to .mp3
  convert-dir  Convert all files in DIRECTORY to .mp3
```