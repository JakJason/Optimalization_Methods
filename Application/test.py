from tkinter import *
from Algorythms import FireflyAlgorithm, PSOAlgorithm, SimulatedAnnealingAlgorithm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class MyApp():

    def __init__(self):
        self.master = Tk()
        self.master.title('Optimalization Methods')
        self.master.configure(background='grey')
        self.master.minsize(width=400, height=300)

        # Base Frame
        self.Base_Frame = Frame(highlightbackground="grey", highlightcolor="grey", highlightthickness=5)
        self.Base_Frame.configure(background='grey')
        self.Alg_Name = StringVar(self.Base_Frame)
        self.Alg_Name.set('No Algorithm')
        self.Menu = OptionMenu(self.Base_Frame, self.Alg_Name,
                               'Firefly Algorithm',
                               'PSO Algorithm',
                               'Simulated Annealing')
        self.Menu.grid(row=0, column=0, sticky="nsew")
        self.Panel_Button = Button(self.Base_Frame, text='Load Algorithm', state=NORMAL, width=20, height=2,
                                   command=self.Load_Panel)
        self.Panel_Button.grid(row=0, column=1, sticky="nsew")

        # Panel Frame
        self.Panel = None
        self.Panel_Frame = Frame(highlightbackground="grey", highlightcolor="grey", highlightthickness=5)
        self.Panel_Frame.configure(background='grey')

        # Plot Frame
        self.Plot_Frame = Frame(highlightbackground="grey", highlightcolor="grey", highlightthickness=5)
        self.Plot_Frame.configure(background='grey')

        # Error Frame
        self.Error_Frame = Frame(highlightbackground="grey", highlightcolor="grey", highlightthickness=5)
        self.Error_Frame.configure(background='grey')
        self.Error_label = Label(self.Error_Frame, anchor='nw', justify='left',)
        self.Error_label.grid(row=0, column=0, sticky="nsew")

        self.Base_Frame.grid(row=0, column=0, sticky="nsew")
        self.Error_Frame.grid(row=0, column=1, sticky="nsew")
        self.Panel_Frame.grid(row=1, column=0, sticky="nsew")
        self.Plot_Frame.grid(row=1, column=1, sticky="nsew")

    def Load_Panel(self):

        if self.Panel is not None:
            self.Panel.Frame.destroy()

        if self.Alg_Name.get() == 'No Algorithm':
            self.Panel = None
        elif self.Alg_Name.get() == 'Firefly Algorithm':
            self.Panel = FireflyAlgorithm.FireflyPanel(self.Panel_Frame, self.Plot_Frame, self.Error_Frame)
        elif self.Alg_Name.get() == 'PSO Algorithm':
            self.Panel = PSOAlgorithm.PSOPanel(self.Panel_Frame, self.Plot_Frame, self.Error_Frame)
        elif self.Alg_Name.get() == 'Simulated Annealing':
            self.Panel = SimulatedAnnealingAlgorithm.AnnealingPanel(self.Panel_Frame, self.Plot_Frame, self.Error_Frame)
        elif self.Alg_Name.get() == 'No Algorithm':
            pass

        if self.Panel is not None:
            self.Panel.Frame.pack()

def main():
    p = MyApp()
    p.master.mainloop()


if __name__ == '__main__':
    main()