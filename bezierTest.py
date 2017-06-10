import numpy as np
import BezierCurve as bezcur

points = np.array([[1,2,3,1],[5,1,0,5]])
ts = 0.01 * np.array(range(101))

bc = bezcur.BezierCurve(points)

if __name__ == '__main__':
    import timeit
    print timeit.timeit('bc(ts)', setup='from __main__ import *', number=100000)