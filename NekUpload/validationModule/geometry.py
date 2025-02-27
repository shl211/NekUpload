import os
from  .hdf5validator import *
from typing import Tuple

class ValidateGeometry:
    
    def __init__(self, file_path: str):
        self.file = file_path
        self.file_name = os.path.basename(self.file)


