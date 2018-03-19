from Algorythms.GenericAlgorithm import GenericAlgorithm
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class LinearCongruentRNG(GenericAlgorithm):

    def __init__(self, list):

        self.mod = list[0]
        self.a = list[1]
        self.c = list[2]
        self.seed = list[3]

        self.fig, self.ax = plt.subplots()
        self.xdata, self.ydata = [], []

        self.ln = None

        super().__init__()

    def update(self, frame):

        if frame == 0:
            self.xdata.append((self.seed % self.mod))# / self.mod)
            print("X: "+((self.seed % self.mod)).__str__())
        else:
            self.xdata.append(((self.ydata[frame-1]*self.a + self.c) % self.mod) / self.mod)
            print("X: "+(((self.ydata[frame-1]*self.a + self.c) % self.mod)).__str__())


        self.ydata.append(((self.xdata[frame]*self.a + self.c) % self.mod))# / self.mod)
        print("Y: " + (((self.xdata[frame]*self.a + self.c) % self.mod)).__str__())

        self.ln.set_data(self.xdata, self.ydata)

        return self.ln,

    def init(self):
        self.ax.set_xlim(0, self.mod)
        self.ax.set_ylim(0, self.mod)

        self.ln, = plt.plot([], [], 'rs', animated=True, markersize=1)
        return self.ln,

    def start(self):
        self.animation = FuncAnimation(self.fig, self.update, frames=None, init_func=self.init, blit=True)

if __name__ == "__main__":

    RNG = LinearCongruentRNG([1,1,1,1])
    RNG.start()
    plt.show()
