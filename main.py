import numpy as np
import BezierCurve as bezcur
import Cubic2DBezierCurve as c2bc
import Cubic1DBezierCurve as c1bc


controlPoints = np.array([[1,2,0.5], [1,0,0.5]], dtype=np.float_)
ts = 0.01 * np.array(range(101))

bc = c2bc.Cubic2DBezierCurve(controlPoints, True)#bezcur.BezierCurve(points) #c1bc.Cubic1DBezierCurve(points, True)

(P, DP) = bc(ts)

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