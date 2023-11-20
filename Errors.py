class Stalemate(BaseException):
    ...


class IncorrectCoordinates(KeyError):
    def __init__(self, *args):
        self.msg = args[0] if args else None
