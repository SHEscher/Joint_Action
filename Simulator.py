from Formulas import *
from RollingBot import CatchBot


class Simulate:
    '''
    ...
    '''

    def __init__(self, simlength = 500):
        self.agent = CatchBot()
        self.simlength = simlength


    def run(self):
        self.agent.movement(self.simlength)
        return np.matrix(self.agent.position)


    def run_and_plot(self):

        pos = np.matrix(self.agent.position)

        for _ in np.arange(self.simlength):
            self.agent.movement()
            pos = np.concatenate((pos, np.matrix(self.agent.position)))

        plt.plot(pos[:,0],pos[:,1] )
        plt.plot(pos[-1,0],pos[-1,1], 'ro' )
        # plt.plot(self.agent.position_target[0], self.agent.position_target[1], 'ro')
        # plt.axis([0, 100, 0, 100])


# Simulate(1000).run_and_plot()