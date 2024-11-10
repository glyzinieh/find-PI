class Condition:
    def __init__(self, **settings):
        self.settings = settings

    def __call__(self, index: list[int], value: list[float]) -> bool:
        raise NotImplementedError
