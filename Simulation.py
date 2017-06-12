import math
import numpy as np
import CubicBezierCurve as cbc
import Cubic2DBezierCurve as c2bc
import State as s

class Simulation(object):
    def __init__(self, b, dt, eps, maxT):
        self.b2 = b / 2.0
        self.dt = dt
        self.eps = eps
        self.maxT = maxT

    def simulate(self, nextState, tau):
        state = s.State(nextState.simulationSpace, tau)



        return state

    def simulationStep(self, state, nextState, sInd, vInd, gammaInd, aInd, alphaInd):
        simSpace = state.simulationSpace
        s = simSpace.sVect[sInd]
        vNorm = simSpace.vVect[vInd]
        gamma = simSpace.gammaVect[gammaInd]

        u = simSpace.aVect[aInd] * getRotationMatrix(simSpace.alphaVect[alphaInd])
        r = s * state.trackTangent + state.trackPoint
        n = np.dot(getRotationMatrix(gamma), state.trackTangent)

        result = self.eulerSimulation(state, r, n, vNorm, u, nextState.tau)

        state.tArr[sInd, vInd, gammaInd, aInd, alphaInd] = result[0] + nextState.tArr[sInd, vInd, gammaInd, aInd, alphaInd]

        if result[0] != np.inf:
            r1 = result[1]
            n1 = result[2]
            vNorm1 = result[3]

            s1 = np.dot(nextState.trackNormal.T, r1 - nextState.trackPoint)[0, 0]
            gamma1 = cmp(s1, 0) * math.acos(np.dot(nextState.trackTangent.T, n1))

            print (s1, vNorm1, gamma1) # REMOVE
        else: # REMOVE
            print "INF" # REMOVE


    def eulerSimulation(self, state, r0, n0, vNorm0, u0, tau1):
        r = np.array(r0)
        n = np.array(n0)
        vNorm = vNorm0
        v = n0 * vNorm
        t = 0.0
        tau = state.tau
        wFun = state.simulationSpace.trackWidthFun

        topBound = min(2.0 * tau1 - state.tau, 1.0)
        track = state.simulationSpace.track

        while tau < tau1:
            r += v * self.dt

            (tau, point, tangent) = track.getNearest(state.tau, topBound, r, self.eps)
            normal = cbc.normalizeVectors(c2bc.orthogonal2DVector(tangent))

            t += self.dt

            if abs(np.dot(normal.T, r - point)[0, 0]) > wFun(tau) or t >= self.maxT:
                return (np.inf, )

            v += (np.dot(u0, n) - self.b2 * vNorm * v) * self.dt
            vNorm = np.linalg.norm(v, axis=0)[0]
            n = n if vNorm == 0 else v / vNorm

        return (t, r, n, vNorm)


def getRotationMatrix(alpha):
    sina = math.sin(alpha)
    cosa = math.cos(alpha)

    return np.array([[cosa, -sina], [sina, cosa]], dtype=np.float32)