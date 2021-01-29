#!/usr/bin/env python3
"""Create manifests.

The photos are handed off to citizen science projects (expeditions) in
Zooniverse, Notes from Nature, for gathering information about what's on the
museum label or the condition of the sample itself. This script creates
zip files of the photos and manifests of what's in them for these projects.

These expeditions tend to be ad hoc.
"""

import csv
import os
from shutil import copy

from PIL import Image
from tqdm import tqdm

from src.pylib.const import DATA_DIR, TEMP_DIR


def zip_images(image_dir, out_dir, threshold=700_000, factor=0.75):
    """Shrink and rotate images and then put them into a zip file."""
    os.makedirs(out_dir, exist_ok=True)
    manifest = out_dir / (out_dir.name + '_manifest.csv')

    with open(manifest, 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(['name'])
        for src in tqdm(image_dir.iterdir()):
            writer.writerow([src.name])
            dst = out_dir / src.name
            copy(src, dst)

            # There has to be a better way
            while dst.stat().st_size > threshold:
                image = Image.open(dst)
                image = image.resize((
                    int(image.size[0] * factor),
                    int(image.size[1] * factor)))
                image.save(dst)


if __name__ == '__main__':
    zip_images(DATA_DIR / 'images', TEMP_DIR / 'label_finder')
