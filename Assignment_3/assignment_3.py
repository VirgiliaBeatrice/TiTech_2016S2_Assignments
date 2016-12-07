import math
import random
import numpy as np
import matplotlib.pyplot as plt

# linear_array
ARRAY = [
    ((1, 2, 3, 4, 5), (1, -1, 1, -1, 0)),
    ((1, 2, 3, 4, 5), (2, 1, -2, 1, 1)),
    ((1, 2, 3, 4, 5), (-1, -1, -2, 1, 3)),
    ((1, 2, 3, 4, 5), (1, -2, 1, 1, 1))
]

SIZE = len(ARRAY) + 1
x_array = (1, 1, 1, 1)
font = {
    'fontname': 'Arial',
    # 'fontname': 'Helvetica',
    # 'color':  'darkred',
    'weight': 'normal',
    'size': 20,
}


class HopfieldNeuronNetwork:

    def __init__(self, states, weights, thresholds, others, gain=0.0,
                 debug=False):
        self.debug_flag = debug
        self.states = states
        self.weights = weights
        self.thresholds = thresholds
        self.others = others
        self.latest_energy = 0
        print u"Current states: "
        print self.states
        self.calculate_energy()
        self.gain = gain

    def _weighted_sum_(self, main_idx):
        w_sum = 0
        for weight in self.weights:
            if main_idx in weight[0]:
                temp = list(weight[0])
                temp.remove(main_idx)
                w_sum += weight[1] * self.states[temp[0] - 1]
        return w_sum

    def _sigmoid_(self, main_idx):
        return (1.0 / (1.0 + math.exp(float(-self.gain) *
                                      float(self._weighted_sum_(main_idx) -
                                            self.thresholds[main_idx - 1][1])))
                )

    def update_state_possibility(self, update_idx):
        rand = random.random()
        result = self._sigmoid_(update_idx)
        if rand >= result:
            self.states[update_idx - 1] = 0
        else:
            self.states[update_idx - 1] = 1

        if self.debug_flag:
            print u"Current states: "
            print self.states

    def calculate_energy(self):
        energy_1 = 0
        energy_2 = 0
        energy_3 = 0

        for weight_item in self.weights:
            energy_1 += (self.states[weight_item[0][0] - 1] *
                         self.states[weight_item[0][1] - 1] *
                         weight_item[1]) / (-2)

        for threshold_item in self.thresholds:
            energy_2 += (self.states[threshold_item[0] - 1] *
                         threshold_item[1])

        for other_item in self.others:
            if other_item[0][0] < SIZE:
                energy_3 += (self.states[other_item[0][0] - 1] *
                             self.states[other_item[0][0] - 1] *
                             other_item[1])
            else:
                energy_3 += other_item[1]

        self.latest_energy = energy_1 + energy_2 + energy_3
        if self.debug_flag:
            print u"Energy: " + str(self.latest_energy)


def equation_pow(linear_array, result):
    for idx_x in range(0, SIZE):
        item = linear_array[0][idx_x]
        value = linear_array[1][idx_x]
        for idx_y in range(0, SIZE):
            key = tuple(sorted([item, linear_array[0][idx_y]]))
            if key in result.keys():
                result[key] += value * linear_array[1][idx_y]
            else:
                result[key] = value * linear_array[1][idx_y]

    return result


def standardize_energy(array):
    theta = []
    omega = []
    other = []

    for key, value in array.iteritems():
        if key[1] != key[0]:
            if key[1] is SIZE:
                theta.append((key[0], value))
            else:
                omega.append((key, value * (-2)))
        else:
            other.append((key, value))

    print u"theta is "
    print sorted(theta)
    print u"omega is "
    print sorted(omega)
    print u"other is "
    print sorted(other)

    return sorted(theta), sorted(omega), sorted(other)


def plot(sequence):
    plt.figure(figsize=(10, 10))
    x = np.linspace(0, len(sequence), len(sequence))
    y = sequence

    plt.plot(x, y, label=r"$\frac{1}{1 + e^{-4x}}$", color="green", linewidth=1.5)

    # plt.title(u'Sigmoid Function with Different \u03b1 Value', fontdict=font)
    # plt.xlabel('time (s)', fontdict=font)
    # plt.ylabel('voltage (mV)', fontdict=font)
    # plt.ylim(0, 6)

    # Tweak spacing to prevent clipping of ylabel
    # plt.subplots_adjust(left=0.15)
    plt.legend(loc=4, fontsize=18)
    plt.show()


def calculate_d(sequence):
    # sequence = []
    temp_set = set(sequence)
    count = {}
    for item in temp_set:
        count[item] = sequence.count(item)

    return count


def main_process():
    result = {}
    for item in ARRAY:
        equation_pow(item, result)
    temp = standardize_energy(result)
    hnn = HopfieldNeuronNetwork([random.randint(0, 1) for idx in range(4)],
                                temp[1], temp[0], temp[2], gain=0.5, debug=False)
    input_sequence = []
    for idx in range(1000):
        hnn.update_state_possibility(random.randint(1, len(ARRAY)))
        hnn.calculate_energy()
        input_sequence.append(tuple(hnn.states))
    print calculate_d(input_sequence)
    plot(input_sequence)
    plot(calculate_d(input_sequence).values())
    pass

if __name__ == '__main__':
    main_process()
