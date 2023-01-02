import numpy as np


def moving_average(arr, window):
    ret = np.cumsum(arr, dtype=float)
    ret[window:] = ret[window:] - ret[:-window]
    return ret[window - 1:] / window
