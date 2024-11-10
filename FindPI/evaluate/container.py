class ResultContainer:
    def __init__(
        self,
        index_list: list[int],
        value_list: list[float],
        time_list: list[float],
        diff_list: list[float],
    ):
        self.index_list = index_list
        self.value_list = value_list
        self.time_list = time_list
        self.diff_list = diff_list
