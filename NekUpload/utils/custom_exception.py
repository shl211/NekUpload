class HDF5ReaderException(Exception):
    def __init__(self, message):
        super().__init__(message)

class XMLReaderException(Exception):
    def __init__(self, message):
        super().__init__(message)