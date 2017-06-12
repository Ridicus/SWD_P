import numpy as np
import Tkinter as tk
import Cubic2DBezierCurve as c2bc
import TrackVisualizer as tv

controlPoints = np.array([[25,150,180], [25,180,120]], dtype=np.float_)

curve = c2bc.Cubic2DBezierCurve(controlPoints, True)

curve.moveHelperPointTo(0, -1, np.array([[20],[20]], dtype=np.float_))
curve.moveHelperPointTo(0, 1, np.array([[10],[30]], dtype=np.float_))

main = tk.Tk()

canvas = tk.Canvas(main, height=200, width=200)

visualizer = tv.TrackVisualizer(canvas, curve, lambda t: 10, 1000, 2, 5, 'blue', 'red', 'orange')
visualizer.setEditMode(True)

canvas.pack(fill='both', expand=1)
main.mainloop()