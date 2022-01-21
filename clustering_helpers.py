from math import dist
import numpy
import statistics


def get_all_feature_pairs():
    all_pairs = []

    for i in range(3, 11):
        for j in range(i + 1, 11):
            cur_pair = [i, j]
            all_pairs.append(cur_pair)

    return all_pairs


def compute_error(X, centers, labels):
    dist_sum = 0

    for i in range(len(X)):
        dist_sum += dist(X[i], centers[labels[i]])

    return dist_sum


def normalize_feature_statistics(feature):
    min_element = min(feature)
    max_element = max(feature)

    for i in range(len(feature)):
        if feature[i] < 0:
            feature[i] /= min_element
        elif feature[i] > 0:
            feature[i] /= max_element

