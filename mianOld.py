import numpy as np
import timeit
import CubicBezierCurve as cbc
import Cubic2DBezierCurve as c2bc
import Simulation as sim
import State as s

controlPoints = np.array([[1,2,0.5], [1,0,0.5]], dtype=np.float_)
ts = 0.01 * np.array(xrange(101))

track = c2bc.Cubic2DBezierCurve(controlPoints, True)

(P, DP) = track(ts)

pxStr = 'Px = ['
pyStr = 'Py = ['

if P.shape != (0, ):
    for i in xrange(P.shape[1] - 1):
        pxStr += ('%f, ' % (P[0, i],))
        pyStr += ('%f, ' % (P[1, i],))

    if P.shape[1] > 0:
        pxStr += ('%f' % (P[0, -1],))
        pyStr += ('%f' % (P[1, -1],))

pxStr += '];'
pyStr += '];'

print pxStr
print pyStr


tau0 = 0.0
tau1 = 0.04

#(r0, n0) = track(tau0)
#n0 = cbc.normalizeVectors(n0)
#vNorm0 = 3.0
#a0 = 8.
b = 2.0
vMax = 5.0
aMax = b/2.0 * vMax ** 2

dt = 0.05
eps = 0.01
maxT = 10.0

print aMax

simulationSpace = s.SimulationSpace(track, lambda tau: 0.1, vMax, aMax, np.pi / 4.0, (5, 5, 5, 5, 5))
state = s.State(simulationSpace, tau0)
nextState = s.State(simulationSpace, tau1)

def simulation():
    sim.Simulation(b, dt, eps, maxT).simulate(nextState, tau0)

#print sim.Simulation(b, dt, eps, maxT).eulerSimulation(state, r0, n0, vNorm0, a0 * sim.getRotationMatrix(0.3), tau1)

# sInd = 10
# vInd = 10
# gammaInd = 10
# aInd = 19
# alphaInd = 10

# def simulation():
#     sim.Simulation(b, dt, eps, maxT).simulationStep(state, nextState, sInd, vInd, gammaInd, aInd, alphaInd)#.eulerSimulation(state, r0, n0, vNorm0, a0 * sim.getRotationMatrix(0.3), tau1)

print "Simulation time: ", timeit.timeit(simulation, number=1)

# print state.tArr[sInd, vInd, gammaInd, aInd, alphaInd], state.s1Arr[sInd, vInd, gammaInd, aInd, alphaInd], \
#     state.v1Arr[sInd, vInd, gammaInd, aInd, alphaInd], state.gamma1Arr[sInd, vInd, gammaInd, aInd, alphaInd], \
#     state.a1Arr[sInd, vInd, gammaInd, aInd, alphaInd], state.alpha1Arr[sInd, vInd, gammaInd, aInd, alphaInd]