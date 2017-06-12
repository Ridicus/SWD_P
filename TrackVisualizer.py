import numpy as np
import Tkinter as tk
import CubicBezierCurve as cbc
import Cubic2DBezierCurve as c2bc

class TrackVisualizer(object):
    def __init__(self, canvas, curve, widthFun, steps, pointSize, clickDistance, trackColor, borderColor, pointColor):
        self.canvas = canvas
        self.curve = curve
        self.widthFun = widthFun
        self.steps = steps
        self.pointSize = pointSize
        self.clickDistance = clickDistance

        canvas.bind('<Button-1>', lambda e: self.mousePressed(e))
        canvas.bind('<B1-Motion>', lambda e: self.mouseHeld(e))
        canvas.bind('<ButtonRelease-1>', lambda e: self.mouseReleased(e))

        self.ts = np.array(xrange(self.steps + 1), dtype=np.float_)
        self.ts /= self.steps

        self.widths = np.vectorize(self.widthFun)(self.ts)

        self.ind = None
        self.off = None

        self.trackColor = trackColor
        self.borderColor = borderColor
        self.pointColor = pointColor

        self.editMode = False

        self.paint()

    def setEditMode(self, editMode):
        self.editMode = editMode
        self.paint()

    def paint(self):
        canvas = self.canvas
        canvas.delete(tk.ALL)

        (trackPoints, tangents) = self.curve(self.ts)
        normals = cbc.normalizeVectors(c2bc.orthogonal2DVector(tangents))
        borderPoints1 = trackPoints + self.widths * normals
        borderPoints2 = trackPoints - self.widths * normals

        for i in xrange(trackPoints.shape[1] - 1):
            j = i + 1
            canvas.create_line(trackPoints[0, i], trackPoints[1, i],
                               trackPoints[0, j], trackPoints[1, j], fill=self.trackColor)
            canvas.create_line(borderPoints1[0, i], borderPoints1[1, i],
                               borderPoints1[0, j], borderPoints1[1, j], fill=self.borderColor)
            canvas.create_line(borderPoints2[0, i], borderPoints2[1, i],
                               borderPoints2[0, j], borderPoints2[1, j], fill=self.borderColor)

        if self.editMode:
            for i in xrange(self.curve.controlPointsCount):
                self.drawPoints(i)


    def drawPoints(self, index):
        canvas = self.canvas
        curve = self.curve
        controlPointIndex = curve.controlPointIndex(index)

        point = curve.allPoints[:, controlPointIndex]
        fstHelper = None
        sndHelper = None

        if index > 0:
            fstHelper = curve.allPoints[:, controlPointIndex - 1]

        elif curve.closed and index == 0:
            fstHelper = curve.allPoints[:, -2]

        if curve.closed or index < curve.controlPointsCount - 1:
            sndHelper = curve.allPoints[:, controlPointIndex + 1]

        if fstHelper is not None:
            canvas.create_line(point[0], point[1], fstHelper[0], fstHelper[1], fill=self.pointColor)
            canvas.create_rectangle(fstHelper[0] - self.pointSize, fstHelper[1] - self.pointSize,
                                    fstHelper[0] + self.pointSize, fstHelper[1] + self.pointSize,
                                    outline=self.pointColor, fill=self.pointColor)

        if sndHelper is not None:
            canvas.create_line(point[0], point[1], sndHelper[0], sndHelper[1], fill=self.pointColor)
            canvas.create_rectangle(sndHelper[0] - self.pointSize, sndHelper[1] - self.pointSize,
                                    sndHelper[0] + self.pointSize, sndHelper[1] + self.pointSize,
                                    outline=self.pointColor, fill=self.pointColor)

        canvas.create_oval(point[0] - self.pointSize, point[1] - self.pointSize,
                           point[0] + self.pointSize, point[1] + self.pointSize,
                                outline=self.pointColor, fill=self.pointColor)

    def mousePressed(self, event):
        if self.editMode:
            (self.ind, self.off) = self.curve.getNearestTableIndices(np.array([[event.x], [event.y]], dtype=np.float_), self.clickDistance)

    def mouseHeld(self, event):
        if self.editMode:
            point = np.array([[event.x], [event.y]], dtype=np.float_)

            if self.ind is None:
                pass

            elif self.off != 0:
                self.curve.moveHelperPointTo(self.ind, self.off, point)

            else:
                self.curve.moveControlPointTo(self.ind, point)

            self.paint()

    def mouseReleased(self, event):
        (self.ind, self.off) = (None, None)