import numpy as np

def removeCopies(points):
    indexes = []

    for i in xrange(points.shape[1]):
        if np.array_equal(points[:, i], points[:, i - 1]):
            indexes.append(i)

    return points[:, indexes]