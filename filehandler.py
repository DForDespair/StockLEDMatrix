from abc import ABC, abstractmethod
from PIL import Image
from io import BytesIO
import os


class FileHandler(ABC):

    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def get(self):
        pass


class LogoHandler(FileHandler):

    def __init__(self, filePath):
        self.filepath = filePath

    def add(self, image: BytesIO, fileName) -> None:
        image = Image.open(image)
        image.save(self.filepath + '/' + fileName)

    def get(self, fileName, directory):
        return Image.open(f"{directory}/{fileName}")

    def getExistingLogos(self, directory):
        pass