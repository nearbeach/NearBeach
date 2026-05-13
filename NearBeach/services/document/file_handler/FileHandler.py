class FileHandler:
    """Abstraction for file handler classes"""

    @staticmethod
    def upload(_, upload_document, document_results, file):
        return NotImplemented

    @staticmethod
    def fetch(_, document_results):
        return NotImplemented