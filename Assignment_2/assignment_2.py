import math
import random

# linear_array
ARRAY = [
    ((1, 2, 3, 4, 5), (1, -1, 1, -1, 0)),
    ((1, 2, 3, 4, 5), (2, 1, -2, 1, -1)),
    ((1, 2, 3, 4, 5), (-1, -1, -2, 1, -3)),
    ((1, 2, 3, 4, 5), (1, -2, 1, 1, -1))
]
x_array = (1, 1, 1, 1)

def equation_sqrt(linear_array, result):
    for idx_x in range(0, 5):
        item = linear_array[0][idx_x]
        value = linear_array[1][idx_x]
        for idx_y in range(0, 5):
            key = tuple(sorted([item, linear_array[0][idx_y]]))
            if key in result.keys():
                result[key] += value * linear_array[1][idx_y]
            else:
                result[key] = value * linear_array[1][idx_y]

    return result


if __name__ == '__main__':
    result = {}
    for item in ARRAY:
        equation_sqrt(item, result)
    print result
    pass
