from Algorythms.GenericAlgorythm import GenericAlgorythm
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random


class FireflyAlgorythm(GenericAlgorythm):

    def __init__(self):

        self.x_min = -1
        self.x_max = 3
        self.y_min = -2
        self.y_max = 4
        self.steps = 41
        self.n_flies = 20
        self.delta = -2.4
        self.rand_wander = 0.1

        self.fig, self.ax = plt.subplots()
        self.back = None
        self.ln = None
        self.flies = []

        super().__init__()

    def update(self, frame):

        self.flies.sort(key=lambda f: f.lightness, reverse=True)
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
        z = np.array([((1 - i) ** 2 + 100 * (j - i ** 2) ** 2) for j in y for i in x])

        X, Y = np.meshgrid(x, y)
        Z = z.reshape(self.steps, self.steps)

        for i in range(0, self.n_flies):
            self.flies.append(Firefly(self.x_min, self.x_max, self.y_min, self.y_max, ))

        self.back = plt.pcolormesh(X, Y, Z)
        self.ln, = plt.plot([fly.x for fly in self.flies], [fly.y for fly in self.flies], 'wo',
                            animated=True, markersize=1)

        return self.ln,

    def start(self):
        self.animation = FuncAnimation(self.fig, self.update, frames=None,
                    init_func=self.init, blit=True)


class Firefly:

    def __init__(self, x_min, x_max, y_min, y_max):
        self.x = random.uniform(x_min, x_max)
        self.y = random.uniform(y_min, y_max)
        self.lightness = ((1 - self.x) ** 2 + 100 * (self.y - self.x ** 2) ** 2)
        self.rand_wander = 0.2

    def adjust_lightness(self):
        self.lightness = ((1 - self.x) ** 2 + 100 * (self.y - self.x ** 2) ** 2)

    def move_to(self, other_firefly):
        self.x = self.x + (other_firefly.x - self.x) * random.gauss(0, self.rand_wander)
        self.y = self.y + (other_firefly.y - self.y) * random.gauss(0, self.rand_wander)

    def dist(self, other_firefly):
        return np.sqrt((other_firefly.x - self.x)**2 + (other_firefly.y - self.y)**2)

    def move_rand(self):
        self.x = self.x + random.gauss(0, self.rand_wander)
        self.y = self.y + random.gauss(0, self.rand_wander)

if __name__ == "__main__":
    FfA = FireflyAlgorythm()
    FfA.start()
    plt.show()