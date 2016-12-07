import math
import random


ld_1 = {
    (1, 0, 0): 1,
    (1, 0, 1): 0,
    (1, 1, 0): 1,
    (1, 1, 1): 0,
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
        # if idx == 0:
        #     w_sum -= weights[idx] * states[idx]
        # else:
        #     w_sum += weights[idx] * states[idx]
        w_sum += weights[idx] * states[idx]

    return w_sum


def update_parameters(para_seq, learning_dataset):
    learning_rate = 1.0
    gain = 1.0

    def delta_calculation(dataset):
        delta = 0.0

        for data in dataset.iteritems():
            y = sigmoid(data[0], para_seq, gain)
            delta += (y - data[1]) * gain * y * (1.0 - y)
        # for state_1 in (0, 1):
        #     for state_2 in (0, 1):
        #         y = sigmoid((1, state_1, state_2), para_seq)
        #         delta += (y - dataset[(1, state_1, state_2)]) * gain * y * (1.0 - y)

        return delta

    def delta_calculation_modified(data):
        y = sigmoid(data[0], para_seq, gain)
        delta = (y - data[1]) * gain * y * (1.0 - y)
        # for state_1 in (0, 1):
        #     for state_2 in (0, 1):
        #         y = sigmoid((1, state_1, state_2), para_seq)
        #         delta += (y - dataset[(1, state_1, state_2)]) * gain * y * (1.0 - y)

        return delta

    for learning_data in learning_dataset.iteritems():
        next_para_seq = []
        # learning_data = ((1, 0, 0), 1)
        for idx in range(len(para_seq)):
            next_para_seq.append(
                # para_seq[idx] - learning_rate * delta_calculation(learning_dataset) * learning_data[0][idx] * 2.0
                # para_seq[idx] - learning_rate * delta_calculation_modified(learning_data) * learning_data[0][idx] * 2.0
                para_seq[idx] - learning_rate * evaluation_dfunction(para_seq, learning_dataset) * learning_data[0][idx] * 2.0
            )

        para_seq = next_para_seq

    return para_seq


def evaluation_function(para_seq, dataset):
    error = 0.0
    # for state_1 in (0, 1):
    #     for state_2 in (0, 1):
    #         error += (sigmoid((1, state_1, state_2), para_seq) - dataset[(1, state_1, state_2)]) ** 2

    for data in dataset.iteritems():
        error += (sigmoid(data[0], para_seq, 1.0) - data[1]) ** 2

    return error / 2.0


def evaluation_dfunction(para_seq, dataset):
    error = 0.0
    # for state_1 in (0, 1):
    #     for state_2 in (0, 1):
    #         error += (sigmoid((1, state_1, state_2), para_seq) - dataset[(1, state_1, state_2)]) ** 2

    for data in dataset.iteritems():
        output = sigmoid(data[0], para_seq, 1.0)
        # (y - data[1]) * gain * y * (1.0 - y)
        error += ((output - data[1]) * output * (1.0 - output))

    return error


def main_process():
    # paras = [random.randrange(0, 2) for idx in range(3)]
    paras = [-1.0, 2.0, 3.0]
    print paras
    test_times = 10
    # prev_error = evaluation_function(paras, ld_1)
    # print prev_error
    for idx in range(test_times):
        paras = update_parameters(paras, ld_1)
        curr_error = evaluation_function(paras, ld_1)

        print curr_error

        for key, value in ld_1.iteritems():
            print u"Target Value: " + str(value)
            print u"Output Value: " + str(sigmoid(key, paras, 1.0))
            print u""
        # if curr_error >= prev_error:
        #     print curr_error
        #     print idx
        #     break
        # else:
        #     prev_error = curr_error

    print paras

    print evaluation_function(paras, ld_1)

if __name__ == '__main__':
    # a = {(1, 0, 1): 1}
    # for item in a.iteritems():
    #     print item
    main_process()
    pass
