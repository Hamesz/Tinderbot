class Classifier:

    def __init__(self, *args, **kwargs):
        pass

    def __repr__(self):
        return f"{self.__name__}()"

    def classify(self, *args, **kwargs):
        return self._classify(*args, **kwargs)

    def _classify(self, *args, **kwargs):
        return 1
