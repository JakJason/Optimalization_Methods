from Algorythms.GenericAlgorithm import GenericAlgorithm
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from tkinter import *


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
        self.f_p = list[8]


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
        if self.f_p == 'Rosenbrock function':
            return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2
        elif self.f_p == 'Eggcrate function':
            return (x ** 2 + y ** 2 + 25 * (np.sin(x) ** 2 + np.sin(y) ** 2))


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


class PSOPanel:

    def __init__(self, panel_frame, plot_frame, error_frame):
        self.algorytm = None
        self.canvas = None
        self.Frame = Frame(panel_frame, highlightbackground="grey", highlightcolor="grey", highlightthickness=5)
        self.P_Frame = Frame(plot_frame, highlightbackground="grey", highlightcolor="grey", highlightthickness=5)
        self.P_Frame.pack()

        self.X_min = StringVar(self.Frame)
        self.X_min_Label = Label(self.Frame, anchor='nw', justify='left', text="X min")
        self.X_min_Label.grid(row=0, column=0, sticky="nsew")
        self.X_min_Entry = Entry(self.Frame, textvariable=self.X_min)
        self.X_min.set(-2)
        self.X_min_Entry.grid(row=0, column=1, sticky="nsew")

        self.X_max = StringVar(self.Frame)
        self.X_max_Label = Label(self.Frame, anchor='nw', justify='left', text="X max")
        self.X_max_Label.grid(row=1, column=0, sticky="nsew")
        self.X_max_Entry = Entry(self.Frame, textvariable=self.X_max)
        self.X_max.set(2)
        self.X_max_Entry.grid(row=1, column=1, sticky="nsew")

        self.Y_min = StringVar(self.Frame)
        self.Y_min_Label = Label(self.Frame, anchor='nw', justify='left', text="Y min")
        self.Y_min_Label.grid(row=2, column=0, sticky="nsew")
        self.Y_min_Entry = Entry(self.Frame, textvariable=self.Y_min)
        self.Y_min.set(-2)
        self.Y_min_Entry.grid(row=2, column=1, sticky="nsew")

        self.Y_max = StringVar(self.Frame)
        self.Y_max_Label = Label(self.Frame, anchor='nw', justify='left', text="Y max")
        self.Y_max_Label.grid(row=3, column=0, sticky="nsew")
        self.Y_max_Entry = Entry(self.Frame, textvariable=self.Y_max)
        self.Y_max.set(2)
        self.Y_max_Entry.grid(row=3, column=1, sticky="nsew")

        self.Resolution = StringVar(self.Frame)
        self.Resolution_Label = Label(self.Frame, anchor='nw', justify='left', text="Resolution")
        self.Resolution_Label.grid(row=4, column=0, sticky="nsew")
        self.Resolution_Entry = Entry(self.Frame, textvariable=self.Resolution)
        self.Resolution.set(101)
        self.Resolution_Entry.grid(row=4, column=1, sticky="nsew")

        self.N = StringVar(self.Frame)
        self.N_Label = Label(self.Frame, anchor='nw', justify='left', text="Number of particles")
        self.N_Label.grid(row=5, column=0, sticky="nsew")
        self.N_Entry = Entry(self.Frame, textvariable=self.N)
        self.N.set(100)
        self.N_Entry.grid(row=5, column=1, sticky="nsew")

        self.Inertia = StringVar(self.Frame)
        self.Inertia_Label = Label(self.Frame, anchor='nw', justify='left', text="Delta")
        self.Inertia_Label.grid(row=6, column=0, sticky="nsew")
        self.Inertia_Entry = Entry(self.Frame, textvariable=self.Inertia)
        self.Inertia.set(0.7)
        self.Inertia_Entry.grid(row=6, column=1, sticky="nsew")

        self.Correction = StringVar(self.Frame)
        self.Correction_Label = Label(self.Frame, anchor='nw', justify='left', text="Random wandering")
        self.Correction_Label.grid(row=7, column=0, sticky="nsew")
        self.Correction_Entry = Entry(self.Frame, textvariable=self.Correction)
        self.Correction.set(1.4)
        self.Correction_Entry.grid(row=7, column=1, sticky="nsew")

        self.Fun_opt_Label = Label(self.Frame, anchor='nw', justify='left', text="Function")
        self.Fun_opt_Label.grid(row=8, column=0, sticky="nsew")
        self.Fun_opt = StringVar(self.Frame)
        self.Fun_opt.set('Rosenbrock function')
        self.Menu = OptionMenu(self.Frame, self.Fun_opt,
                               'Rosenbrock function',
                               'Eggcrate function')
        self.Menu.grid(row=8, column=1, sticky="nsew")

        self.Create_button = Button(self.Frame, text='Load Algorithm', state=NORMAL, width=10, height=2,
                                    command=self.Start_Algorytm)
        self.Create_button.grid(row=9, column=0, columnspan=2, sticky="nsew")
        self.Clear_button = Button(self.Frame, text='Clear Algorithm', state=NORMAL, width=10, height=2,
                                    command=self.Clear_Algorytm)
        self.Clear_button.grid(row=10, column=0, columnspan=2, sticky="nsew")

    def Start_Algorytm(self):
        if self.algorytm is not None:
            self.algorytm = None
        if self.canvas is not None:
            self.canvas.get_tk_widget().forget()
        arg_list = [float(self.X_min.get()), float(self.X_max.get()),
                    float(self.Y_min.get()), float(self.Y_max.get()),
                    int(self.Resolution.get()),
                    int(self.N.get()),
                    float(self.Inertia.get()),
                    float(self.Correction.get()),
                    self.Fun_opt.get()]
        self.algorytm = PSOAlgorithm(arg_list)
        self.algorytm.init()
        self.canvas = FigureCanvasTkAgg(self.algorytm.fig, master=self.P_Frame)
        self.canvas.get_tk_widget().grid(row=0, column=0)
        self.algorytm.start()

    def Clear_Algorytm(self):
        self.P_Frame.destroy()
        if self.algorytm is not None:
            self.algorytm = None


if __name__ == "__main__":
    PSO = PSOAlgorithm([-5, 5, -5, 5, 1001, 100, 0.7, 1.4, 'Rosenbrock function'])
    PSO.start()
    plt.show()

