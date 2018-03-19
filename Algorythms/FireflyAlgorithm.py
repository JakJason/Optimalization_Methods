from Algorythms.GenericAlgorithm import GenericAlgorithm
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random


class FireflyAlgorithm(GenericAlgorithm):

    def __init__(self, list):
        self.x_min = list[0]
        self.x_max = list[1]
        self.y_min = list[2]
        self.y_max = list[3]
        self.steps = list[4]
        self.n_flies = list[5]
        self.delta = list[6]
        self.rand_wander = list[7]

        self.fig, self.ax = plt.subplots()
        self.back = None
        self.ln = None
        self.flies = []
        super().__init__()

    def update(self, frame):
        atr = None
        for fly in self.flies:
            if fly.lightness == max(f.lightness for f in self.flies):
                fly.move_rand()
            else:
                atr = sorted(self.flies, key=lambda f: (f.lightness * np.exp(fly.dist(f))*self.delta), reverse=True)
                fly.move_to(atr[0])
            fly.adjust_lightness()

        self.ln, = plt.plot([fly.x for fly in self.flies], [fly.y for fly in self.flies], 'wo', animated=True,
                            markersize=1)
        return self.ln,

    def init(self):
        self.ax.set_xlim(self.x_min, self.x_max)
        self.ax.set_ylim(self.y_min, self.y_max)

        x = np.linspace(self.x_min, self.x_max, self.steps)
        y = np.linspace(self.y_min, self.y_max, self.steps)
        z = np.array([self.function(i, j) for j in y for i in x])

        X, Y = np.meshgrid(x, y)
        Z = z.reshape(self.steps, self.steps)

        for i in range(0, self.n_flies):
            self.flies.append(Firefly(self.x_min, self.x_max, self.y_min, self.y_max, self.rand_wander, self.function))

        self.back = plt.pcolormesh(X, Y, Z)
        self.ln, = plt.plot([fly.x for fly in self.flies], [fly.y for fly in self.flies], 'wo',
                            animated=True, markersize=1)
        return self.ln,

    def start(self):
        self.animation = FuncAnimation(self.fig, self.update, frames=None, init_func=self.init, blit=True)

    def function(self, x, y):
        return ((1 - x) ** 2 + 100 * (y - x ** 2) ** 2)


class Firefly:

    def __init__(self, x_min, x_max, y_min, y_max, r, f):
        self.x = random.uniform(x_min, x_max)
        self.y = random.uniform(y_min, y_max)
        self.lightness = ((1 - self.x) ** 2 + 100 * (self.y - self.x ** 2) ** 2)
        self.rand_wander = r
        self.f = f

    def adjust_lightness(self):
        self.lightness = self.f(self.x, self.y)

    def move_to(self, other_firefly):
        r = random.gauss(0, self.rand_wander)
        self.x = self.x + (other_firefly.x - self.x) * r
        self.y = self.y + (other_firefly.y - self.y) * r

    def dist(self, other_firefly):
        return np.sqrt((other_firefly.x - self.x)**2 + (other_firefly.y - self.y)**2)

    def move_rand(self):
        r = random.gauss(-self.rand_wander, self.rand_wander)
        self.x = self.x + r
        self.y = self.y + r


if __name__ == "__main__":
    FfA = FireflyAlgorithm([-3, 5, -3, 5, 81, 100, -0.2, 0.6])
    FfA.start()
    plt.show()
