class UrbanException(Exception):
    pass

class TokenInvalid(UrbanException):
    def __init__(self, message):
        self.message = message
        super().__init__(message)