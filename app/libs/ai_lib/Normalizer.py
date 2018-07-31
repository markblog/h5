import numpy as np

class Normalizer:

    def difdivstd(self,array):
        mean = np.mean(array)
        std = np.std(array) + 1e-10
        dev = (np.array(array) - mean) / std
        return dev

    def maxmin(self,array):
        min = np.min(array)
        diff = np.max(array) - min
        return (array - min)/diff
