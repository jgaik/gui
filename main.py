import tkinter as tk
import gui


class App:

    def __init__(self):
        self.master = tk.Tk()
        self.gui = gui.Gui(self.master)

    def start(self):
        self.master.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
