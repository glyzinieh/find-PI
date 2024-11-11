class Condition:
    def __init__(self, **settings):
        self.settings = settings

    def __call__(
        self, index_list: list[int], time_list: list[float], value_list: list[float]
    ) -> bool:
        raise NotImplementedError
