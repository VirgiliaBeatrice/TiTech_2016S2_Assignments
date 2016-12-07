import math
import random


ld_1 = {
    (1, 0, 0): 0,
    (1, 0, 1): 1,
    (1, 1, 0): 0,
    (1, 1, 1): 1,
}


def sigmoid(states, weights, gain=1.0):
    # learning_data = (1, 0, 0)
    # try:
        return (1.0 / (1.0 +
                       math.exp(-gain *
                                float(weighted_sum(states, weights)))))
    # except OverflowError:
    #     return 0


def weighted_sum(states, weights):
    w_sum = 0

    for idx in range(len(weights)):
        w_sum += weights[idx] * states[idx]

    return w_sum


def update_parameters(para_seq, learning_dataset):
    learning_rate = 0.5
    gain = 1.0

    for learning_data in learning_dataset.iteritems():
        next_para_seq = []
        # learning_data = ((1, 0, 0), 1)
        for idx in range(len(para_seq)):
            next_para_seq.append(
                para_seq[idx] - learning_rate *
                evaluation_dfunction(para_seq, learning_data) *
                learning_data[0][idx] * 2.0 * gain
            )

        para_seq = next_para_seq

    return para_seq


def evaluation_function(para_seq, dataset):
    error = 0.0

    for data in dataset.iteritems():
        error += (sigmoid(data[0], para_seq, 1.0) - data[1]) ** 2

    return error / 2.0


def evaluation_dfunction(para_seq, data):
    # error = 0.0

    # for data in dataset.iteritems():
    output = sigmoid(data[0], para_seq, 1.0)
    error = ((output - data[1]) * output * (1.0 - output))

    return error


def main_process():
    paras = [random.randrange(0, 2) for idx in range(3)]
    # paras = [-1.0, 2.0, 3.0]
    print paras
    test_times = 10000
    # prev_error = evaluation_function(paras, ld_1)
    # print prev_error
    for idx in range(test_times):
        paras = update_parameters(paras, ld_1)
        curr_error = evaluation_function(paras, ld_1)

        print curr_error

        for key, value in ld_1.iteritems():
            print key
            print u"Target Value: " + str(value)
            print u"Output Value: " + str(sigmoid(key, paras, 1.0))
            print u""

    print paras

    print evaluation_function(paras, ld_1)

if __name__ == '__main__':
    main_process()
    pass
