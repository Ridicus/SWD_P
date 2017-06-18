import threading as th
import State as state
import Simulation as sim

class SimulationThread(th.Thread):
    def __init__(self, mainFrame):
        th.Thread.__init__(self)

        self.daemon = True

        self.mainFrame = mainFrame
        self.simulationSpace = self.mainFrame.getSimulationSpace()
        self.simulationStepsCount = self.mainFrame.getSimulationStepsCount()
        self.tauDelta = 1.0 / self.simulationStepsCount

        self.dt = self.mainFrame.dt
        self.eps = self.mainFrame.eps
        self.maxT = self.mainFrame.maxT

        self.states = [state.LastState(self.simulationSpace)]

    def run(self):
        simulation = sim.Simulation(self.mainFrame.getBParam(), self.dt, self.eps, self.maxT)

        while self.mainFrame.continueExecution() and self.simulationStepsCount > 0:
            nextState = self.states[0]
            print nextState.tArr.min()
            self.states.insert(0, simulation.simulate(nextState, nextState.tau - self.tauDelta,
                                                      lambda : not self.mainFrame.continueExecution(),
                                                      self.mainFrame.progressStep))

            self.simulationStepsCount -= 1

        if self.simulationStepsCount == 0:
            self.mainFrame.finished()