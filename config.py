
from collections import namedtuple
import os

class Paths:
    @property
    def datasets(self):
        return os.environ.get('MD_DATASETS')

paths = Paths()
