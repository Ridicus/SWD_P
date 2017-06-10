import numpy as np
from BezierCurve import BezierCurve


class CubicBezierCurve(object):
    def __init__(self, controlPoints, orthoFun, closed=False):
        self.orthoFun = orthoFun
        self.closed = closed
        self.controlPointsCount = controlPoints.shape[1]
        self.allPoints = self.addMidpoints(controlPoints)
        self.curves = self.createCurves()

    def __call__(self, ts):
        ts = np.array(ts)
        ts.shape = (-1, )

        if ts.shape[0] == 0 or len(self.curves) == 0:
            return (np.array([]), np.array([]))

        else:
            pts = np.zeros((self.allPoints.shape[0], ts.shape[0]))
            pds = np.zeros((self.allPoints.shape[0], ts.shape[0]))

            ts *= len(self.curves)
            tts = np.trunc(ts)
            tfs = ts - tts

            for i in xrange(len(self.curves)):
                inds = tts == i
                (pts[:, inds], pds[:, inds]) = self.curves[i](tfs[inds])

            inds = ts == len(self.curves)
            (pts[:, inds], pds[:, inds]) = self.curves[-1](tfs[inds] + 1)

            return (pts, pds)

    def addMidpoints(self, points):
        allPoints = np.zeros((points.shape[0], 3 * points.shape[1] - (0 if self.closed or points.shape[1] == 0 else 2)))

        if points.shape[1] > 0:
            if not self.closed and allPoints.shape[1] == 1:
                allPoints[:, 0, np.newaxis] = points

            else:
                if self.closed:
                    indexes = np.array((0, 1, 2))
                    pointRange = xrange(points.shape[1])

                else:
                    allPoints[:, (0, 1)] = calculateMidpoints(points[:, 0, np.newaxis], None, points[:, 1, np.newaxis],
                                                              self.orthoFun)
                    allPoints[:, (-2, -1)] = calculateMidpoints(points[:, -1, np.newaxis], points[:, -2, np.newaxis],
                                                                None, self.orthoFun)
                    indexes = np.array((2, 3, 4))
                    pointRange = xrange(1, points.shape[1] - 1)

                for i in pointRange:
                    allPoints[:, indexes] = calculateMidpoints(points[:, i, np.newaxis], points[:, i - 1, np.newaxis],
                                                               points[:, (i + 1) % points.shape[1], np.newaxis],
                                                               self.orthoFun)
                    indexes += 3

        return allPoints

    def createCurves(self):
        curves = []

        if self.controlPointsCount > 0:
            sliceStart = 1 if self.closed else 0
            sliceEnd = sliceStart + 4

            for i in xrange(self.controlPointsCount - 1):
                curves.append(BezierCurve(self.allPoints[:, sliceStart:sliceEnd], False))
                sliceStart += 3
                sliceEnd += 3

            if self.closed:
                curves.append(BezierCurve(self.allPoints[:, (-2,-1,0,1)], False)) # FIX IT!

        return curves

    def insertControlPoint(self, point, index):
        if 0 <= index <= self.controlPointsCount:
            pointBefore = None
            pointAfter = None

            if self.allPoints.shape[1] == 0:
                if self.closed:
                    pointBefore = point
                    pointAfter = point
            else:
                if index > 0 or self.closed:
                    pointBefore = self.allPoints[:, self.controlPointIndex(index - 1), np.newaxis]

                if index < self.controlPointsCount or self.closed:
                    pointAfter = self.allPoints[:, self.controlPointIndex(index), np.newaxis]

            self.allPoints = np.insert(self.allPoints, self.insertionIndex(index),
                                       calculateMidpoints(point, pointBefore, pointAfter, self.orthoFun), axis=1)
            self.controlPointsCount += 1
            self.curves = self.createCurves()

    def insertionIndex(self, index):
        if self.closed:
            return 3 * index
        else:
            if index == 0:
                return 0
            elif index == self.controlPointsCount:
                return self.allPoints.shape[1]
            else:
                return 3 * index - 1

    def controlPointIndex(self, index):
        return 3 * (index % self.controlPointsCount) + (1 if self.closed else 0)

def calculateMidpoints(point, pointBefore, pointAfter, orthoFun):
    isBeforeNone = pointBefore is None
    isAfterNone = pointAfter is None
    isBeforeEqPoint = np.array_equal(pointBefore, point)
    isAfterEqPoint = np.array_equal(pointAfter, point)

    if isBeforeNone and isAfterNone:
        return np.array(point)

    elif isBeforeNone:
        midpoints = np.zeros((point.shape[0], 2))
        midpoints[:, 0, np.newaxis] = point
        midpoints[:, 1, np.newaxis] = point + normalizeVectors(orthoFun(pointAfter - point) if not isAfterEqPoint else np.ones(point.shape))

    elif isAfterNone:
        midpoints = np.zeros((point.shape[0], 2))
        midpoints[:, 0, np.newaxis] = point + normalizeVectors(orthoFun(pointBefore - point) if not isBeforeEqPoint else np.ones(point.shape))
        midpoints[:, 1, np.newaxis] = point

    else:
        midpoints = np.zeros((point.shape[0], 3))
        midpoints[:, 1, np.newaxis] = point
        vb = pointBefore - point
        va = pointAfter - point

        if isBeforeEqPoint and isAfterEqPoint:
            normal = normalizeVectors(np.ones(point.shape))

        elif isBeforeEqPoint:
            normal = -normalizeVectors(orthoFun(va))

        elif isAfterEqPoint or (np.dot(normalizeVectors(va).T, normalizeVectors(vb)) == 1).all():
            normal = normalizeVectors(orthoFun(vb))

        else:
            normal = normalizeVectors(pointBefore - pointAfter)

        midpoints[:, 0, np.newaxis] = point + normal
        midpoints[:, 2, np.newaxis] = point - normal

    return midpoints


def normalizeVectors(vs, copy=False):
    result = np.array(vs) if copy else vs
    norms = np.linalg.norm(result, axis=0)

    for i in xrange(result.shape[1]):
        result[:, i] /= norms[i] if norms[i] > 0 else 1

    return result