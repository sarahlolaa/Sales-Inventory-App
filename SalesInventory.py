try:
    import tkinter as tk
    import tkinter.font as tkFont
except ImportError:
    import Tkinter as tk
    import Tkinter.font as tkFont


from startpage import StartPage

class TkApp(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        
        self.state("zoomed")
        self.title("Sales Inventory Application")

        self.frame = None
        self.switchframe(StartPage)
        

    def switchframe(self, frame_class):
        new_frame = frame_class(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.frame.pack(fill=tk.BOTH, expand=True)


    def check_frame_dimensions(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        return(width, height)


def main():
    App = TkApp()
    App.mainloop()
if __name__ == '__main__':
    main()