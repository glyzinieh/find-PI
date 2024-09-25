import time


class FindPIFunc:
    def __init__(self, find_pi_func, judge_func):
        self.find_pi_func = find_pi_func
        self.judge_func = judge_func

        self.running_time_list = list()
        self.n = None
        self.values = None

    def evaluate_once(self):
        start_time = time.perf_counter()
        n, value = self.find_pi_func(self.judge_func)
        running_time = time.perf_counter() - start_time

        if (self.n is None) or (self.values is None):
            self.n = n
            self.value = value
        self.running_time_list.append(running_time)

    def evaluate(self, evaluate_times):
        for _ in range(evaluate_times):
            self.evaluate_once()

        self.running_time = sum(self.running_time_list) / len(self.running_time_list)
