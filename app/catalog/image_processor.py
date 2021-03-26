"""Service for processing uploaded images data"""


import os
import time
from typing import Optional
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from PIL import Image


class ImageProcessor:
    def __init__(self, images_dir: str) -> None:
        self.images_dir = images_dir

    def process(self, image: FileStorage) -> str:
        assert image.filename, 'Image filename is required'

        filename = '{time}_{name}'.format(
            time=str(int(time.time())),
            name=secure_filename(image.filename)
            )
        path = self.create_path(filename)
        image.save(path)

        image = Image.open(path)
        image.thumbnail((360, 360))
        image.save(path)
        return filename

    def remove(self, image_name: str) -> None:
        os.remove(self.create_path(image_name))

    def create_path(self, image_name: Optional[str]) -> str:
        if not image_name:
            return ''
        return os.path.join(self.images_dir, image_name)
