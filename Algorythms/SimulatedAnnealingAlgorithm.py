from Algorythms.GenericAlgorithm import GenericAlgorithm
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

class SimAnnealingAlgorithm(GenericAlgorithm):

    def __init__(self, list):
        self.x_min = list[0]
        self.x_max = list[1]
        self.y_min = list[2]
        self.y_max = list[3]
        self.steps = list[4]
        self.n_of_points = list[5]

        self.temperature = list[6]

        self.fig, self.ax = plt.subplots()
        self.back = None
        self.ln = None
        self.points = []
        super().__init__()

    def update(self, frame):

        ##update points


        for point in self.points:
            point.update(-1, 1, self.temperature)

        self.temperature = self.temperature * 0.98

        self.ln, = plt.plot([point.x for point in self.points], [point.y for point in self.points],
                            'wo', animated=True, markersize=1)
        return self.ln,


    def init(self):
        self.ax.set_xlim(self.x_min, self.x_max)
        self.ax.set_ylim(self.y_min, self.y_max)

        x = np.linspace(self.x_min, self.x_max, self.steps)
        y = np.linspace(self.y_min, self.y_max, self.steps)
        z = np.array([self.function(i, j) for j in y for i in x])

        X, Y = np.meshgrid(x, y)
        Z = z.reshape(self.steps, self.steps)

        ##init points
        for i in range(0, self.n_of_points):
            self.points.append(ChillingPoint(self.x_min, self.x_max, self.y_min, self.y_max, self.function))

        self.back = plt.pcolormesh(X, Y, Z)
        self.ln, = plt.plot([point.x for point in self.points], [point.y for point in self.points],
                            'wo', animated=True, markersize=1)
        return self.ln,

    def start(self):
        self.animation = FuncAnimation(self.fig, self.update, frames=None, init_func=self.init, blit=True)


    def function(self, x, y):
        ##    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2
        return (x ** 2 + y ** 2 + 25 * (np.sin(x) ** 2 + np.sin(y) ** 2))


class ChillingPoint:

    def __init__(self, x_min, x_max, y_min, y_max, f):
        self.x = random.uniform(x_min, x_max)
        self.y = random.uniform(y_min, y_max)

        self.f = f

    def update(self, d_min, d_max, temperature):
        x = self.x + random.uniform(d_min, d_max)
        y = self.y + random.uniform(d_min, d_max)

        delta = self.f(x, y) - self.f(self.x, self.y)

        r = random.uniform(0,1)

        if delta < 0 :
            self.x = x
            self.y = y

        elif (r < np.exp(-delta/temperature)):
            self.x = x
            self.y = y


if __name__ == "__main__":
    PSO = SimAnnealingAlgorithm([-5, 5, -5, 5, 1001, 100, 5000])
    PSO.start()
    plt.show()