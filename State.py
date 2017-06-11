import numpy as np
import CubicBezierCurve as cbc
import Cubic2DBezierCurve as c2bc

class SimulationSpace(object):
    def __init__(self, vMax, aMax, alphaMax, discretization):
        self.vMax = vMax
        self.aMax = aMax
        self.alphaMax = alphaMax
        self.discretization = discretization

        self.sVect = discretizeInterval(-1.0, 1.0, self.discretization[0])
        self.vVect = discretizeInterval(0.0, self.vMax, self.discretization[1])
        self.gammaVect = discretizeInterval(-np.pi / 2.0, np.pi / 2.0, self.discretization[2])
        self.aVect = discretizeInterval(0.0, self.aMax, self.discretization[3])
        self.alphaVect = discretizeInterval(-self.alphaMax, self.alphaMax, self.discretization[4])


class State(object):
    def __init__(self, track, tau, trackWidth, simulationSpace):
        self.track = track
        self.tau = tau
        self.trackWidth = trackWidth
        self.simulationSpace = simulationSpace

        self.trackNormal = cbc.normalizeVectors(c2bc.orthogonal2DVector(self.track(self.tau)[1]))

        self.s1Arr = np.zeros(self.simulationSpace.discretization, dtype=np.uint8)
        self.v1Arr = np.zeros(self.simulationSpace.discretization, dtype=np.uint8)
        self.gamma1Arr = np.zeros(self.simulationSpace.discretization, dtype=np.uint8)
        self.tArr = np.zeros(self.simulationSpace.discretization, dtype=np.float32)


def discretizeInterval(minVal, maxVal, levels, dtype=np.float_):
    result = np.array(xrange(levels), dtype)
    result *= (maxVal - minVal) / (levels - 1.0)
    result += minVal

    return result