import numpy as np
from CubicBezierCurve import  CubicBezierCurve


class Cubic1DBezierCurve(CubicBezierCurve):
    def __init__(self, controlPoints, closed=False):
        super(Cubic1DBezierCurve, self).__init__(controlPoints, lambda v: v, closed)