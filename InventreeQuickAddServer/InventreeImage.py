#!/usr/bin/env python3
import tempfile
from urllib.parse import urlsplit
import os.path
import inventree
import requests

def set_inventree_image(company: inventree.base.ImageMixin, image_url: str):
    if not image_url:
        return
    # Get extension from image_url
    path = urlsplit(image_url).path
    extension = os.path.splitext(path)[-1] # e.g. ".jpg"
    # Create named temporary file
    with tempfile.NamedTemporaryFile(suffix=extension) as image_file:
        # Download image to temporary file
        image_file.write(requests.get(image_url).content)
        # Upload image to InvenTree
        company.uploadImage(image_file.name)
        # Delete temporary file
        image_file.close()
