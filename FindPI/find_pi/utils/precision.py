import math

# 桁数を判定
def judge_digits(value_list, digits, threshold=None):
    if len(value_list) >= 1:
        value = value_list[-1]
        return str(value)[:digits+1] == str(math.pi)[:digits+1]
    else:
        return False

# 移動量を判定
def judge_moving_distance(value_list, threshold, digits=None):
    if len(value_list) >= 1:
        value = value_list[-1]
        if len(value_list) >= 2:
            last_value = value_list[-2]
            return abs(value - last_value) <= threshold
        else:
            return False
    else:
        return False

# 桁数と移動量で判定
def judge_digits_and_distance(value_list, digits, threshold):
    return judge_digits(value_list, digits) and judge_moving_distance(value_list, threshold)

class Judge:
    def __init__(self, judge_func, digits, threshold):
        self.judge_func = judge_func
        self.digits = digits
        self.threshold = threshold

    def judge(self, value_list):
        return self.judge_func(value_list, self.digits, self.threshold)
