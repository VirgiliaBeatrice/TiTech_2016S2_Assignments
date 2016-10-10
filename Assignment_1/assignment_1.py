import math
import random


RAND_MAX = 65535

# input_values = [1.0, 2.0, -3.0]
# weighted_values = [2.2, 1.5, 1.0]
input_values = [-2.4, 1.3, -1.0]
weighted_values = [2.2, 4.0, 1.5]
theta = 1.0
alphas = [4.0, 2.0, 1.0, 0.5, 0.25]
test_times = 10000


def sigmoid(input_alpha, w_sum, threshold):
    return 1.0 / (1.0 + math.exp(float(-input_alpha) * float(w_sum - threshold)))


def weighted_sum(input_vals, weight_vals):
    w_sum = 0
    for idx in range(len(input_vals)):
        w_sum += input_vals[idx] * weight_vals[idx]
    return w_sum


def test(times, sig):
    cnt = 0
    for idx in range(times):
        rand_val = random.randrange(0.0, float(RAND_MAX))
        if rand_val < (sig * float(RAND_MAX)):
            cnt += 1

    return cnt


def calculation():
    w_sum = weighted_sum(input_values, weighted_values)
    print u"Weighted Sum is " + str(w_sum) + u"."

    for alpha in alphas:
        sig_val = sigmoid(alpha, w_sum, theta)
        result = test(test_times, sig_val)
        print u"For alpha equals " + str(alpha)
        print u"Theoretical Value: " + str(sig_val)
        print u"Actual Value: " + str(float(result) / test_times)
        print u"Actual Counts: " + str(result) + u" / " + str(test_times)


if __name__ == '__main__':
    calculation()
    pass
