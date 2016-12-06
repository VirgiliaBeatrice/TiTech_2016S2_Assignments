import math
import random

num_neurons = 25
city_locations = [
    (2, 1), (2, 5), (5, 3), (6, 7), (8, 2)
]
rand_seq = [random.randint(0, 1) for dummy_idx in range(num_neurons)]


class HopfieldNeuronNetwork:

    def __init__(self, states, weights, thresholds, gain=1.0, debug=False):
        self.debug_flag = debug
        self.states = states
        self.weights = weights
        self.thresholds = thresholds
        self.latest_energy = energy_calculation_tlp(self.states)
        self.gain = gain
        print u"Initial states: "
        self.print_current_state()
        # print self.states
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
        try:
            return (1.0 / (1.0 + math.exp(round(float(-self.gain), 2) *
                                          round(float(self._weighted_sum_(update_idx) -
                                                self.thresholds[update_idx]), 2)
                                          )
                           )
                    )
        except OverflowError, e:
            print e
            print round(float(-self.gain), 10)
            print round(float(self._weighted_sum_(update_idx) -
                              self.thresholds[update_idx]), 10)

    def update_state(self, update_idx):
        bias = 0
        minus = (self._weighted_sum_(update_idx) -
                 self.thresholds[update_idx] + bias)

        if minus < 0:
            self.states[update_idx] = 0
        else:
            self.states[update_idx] = 1

        self.latest_energy = energy_calculation_tlp(self.states)

        if self.debug_flag:
            print u"Current states: "
            self.print_current_state()
            # print self.states
            print u"Energy: " + str(self.latest_energy)

    def update_state_possibility(self, update_idx):
        rand = random.random()
        result = self._sigmoid_(update_idx)
        if rand > result:
            self.states[update_idx - 1] = 0
        else:
            self.states[update_idx - 1] = 1

        self.latest_energy = energy_calculation_tlp(self.states)

        if self.debug_flag:
            print u"Current states: "
            self.print_current_state()
            # print self.states
            print u"Energy: " + str(self.latest_energy)

    def print_current_state(self):
        dim = int(math.sqrt(len(self.states)))
        for idx in range(dim):
            print self.states[(idx * dim):((idx + 1) * dim)]


def energy_calculation_tlp(state_seq, bias=10):
    length = 0
    restriction_1 = 0
    restriction_2 = 0
    dim = int(math.sqrt(num_neurons))

    # Reform target matrix
    def seq_to_matrix(sequence):
        target_matrix = []
        for idx in range(len(sequence) / dim):
            target_matrix.append(sequence[(dim * idx):(dim * (idx + 1))])
        return target_matrix

    state_matrix = seq_to_matrix(state_seq)
    dist_matrix = distance_matrix_calculation(city_locations)

    # Calculate length
    for order_idx in range(dim):
        for city1_idx in range(dim):
            for city2_idx in range(dim):
                if order_idx + 1 < dim:
                    length += (
                        state_matrix[order_idx][city1_idx] *
                        state_matrix[order_idx + 1][city2_idx] *
                        dist_matrix[city1_idx][city2_idx]
                    )
                else:
                    length += (
                        state_matrix[order_idx][city1_idx] *
                        state_matrix[1][city2_idx] *
                        dist_matrix[city1_idx][city2_idx]
                    )

    # Calculate first part of restriction
    for order_idx in range(dim):
        temp_sum = 0
        for city_idx in range(dim):
            temp_sum += state_matrix[order_idx][city_idx]
        restriction_1 += (temp_sum - 1) ** 2

    # Calculate second part of restriction
    for city_idx in range(len(state_matrix)):
        temp_sum = 0
        for order_idx in range(len(state_matrix)):
            temp_sum += state_matrix[order_idx][city_idx]
        restriction_2 += (temp_sum - 1) ** 2

    return length + (restriction_1 + restriction_2) * bias


def pre_calculation():
    zero_seq = [0 for dummy_idx in range(num_neurons)]
    calc_seq = zero_seq[:]

    thresholds = []
    weights = {}

    ij_energy = {}

    zero_energy = energy_calculation_tlp(zero_seq)

    i_energy = []
    for idx in range(num_neurons):
        calc_seq[idx] = 1
        i_energy.append(energy_calculation_tlp(calc_seq))
        thresholds.append(i_energy[idx] - zero_energy)
        calc_seq[idx] = 0

    for idx_i in range(num_neurons):
        for idx_j in range(num_neurons):
            if idx_i != idx_j:
                calc_seq[idx_i] = 1
                calc_seq[idx_j] = 1
                index = tuple(sorted([idx_i, idx_j]))
                ij_energy[index] = energy_calculation_tlp(calc_seq)
                weights[index] = (
                    thresholds[idx_i] +
                    thresholds[idx_j] +
                    zero_energy -
                    ij_energy[index]
                )
                calc_seq[idx_i] = 0
                calc_seq[idx_j] = 0

    print zero_energy
    print thresholds
    print weights
    return weights, thresholds


def distance_matrix_calculation(loc):
    dist_matrix = []

    for row_idx in range(len(loc)):
        dist_matrix_row = []
        for col_idx in range(len(loc)):
            dist_matrix_row.append(
                round(
                    math.sqrt(
                        (loc[row_idx][0] - loc[col_idx][0]) ** 2 +
                        (loc[row_idx][1] - loc[col_idx][1]) ** 2
                    ), 2
                )
            )
        dist_matrix.append(dist_matrix_row)

    return dist_matrix


def num_mapping():
    DIM = 5
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


def main_process():
    inits = pre_calculation()
    result = []
    # print result
    hnn = HopfieldNeuronNetwork(rand_seq,
                                inits[0], inits[1], gain=1, debug=False)
    for idx in range(1000):
        hnn.update_state(random.randint(0, 24))
        # hnn.update_state_possibility(random.randint(0, 24))
        result.append(hnn.latest_energy)
    print u"Final states: "
    hnn.print_current_state()
    print calculate_d(result)
    print sorted(list(set(result)))


if __name__ == '__main__':
    main_process()
    # print distance_matrix_calculation(city_locations)
