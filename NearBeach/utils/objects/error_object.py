class ErrorObject(object):
    """A simple class for holding error data"""
    errors: str = ""

    def __init__(self, errors: str):
        """Initialize the class"""
        self.errors = errors
