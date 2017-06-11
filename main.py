import numpy as np
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

simulationSpace = s.SimulationSpace(track, lambda tau: 0.1, 1.0, 1.0, np.pi / 4.0, (10,10,10,10,10))

tau0 = 0.0
tau1 = 0.01

state = s.State(simulationSpace, tau0)

(r0, n0) = track(tau0)
n0 = cbc.normalizeVectors(n0)
vNorm0 = 0.3
a0 = 0.1
b = 2.0

print sim.eulerSimulation(state, r0, n0, vNorm0, tau1, a0 * sim.getRotationMatrix(0.3), b/2.0, 0.001, 0.001, 100.0)