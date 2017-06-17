import numpy as np
import Tkinter as tk
import ttk
import Cubic2DBezierCurve as c2bc
import TrackVisualizer as tv

class MainFrame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.running = False
        self.editMode = False

        self.initWidgets()
        self.placeWidgets()
        self.configureGrid()

        self.visualizer = tv.TrackVisualizer(self.canvas,
                                             c2bc.Cubic2DBezierCurve(np.array([[], []], dtype=np.float_), True, 20),
                                             lambda tau: self.wScale.get(), 1000, 2, 10, 'blue', 'red', 'orange')
        # self.columnconfigure(0, weight=1)
        # self.columnconfigure(1, weight=1)
        # self.columnconfigure(2, weight=1)

        # self.rowconfigure(0, weight=1)

    def initWidgets(self):
        self.wScale = tk.Scale(self, orient='horizontal', from_=0, to=30, label='Szerkosc trasy')
        self.divPtsScale = tk.Scale(self, orient='horizontal', from_=2, to=20, label='Liczba punktow podzialu')
        self.bScale = tk.Scale(self, orient='horizontal', from_=0.0, to=2.0, resolution=0.1, label='Parametr b')
        self.vMaxScale = tk.Scale(self, orient='horizontal', from_=0.0, to=20.0, label='Predkosc maksymalna')
        self.alphaMaxScale = tk.Scale(self, orient='horizontal', from_=0, to=90, label='Maksymalny kat skretu')

        self.lboxLabel = tk.Label(self, text='Decyzje')

        self.lboxScroll = tk.Scrollbar(self, orient=tk.VERTICAL)

        self.decisionListBox = tk.Listbox(self, yscrollcommand=self.lboxScroll.set)
        self.lboxScroll['command'] = self.decisionListBox.yview

        self.progress = ttk.Progressbar(self, mode='determinate')

        self.startStopButton = tk.Button(self, text='Start', command=self.startClicked)
        self.editButton = tk.Button(self, text='Edytuj trase', command=self.editClicked)

        self.canvas = tk.Canvas(self, bd=4, relief=tk.GROOVE)

    def placeWidgets(self):
        self.wScale.grid(row=0, column=0, columnspan=3, sticky='NEWS')
        self.divPtsScale.grid(row=1, column=0, columnspan=3, sticky='NEWS')
        self.bScale.grid(row=2, column=0, columnspan=3, sticky='NEWS')
        self.vMaxScale.grid(row=3, column=0, columnspan=3, sticky='NEWS')
        self.alphaMaxScale.grid(row=4, column=0, columnspan=3, sticky='NEWS')

        self.lboxLabel.grid(row=5, column=0, sticky='NEWS')

        self.decisionListBox.grid(row=6, column=0, rowspan=2, columnspan=2, sticky='NEWS')

        self.lboxScroll.grid(row=6, column=2, rowspan=2, sticky='NWS')

        self.progress.grid(row=8, column=0, columnspan=5, sticky='NEWS')

        self.startStopButton.grid(row=7, column=3)
        self.editButton.grid(row=7, column=4)

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
        self.rowconfigure(6, weight=2)
        self.rowconfigure(7, weight=2)
        self.rowconfigure(8, weight=1)


    def startClicked(self):
        if self.running:
            self.startStopButton['text'] = 'Start'
            self.running = False
        else:
            self.startStopButton['text'] = 'Stop'
            self.running = True

    def editClicked(self):
        if self.editMode:
            self.editButton['text'] = 'Edytuj trase'
            self.editMode = False
        else:
            self.editButton['text'] = 'Zakoncz edycje'
            self.editMode = True