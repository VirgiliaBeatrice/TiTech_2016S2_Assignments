import math
import random


ld_1 = {
    (1, 0, 0): 0,
    (1, 0, 1): 1,
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
        w_sum += weights[idx] * states[idx]

    return w_sum


def update_parameters(layer1_seq, layer2_seq, learning_dataset):
    learning_rate = 0.5
    gain = 1.0
    outputs = {}

    for learning_data in learning_dataset.iteritems():
        # learning_data = ((1, 0, 0), 1)

        def output_calculation(data, seq1, seq2):
            layer1 = [1.0]
            for idx in range(3):
                layer1.append(
                    sigmoid(data[0], [seq1[idx % 3],
                                      seq1[(idx % 3) + 3],
                                      seq1[(idx % 3) + 6]])
                )
            layer2 = sigmoid(layer1, seq2)
            return layer1, layer2

        layer1_output, layer2_output = output_calculation(
            learning_data, layer1_seq, layer2_seq
        )

        layer2_seq_new = []
        for idx_j in range(len(layer2_seq)):
            error = ((layer2_output - learning_data[1]) * layer2_output *
                     (1.0 - layer2_output))
            layer2_seq_new.append(
                layer2_seq[idx_j] - learning_rate * error * layer1_output[
                    idx_j] * 2.0 * gain)
        layer2_seq = layer2_seq_new

        layer1_seq_new = []
        for idx_i in range(3):
            for idx_j in range(1, 4):
                z = layer1_output[idx_j]
                error = (z * (1.0 - z) * layer2_output *
                         (1.0 - layer2_output) *
                         (layer2_output - learning_data[1]))
                layer1_seq_new.append(
                    layer1_seq[(idx_i * 3) + (idx_j - 1)] -
                    learning_rate * error *
                    learning_data[0][idx_i] *
                    layer2_seq[idx_j] * 2.0 * (gain ** 2)
                )
        layer1_seq = layer1_seq_new

        layer1_output, layer2_output = output_calculation(
            learning_data, layer1_seq, layer2_seq
        )

        outputs[learning_data[0]] = (learning_data[1], layer2_output)

    return layer1_seq, layer2_seq, outputs


def evaluation_function(para_seq, dataset):
    error = 0.0

    for data in dataset.iteritems():
        error += (sigmoid(data[0], para_seq, 1.0) - data[1]) ** 2

    return error / 2.0


def main_process():
    para_layer1 = [random.randrange(0, 2) for idx in range(9)]
    # para_layer1 = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    para_layer2 = [random.randrange(0, 2) for idx in range(4)]
    print para_layer1
    print para_layer2
    test_times = 1000
    for idx in range(test_times):
        result = update_parameters(para_layer1, para_layer2, ld_1)
        para_layer1 = result[0]
        para_layer2 = result[1]
        output = result[2]

        print u"------------------------"
        for key, value in output.iteritems():
            print key
            print u"Target Value: " + str(value[0])
            print u"Output Value: " + str(value[1])
            print u""


if __name__ == '__main__':
    # a = {(1, 0, 1): 1}
    # for item in a.iteritems():
    #     print item
    main_process()
    pass
