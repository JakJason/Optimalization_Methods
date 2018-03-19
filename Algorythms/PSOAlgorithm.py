from Algorythms.GenericAlgorithm import GenericAlgorithm
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random


class PSOAlgorithm(GenericAlgorithm):

    def __init__(self, list):
        self.x_min = list[0]
        self.x_max = list[1]
        self.y_min = list[2]
        self.y_max = list[3]
        self.steps = list[4]
        self.n_particles = list[5]
        self.inertia = list[6]
        self.correction = list[7]

        self.best_x = 0
        self.best_y = 0
        self.fig, self.ax = plt.subplots()
        self.back = None
        self.ln = None
        self.particles = []
        super().__init__()

    def update(self, frame):

        for particle in self.particles:
            particle.update_velocity(self.best_x, self.best_y, self.inertia, self.correction)
            particle.move()
            particle.check_best()
            if particle.f(particle.x, particle.y) <= self.function(self.best_x, self.best_y):
                self.best_x = particle.x
                self.best_y = particle.y

        self.ln, = plt.plot([particle.x for particle in self.particles], [particle.y for particle in self.particles],
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

        for i in range(0, self.n_particles):
            self.particles.append(Particle(self.x_min, self.x_max, self.y_min, self.y_max, self.function))
            if i == 0:
                self.best_x = self.particles[i].x
                self.best_y = self.particles[i].y
            else:
                if self.function(self.particles[i].x, self.particles[i].y) < self.function(self.best_x, self.best_y):
                    self.best_x = self.particles[i].x
                    self.best_y = self.particles[i].y

        self.back = plt.pcolormesh(X, Y, Z)
        self.ln, = plt.plot([particle.x for particle in self.particles], [particle.y for particle in self.particles],
                            'wo', animated=True, markersize=1)
        return self.ln,

    def start(self):
        self.animation = FuncAnimation(self.fig, self.update, frames=None, init_func=self.init, blit=True)

    def function(self, x, y):
        return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2


class Particle:

    def __init__(self, x_min, x_max, y_min, y_max, f):
        self.x = random.uniform(x_min, x_max)
        self.y = random.uniform(y_min, y_max)
        self.best_x = self.x
        self.best_y = self.y
        self.v_x = random.uniform(-(x_max - x_min)/2, (x_max - x_min)/2)
        self.v_y = random.uniform(-(y_max - y_min)/2, (y_max - y_min)/2)
        self.f = f

    def update_velocity(self, global_best_x, global_best_y, inertia, correction):
        r1 = random.uniform(0, 1)
        r2 = random.uniform(0, 1)

        self.v_x = inertia * self.v_x + correction * r1 * (self.best_x - self.x) + \
                   correction * r2 * (global_best_x - self.x)
        self.v_y = inertia * self.v_y + correction * r1 * (self.best_y - self.y) + \
                   correction * r2 * (global_best_y - self.y)

    def move(self):
        self.x = self.x + self.v_x
        self.y = self.y + self.v_y

    def check_best(self):
        if self.f(self.x, self.y) < self.f(self.best_x, self.best_y):
            self.best_x = self.x
            self.best_y = self.y


if __name__ == "__main__":
    PSO = PSOAlgorithm([-5, 5, -5, 5, 1001, 100, 0.7, 1.4])
    PSO.start()
    plt.show()

