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
        allPoints = np.zeros((points.shape[0], 3 * points.shape[1] + (0 if points.shape[1] == 0 else (1 if self.closed else -2))))

        if points.shape[1] > 0:
            if not self.closed and points.shape[1] == 1:
                allPoints[:, 0, np.newaxis] = points

            else:
                if self.closed:
                    allPoints[:, (-2, 0, 1)] = calculateMidpoints(points[:, 0, np.newaxis], points[:, -1, np.newaxis],
                                                                  points[:, 0 if points.shape[1] == 1 else 1, np.newaxis],
                                                                  self.orthoFun)
                    allPoints[:, -1, np.newaxis] = points[:, 0, np.newaxis]
                    pointsRange = xrange(1, points.shape[1])

                else:
                    allPoints[:, (0, 1)] = calculateMidpoints(points[:, 0, np.newaxis], None, points[:, 1, np.newaxis],
                                                              self.orthoFun)
                    allPoints[:, (-2, -1)] = calculateMidpoints(points[:, -1, np.newaxis], points[:, -2, np.newaxis],
                                                                None, self.orthoFun)
                    pointsRange = xrange(1, points.shape[1] - 1)

                sliceStart = 2
                sliceEnd = sliceStart + 3

                for i in pointsRange:
                    allPoints[:, sliceStart:sliceEnd] = calculateMidpoints(points[:, i, np.newaxis], points[:, i - 1, np.newaxis],
                                                               points[:, (i + 1) % points.shape[1], np.newaxis],
                                                               self.orthoFun)
                    sliceStart += 3
                    sliceEnd += 3

        return allPoints

    def createCurves(self):
        curves = []

        if self.controlPointsCount > 0:
            sliceStart = 0
            sliceEnd = sliceStart + 4

            for i in xrange(self.controlPointsCount - (0 if self.closed else 1)):
                curves.append(BezierCurve(self.allPoints[:, sliceStart:sliceEnd], False))
                sliceStart += 3
                sliceEnd += 3

        return curves

    def insertControlPoint(self, point, index):
        if 0 <= index <= self.controlPointsCount:

            if self.controlPointsCount == 0:
                if self.closed:
                    self.allPoints = np.zeros((self.allPoints.shape[0], 4))
                    self.allPoints[:, (-2, 0, 1)] = calculateMidpoints(point, point, point, self.orthoFun)
                    self.allPoints[:, -1, np.newaxis] = point

                else:
                    self.allPoints = np.insert(self.allPoints, (0, ), point, axis=1)

            elif self.controlPointsCount == 1 and not self.closed:
                self.allPoints = np.insert(self.allPoints, (index,), np.zeros((self.allPoints.shape[0], 3)), axis=1)
                self.allPoints[:, -index, np.newaxis] = point
                self.allPoints[:, :2] = calculateMidpoints(self.allPoints[:, 0, np.newaxis], None,
                                                            self.allPoints[:, -1, np.newaxis], self.orthoFun)
                self.allPoints[:, -2:] = calculateMidpoints(self.allPoints[:, -1, np.newaxis],
                                                            self.allPoints[:, 0, np.newaxis], None, self.orthoFun)

            elif 0 < index and (index < self.controlPointsCount or self.closed):
                self.allPoints = np.insert(self.allPoints, (self.insertionIndex(index), ),
                                           calculateMidpoints(point,
                                                              self.allPoints[:, self.controlPointIndex(index - 1), np.newaxis],
                                                              self.allPoints[:, self.controlPointIndex(index + 1), np.newaxis],
                                                              self.orthoFun), axis=1)

            elif index == 0:
                self.allPoints = np.insert(self.allPoints, (0,), np.zeros((self.allPoints.shape[0], 3)), axis=1)

                if self.closed:
                    self.allPoints[:, 2, np.newaxis] = self.allPoints[:, -2, np.newaxis]
                    self.allPoints[:, (-2, 0, 1)] = calculateMidpoints(point,
                                                                       self.allPoints[:, self.controlPointIndex(-1), np.newaxis],
                                                                       self.allPoints[:, self.controlPointIndex(1), np.newaxis],
                                                                       self.orthoFun)
                    self.allPoints[:, -1, np.newaxis] = point

                else:
                    oldStartPointIndex = self.controlPointIndex(1)
                    oldStartPoint = self.allPoints[:, oldStartPointIndex, np.newaxis]
                    self.allPoints[:, (0, 1)] = calculateMidpoints(point, None, oldStartPoint, self.orthoFun)

                    self.allPoints[:, 2, np.newaxis] = oldStartPoint - normalizeVectors(self.allPoints[:, oldStartPointIndex + 1, np.newaxis]
                                                                                        - oldStartPoint)

            else:
                oldEndPointIndex = self.controlPointIndex(-1)
                oldEndPoint = self.allPoints[:, oldEndPointIndex, np.newaxis]
                self.allPoints = np.insert(self.allPoints, (oldEndPointIndex + 1,), np.zeros((self.allPoints.shape[0], 3)), axis=1)
                self.allPoints[:, -2:] = calculateMidpoints(point, oldEndPoint, None, self.orthoFun)
                self.allPoints[:, -3, np.newaxis] = oldEndPoint - normalizeVectors(self.allPoints[:, oldEndPointIndex - 1, np.newaxis]
                                                                                  - oldEndPoint)

            self.controlPointsCount += 1
            self.curves = self.createCurves()

    def deleteControlPoint(self, index):
        if 0 <= index < self.controlPointsCount:
            deletionIndex = self.insertionIndex(index)
            deletionCount = 3

            if self.controlPointsCount == 1:
                deletionCount = self.allPoints.shape[1]

            elif index == 0 and self.closed:
                self.allPoints[:, -2:] = self.allPoints[:, 2:4]

            elif index == self.controlPointsCount - 1 and not self.closed:
                deletionIndex -= 1

            self.allPoints = np.delete(self.allPoints, xrange(deletionIndex, deletionIndex + deletionCount), axis=1)
            self.controlPointsCount -= 1
            self.curves = self.createCurves()

    def translateControlPoint(self, index, vector):
        if 0 <= index < self.controlPointsCount:
            segmentIndex = self.insertionIndex(index)
            segmentSize = 3

            if self.controlPointsCount == 1:
                segmentSize = self.allPoints.shape[1]

            elif index == 0:
                segmentSize = 2

                if self.closed:
                    self.allPoints[:, -2:] += vector

            elif index == self.controlPointsCount - 1 and not self.closed:
                segmentSize = 2

            self.allPoints[:, segmentIndex:(segmentIndex + segmentSize)] += vector

    def insertionIndex(self, index):
        return 0 if index == 0 else 3 * index - 1

    def controlPointIndex(self, index):
        return 3 * (index % self.controlPointsCount)

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