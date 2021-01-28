#!/usr/bin/env python3
"""Given a CSV file of iDigBio records download the images."""

from os.path import splitext
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import urlretrieve

import pandas as pd
from tqdm import tqdm

from src.pylib.util import DATA_DIR


def download_idigbio(csv_path):
    """Download iDigBio images out of a CSV file."""
    target = 'dwc:associatedMedia'
    df = pd.read_csv(csv_path, dtype=str)

    images = df.loc[df[target].str.contains('http:')][target]

    for url in tqdm(images):
        fields = urlparse(url)
        name = f'{fields.netloc}_{fields.path}'.replace('/', '_')
        name += '.jpg' if not splitext(name)[1] else ''
        path = DATA_DIR / 'images' / name
        if path.exists():
            continue
        try:
            urlretrieve(url, path)
        except HTTPError:
            continue


if __name__ == '__main__':
    download_idigbio(DATA_DIR / 'idb_image_url.csv')
