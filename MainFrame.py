import numpy as np
import Tkinter as tk
import ttk
import Cubic2DBezierCurve as c2bc
import State as state
import SimulationThread as st
import TrackVisualizer as tv

class MainFrame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.discretization = (5, 5, 5, 5, 5)
        self.dt = 0.1
        self.eps = 0.01
        self.maxT = 10.0

        self.running = False
        self.editMode = False

        self.states = []
        self.simulationThread = None

        self.initWidgets()
        self.placeWidgets()
        self.configureGrid()

        self.widthFun = lambda tau: float(self.wScale.get())
        waypointsCountFun = lambda : int(self.divPtsScale.get())
        startPositionFun = lambda : float(self.startPosScale.get())

        self.visualizer = tv.TrackVisualizer(self.canvas,
                                             c2bc.Cubic2DBezierCurve(np.array([[], []], dtype=np.float_), True, 20),
                                             self.widthFun, waypointsCountFun, startPositionFun, 1000, 2, 10,
                                             'blue', 'red', 'green', 'purple', 'orange')

        self.wScale['command'] = lambda x: self.visualizer.paint()

    def initWidgets(self):
        self.wScale = tk.Scale(self, orient='horizontal', from_=0, to=30, label='Szerkosc trasy', state=tk.DISABLED)
        self.divPtsScale = tk.Scale(self, orient='horizontal', from_=2, to=20, label='Liczba punktow kontrolnych',
                                    command=self.divPointsScaleChanged)
        self.startPosScale = tk.Scale(self, orient='horizontal', from_=-1.0, to=1.0, resolution=0.1, label='Pozycja startowa',
                                      command=self.startPosScaleChanged)
        self.bScale = tk.Scale(self, orient='horizontal', from_=0.0, to=2.0, resolution=0.1, label='Parametr oporu powietrza')
        self.vMaxScale = tk.Scale(self, orient='horizontal', from_=0.0, to=20.0, resolution=0.1, label='Predkosc maksymalna')
        self.alphaMaxScale = tk.Scale(self, orient='horizontal', from_=0, to=90, label='Maksymalny kat skretu')

        self.lboxLabel = tk.Label(self, text='Decyzje')
        self.timeLabel = tk.Label(self, text='Minimalny czas: ')

        self.lboxXScroll = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.lboxYScroll = tk.Scrollbar(self, orient=tk.VERTICAL)

        self.decisionListBox = tk.Listbox(self, xscrollcommand=self.lboxXScroll.set, yscrollcommand=self.lboxYScroll.set)
        self.lboxYScroll['command'] = self.decisionListBox.yview
        self.lboxXScroll['command'] = self.decisionListBox.xview

        self.progress = ttk.Progressbar(self, mode='determinate', maximum=2.0 * reduce(lambda acc, x: acc * x, self.discretization, 1.0))

        self.startStopButton = tk.Button(self, text='Start', command=self.startClicked, state=tk.DISABLED)
        self.editButton = tk.Button(self, text='Edytuj trase', command=self.editClicked)

        self.canvas = tk.Canvas(self, bd=4, relief=tk.GROOVE)

    def placeWidgets(self):
        self.wScale.grid(row=0, column=0, columnspan=3, sticky='NEWS')
        self.divPtsScale.grid(row=1, column=0, columnspan=3, sticky='NEWS')
        self.startPosScale.grid(row=2, column=0, columnspan=3, sticky='NEWS')
        self.bScale.grid(row=3, column=0, columnspan=3, sticky='NEWS')
        self.vMaxScale.grid(row=4, column=0, columnspan=3, sticky='NEWS')
        self.alphaMaxScale.grid(row=5, column=0, columnspan=3, sticky='NEWS')

        self.lboxLabel.grid(row=6, column=0, sticky='NEWS')
        self.timeLabel.grid(row=9, column=0, columnspan=2, sticky='NWS')

        self.decisionListBox.grid(row=7, column=0, rowspan=2, columnspan=2, sticky='NEWS')

        self.lboxXScroll.grid(row=9, column=0, columnspan=2, sticky='NEW')
        self.lboxYScroll.grid(row=7, column=2, rowspan=2, sticky='NWS')

        self.progress.grid(row=11, column=0, columnspan=5, sticky='NEWS')

        self.startStopButton.grid(row=8, column=3, rowspan=3)
        self.editButton.grid(row=8, column=4, rowspan=3)

        self.canvas.grid(row=0, column=3, rowspan=7, columnspan=2, sticky='NEWS')

    def configureGrid(self):
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=2)
        self.columnconfigure(4, weight=2)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=2)
        self.rowconfigure(8, weight=2)
        self.rowconfigure(9, weight=1)
        self.rowconfigure(10, weight=1)
        self.rowconfigure(11, weight=1)

    def enableInputWidgets(self):
        self.editButton['state'] = tk.NORMAL
        self.divPtsScale['state'] = tk.NORMAL
        self.bScale['state'] = tk.NORMAL
        self.vMaxScale['state'] = tk.NORMAL
        self.alphaMaxScale['state'] = tk.NORMAL

    def disableInputWidgets(self):
        self.editButton['state'] = tk.DISABLED
        self.divPtsScale['state'] = tk.DISABLED
        self.bScale['state'] = tk.DISABLED
        self.vMaxScale['state'] = tk.DISABLED
        self.alphaMaxScale['state'] = tk.DISABLED

    def startClicked(self):
        self.progress['value'] = 0
        self.states = []
        self.updateDecisionData()

        if self.running:
            self.startStopButton['text'] = 'Start'
            self.running = False
            self.enableInputWidgets()

            self.simulationThread = None

        else:
            self.startStopButton['text'] = 'Stop'
            self.running = True
            self.disableInputWidgets()

            self.simulationThread = st.SimulationThread(self)
            self.simulationThread.start()

    def editClicked(self):
        if self.editMode:
            self.editButton['text'] = 'Edytuj trase'
            self.editMode = False
            self.startStopButton['state'] = tk.NORMAL if self.visualizer.curve.controlPointsCount >= 2 else tk.DISABLED
            self.wScale['state'] = tk.DISABLED

        else:
            self.editButton['text'] = 'Zakoncz edycje'
            self.editMode = True
            self.startStopButton['state'] = tk.DISABLED
            self.wScale['state'] = tk.NORMAL

        self.visualizer.setEditMode(self.editMode)

    def divPointsScaleChanged(self, val):
        self.progress['maximum'] = float(val) * reduce(lambda acc, x: acc * x, self.discretization, 1.0)
        self.visualizer.paint()

    def startPosScaleChanged(self, val):
        self.visualizer.paint()

    def continueExecution(self):
        return self.running

    def getSimulationSpace(self):
        vMax = float(self.vMaxScale.get())
        return state.SimulationSpace(self.visualizer.curve, self.widthFun, vMax, float(self.bScale.get()) * (vMax ** 2) / 2.0,
                                     float(self.alphaMaxScale.get()) * np.pi / 180.0, self.discretization)

    def getSimulationStepsCount(self):
        return int(self.divPtsScale.get()) - 1

    def getBParam(self):
        return float(self.bScale.get())

    def progressStep(self):
        self.progress.step(1.0)

    def finished(self):
        self.progress['value'] = 0
        self.startStopButton['text'] = 'Start'
        self.running = False
        self.enableInputWidgets()

        self.states = self.simulationThread.states
        self.simulationThread = None

        self.updateDecisionData()

    def updateDecisionData(self):
        self.decisionListBox.delete(0, self.decisionListBox.size())

        if len(self.states) == 0:
            self.timeLabel['text'] = 'Minimalny czas: '

        else:
            pass