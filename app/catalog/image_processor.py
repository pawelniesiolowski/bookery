import os
from werkzeug.utils import secure_filename
from PIL import Image
import time


class ImageProcessor:

    def __init__(self, static_dir, logger):
        self.static_dir = static_dir
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
        return self._do_create_path(self.static_dir, image_name)

    def create_relative_path(self, image_name):
        return self._do_create_path('/static', image_name)

    def _do_create_path(self, static_dir, image_name):
        if not image_name:
            return ''
        return os.path.join(static_dir, 'book_img', image_name)
