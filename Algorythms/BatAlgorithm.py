from Algorythms.GenericAlgorithm import GenericAlgorithm
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random


class BatAlgorithm:

    def __init__(self, list):
        self.x_min = list[0]
        self.x_max = list[1]
        self.y_min = list[2]
        self.y_max = list[3]
        self.steps = list[4]
        self.n_vampires = list[5]
        self.min_freq = list[6]
        self.max_freq = list[7]
        self.min_loudness = list[8]
        self.max_loudness = list[9]

        self.fig, self.ax = plt.subplots()
        self.back = None
        self.ln = None
        self.vampires = []
        super().__init__()

    def update(self, frame):

        ## update vampires


        return self.ln,

    def init(self):
        self.ax.set_xlim(self.x_min, self.x_max)
        self.ax.set_ylim(self.y_min, self.y_max)

        x = np.linspace(self.x_min, self.x_max, self.steps)
        y = np.linspace(self.y_min, self.y_max, self.steps)
        z = np.array([self.function(i, j) for j in y for i in x])

        X, Y = np.meshgrid(x, y)
        Z = z.reshape(self.steps, self.steps)

        ##init vampires
        for i in range(0, self.n_vampires):
            self.vampires.append(Vampire(self.x_min, self.x_max, self.y_min, self.y_max, self.min_freq, self.max_freq, self.min_loudness, self.max_loudness, self.function))



        self.back = plt.pcolormesh(X, Y, Z)
        self.ln, = plt.plot([vampire.x for vampire in self.vampires], [vampire.y for vampire in self.vampires],
                            'wo', animated=True, markersize=1)
        return self.ln,

    def start(self):
        self.animation = FuncAnimation(self.fig, self.update, frames=None, init_func=self.init, blit=True)

    def function(self, x, y):
        return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2


class Vampire:

    def __init__(self, x_min, x_max, y_min, y_max, f_min, f_max, A_min, A_max, function):
        self.x = random.uniform(x_min, x_max)
        self.y = random.uniform(y_min, y_max)
        self.v_x = random.uniform(-(x_max - x_min)/2, (x_max - x_min)/2)
        self.v_y = random.uniform(-(y_max - y_min)/2, (y_max - y_min)/2)

        self.frequency = random.uniform(f_min, f_max)
        self.loudness = random.uniform(A_min, A_max)
        self.rate = random.uniform(0, 1)

    def move(self):
        self.x = self.x + self.v_x
        self.y = self.y + self.v_y

    def update(self):
        pass


if __name__ == "__main__":
    Bat = BatAlgorithm([-5, 5, -5, 5, 1001, 100, 0, 10, 0, 1])
    Bat.start()
    plt.show()
