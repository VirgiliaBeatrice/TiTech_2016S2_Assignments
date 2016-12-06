import math
import random


def sigmoid(learning_data, weights, gain=1.0):
    return (1.0 / (1.0 +
                   math.exp(-gain *
                            float(weighted_sum(learning_data, weights)))))


learning_dataset = {
    (0, 0): 1,
    (0, 1): 0,
    (1, 0): 1,
    (1, 1): 0,
}


def weighted_sum(learning_data, weights):
    w_sum = 0

    for idx in range(len(weights)):
        w_sum += weights[idx] * learning_data[idx]

    return w_sum


# def output_function(learning_data, weights):
#     rand = random.random()
#     sigmoid_value = sigmoid(learning_data, weights)
#
#     if rand > sigmoid_value:
#         return 0
#     else:
#         return 1

def output_function(learning_data, weights):
    return sigmoid(learning_data, weights)



def update_parameters(para_seq):
    para_seq = [1, 1, 1]
    learning_rate = 1

    delta = 0.0

    for state_1 in (0, 1):
        for state_2 in (0, 1):
            y = sigmoid((state_1, state_2), para_seq[1:])
            delta += (2 *
                      (y -
                       learning_dataset[(state_1, state_2) * gain * y * (1 - y)]))
    for para in para_seq:
        para_new = para - learning_rate *



if __name__ == '__main__':
    pass