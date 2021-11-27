try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

class ScrollableFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
    
        self.display_canvas = tk.Canvas(self, bg = "white")
        
        vertical_scrollbar = tk.Scrollbar(self, orient = tk.VERTICAL)
        vertical_scrollbar.pack(side = "right", fill = "y")
        
        horizontal_scrollbar = tk.Scrollbar(self, orient = tk.HORIZONTAL)
        horizontal_scrollbar.pack(side = "bottom", fill = "x")
        
        self.canvas_frame = tk.Frame(self.display_canvas)
        self.display_canvas.create_window((0, 0), window = self.canvas_frame, anchor = "nw")
        
        self.display_canvas.configure(yscrollcommand = vertical_scrollbar.set, 
                                      xscrollcommand = horizontal_scrollbar.set)
        
        vertical_scrollbar.config(command = self.display_canvas.yview)
        horizontal_scrollbar.configure(command = self.display_canvas.xview)
        
        self.canvas_frame.bind("<Configure>", self.vertical_configure)
        self.canvas_frame.bind("<Configure>", self.horizontal_configure)
        
        self.display_canvas.pack(side = "left", fill = "both", expand = True)
        
    def vertical_configure(self, event):
        self.display_canvas.config(scrollregion = self.display_canvas.bbox("all"))
        
    def horizontal_configure(self, event):
        self.display_canvas.configure(scrollregion = self.display_canvas.bbox("all"))