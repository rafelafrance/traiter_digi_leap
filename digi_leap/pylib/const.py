"""Define literals used in the system."""

from pathlib import Path

__VERSION__ = '0.5.0'

BATCH_SIZE = 1_000_000  # How many records to work with at a time

DATA_DIR = Path('.') / 'data'
if not DATA_DIR.exists():
    DATA_DIR = Path('..') / 'data'

TEMP_DIR = DATA_DIR / 'temp'
