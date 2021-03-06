import os
from werkzeug.utils import secure_filename
from PIL import Image
import time


class ImageProcessor:

    def __init__(self, images_dir, logger):
        self.images_dir = images_dir
        self.logger = logger

    def process(self, image):
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

    def remove(self, image_name):
        try:
            os.remove(self.create_path(image_name))
        except OSError as e:
            self.logger.error(e)

    def create_path(self, image_name):
        if not image_name:
            return ''
        return os.path.join(self.images_dir, image_name)
