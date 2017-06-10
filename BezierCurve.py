import numpy as np


class BezierCurve(object):
    def __init__(self, points, copy=True):
        self.points = np.array(points) if copy else points

    def __call__(self, ts):
        ts = np.array(ts)
        ts.shape = (-1, 1, 1)

        if ts.shape[0] == 0:
            return (np.zeros((self.points.shape[0], 0)), np.zeros((self.points.shape[0], 0)))

        else:
            ps = np.array([self.points])
            pds = np.array([self.points[:, 1:] - self.points[:, :-1]])
            n = ps.shape[2]

            for i in xrange(n - 2):
                ps = deCastelajuStep(ps, ts)
                pds = deCastelajuStep(pds, ts)

            ps = deCastelajuStep(ps, ts)
            pds *= n

            return (ps.T.reshape((-1, ts.shape[0])), pds.T.reshape((-1, ts.shape[0])))


def deCastelajuStep(pts, ts):
    return ts * (pts[:, :, 1:] - pts[:, :, :-1]) + pts[:, :, :-1]
