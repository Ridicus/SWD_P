import math
import numpy as np
import CubicBezierCurve as cbc
import Cubic2DBezierCurve as c2bc
import State as s


def simulate(nextState, tau):
    state = s.State(nextState.simulationSpace, tau)



    return state

def eulerSimulation(state, r0, n0, vNorm0, tau1, u0, b2, dt, eps, maxT):
    r = np.array(r0)
    n = np.array(n0)
    vNorm = vNorm0
    v = n0 * vNorm
    t = 0.0
    tau = state.tau
    wFun = state.simulationSpace.trackWidthFun

    track = state.simulationSpace.track

    while tau < tau1:
        r += v * dt

        (tau, point, tangent) = track.getNearest(state.tau, 2.0 * tau1 - state.tau, r, eps)
        normal = cbc.normalizeVectors(c2bc.orthogonal2DVector(tangent))

        t += dt

        if abs(np.dot(normal.T, r - point)[0, 0]) > wFun(tau) or t >= maxT:
            return (np.inf, )

        v += (np.dot(u0, n) - b2 * vNorm * v) * dt
        vNorm = np.linalg.norm(v, axis=0)[0]
        n = n if vNorm == 0 else v / vNorm

    return (t, r, n, vNorm)


def getRotationMatrix(alpha):
    sina = math.sin(alpha)
    cosa = math.cos(alpha)

    return np.array([[cosa, -sina], [sina, cosa]], dtype=np.float32)

def eulerStep(f, x0, t0, dt):
    return (x0 + f(x0, t0) * dt, t0 + dt)