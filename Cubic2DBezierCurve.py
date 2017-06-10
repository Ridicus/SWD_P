import numpy as np
from CubicBezierCurve import  CubicBezierCurve


class Cubic2DBezierCurve(CubicBezierCurve):
    def __init__(self, controlPoints, closed=False):
        super(Cubic2DBezierCurve, self).__init__(controlPoints, orthogonal2DVector, closed)


def orthogonal2DVector(v):
    result = np.array(v[(1, 0), :])
    result[1, :] *= -1

    return result