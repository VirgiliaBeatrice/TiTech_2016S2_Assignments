import math
import random

rand_seq = [random.randint(0, 1) for dummy_idx in range(16)]


class HopfieldNeuronNetwork:

    def __init__(self, states, weights, thresholds, gain=1.0, debug=False):
        self.debug_flag = debug
        self.states = states
        self.weights = weights
        self.thresholds = thresholds
        self.latest_energy = calculate_energy(self.states)
        self.gain = gain
        print u"Initial states: "
        print self.states
        print u"Current energy: "
        print self.latest_energy

    def _weighted_sum_(self, main_idx):
        w_sum = 0
        # weights = {}
        for weight_idx, weight_val in self.weights.iteritems():
            if main_idx in weight_idx:
                temp = list(weight_idx)
                temp.remove(main_idx)
                w_sum += weight_val * self.states[temp[0]]
        return w_sum

    def _sigmoid_(self, update_idx):
        return (1.0 / (1.0 + math.exp(float(-self.gain) *
                                      float(self._weighted_sum_(update_idx) -
                                            self.thresholds[update_idx])))
                )

    def update_state(self, update_idx):
        bias = 0
        minus = (self._weighted_sum_(update_idx) -
                 self.thresholds[update_idx] + bias)

        if minus < 0:
            self.states[update_idx] = 0
        else:
            self.states[update_idx] = 1

        self.latest_energy = calculate_energy(self.states)

        if self.debug_flag:
            print u"Current states: "
            print self.states
            print u"Energy: " + str(self.latest_energy)

    def update_state_possibility(self, update_idx):
        rand = random.random()
        result = self._sigmoid_(update_idx)
        if rand > result:
            self.states[update_idx - 1] = 0
        else:
            self.states[update_idx - 1] = 1

        self.latest_energy = calculate_energy(self.states)

        if self.debug_flag:
            print u"Current states: "
            print self.states
            print u"Energy: " + str(self.latest_energy)


def calculate_energy(sequence):
    energy_1 = 0
    energy_2 = 0
    array = []

    for idx in range(len(sequence) / 4):
        array.append(sequence[(4 * idx):(4 * (idx + 1))])

    for row_idx in range(len(array)):
        temp_sum = 0
        for col_idx in range(len(array)):
            temp_sum += array[row_idx][col_idx]

        energy_1 += math.pow(temp_sum - 1, 2)

    for col_idx in range(len(array)):
        temp_sum = 0
        for row_idx in range(len(array)):
            temp_sum += array[row_idx][col_idx]

        energy_2 += math.pow(temp_sum - 1, 2)

    return energy_1 + energy_2


def pre_calculation():
    zero_seq = [0 for dummy_idx in range(16)]
    calc_seq = zero_seq[:]

    thresholds = []
    zero_energy = calculate_energy(zero_seq)
    i_energy = []
    ij_energy = {}
    weights = {}

    for idx in range(16):
        calc_seq[idx] = 1
        i_energy.append(calculate_energy(calc_seq))
        thresholds.append(i_energy[idx] - zero_energy)
        calc_seq[idx] = 0

    for idx_i in range(16):
        for idx_j in range(16):
            if idx_i != idx_j:
                calc_seq[idx_i] = 1
                calc_seq[idx_j] = 1
                index = tuple(sorted([idx_i, idx_j]))
                ij_energy[index] = calculate_energy(calc_seq)
                weights[index] = (
                    -ij_energy[index] +
                    i_energy[idx_i] +
                    i_energy[idx_j] +
                    zero_energy
                )
                calc_seq[idx_i] = 0
                calc_seq[idx_j] = 0

    print zero_energy
    print thresholds
    print weights
    return weights, thresholds


def num_mapping():
    DIM = 4
    mapping = {}
    for idx_i in range(DIM):
        for idx_j in range(DIM):
            mapping[(idx_i, idx_j)] = idx_i * DIM + idx_j

    return mapping


def calculate_d(sequence):
    # sequence = []
    temp_set = set(sequence)
    count = {}
    for item in temp_set:
        count[item] = sequence.count(item)

    return count


if __name__ == '__main__':
    mapping = num_mapping()
    print mapping
    inits = pre_calculation()
    result = []
    # print result
    hnn = HopfieldNeuronNetwork(rand_seq,
                                inits[0], inits[1], gain=0.25, debug=True)
    for idx in range(100):
        hnn.update_state(random.randint(0, 15))
        # hnn.update_state_possibility(random.randint(0, 15))
        result.append(hnn.latest_energy)
    print calculate_d(result)
    print set(result)
