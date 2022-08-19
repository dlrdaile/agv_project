"""
author:dlr123
date:2022年06月13日
"""
import random

import numpy as np


def choose_process(min_num, max_num, process_num):
    process_array = np.arange(process_num) + 1
    choose_list = np.random.choice(process_array, random.randint(min_num, max_num),
                                   replace=True)
    temp = choose_list[:-1] - choose_list[1:]
    temp = choose_list[np.argwhere(temp != 0).flatten()].tolist()
    temp.append(choose_list[-1])
    if len(temp) < min_num:
        temp = choose_process(min_num, max_num, process_num)
    return temp

if __name__ == "__main__":
    print(choose_process(2,4,5))
