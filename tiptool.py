try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

#TipTool Class
class TipTool():
    def __init__(self, widget, container, text="Object Info"):
        self.waittime = 500
        self.wraplength = 190
        self.widget = widget
        self.text = text
        self.container = container
        self.widget.bind("<Enter>", self.enter_widget)
        self.widget.bind("<Leave>", self.leave_widget)
        self.id = None
        self.topwindow = None
        
    def enter_widget(self, event=None):
        self.schedule()
        
    def leave_widget(self, event=None):
        self.unschedule()
        self.undisplay_tip()
        
    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.display_tip)
        
    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)
    
    def display_tip(self, event=None):
        def tip_position(widget, label, tip_delta = (10,5)):
            try:
                w = widget

                screen_width, screen_height = self.container.parent.check_frame_dimensions()

                width, height = (8 + label.winfo_reqwidth(), 8 + label.winfo_reqheight())

                mouse_x, mouse_y = w.winfo_pointerxy()

                x1, y1 = mouse_x + tip_delta[0], mouse_y + tip_delta[1]
                x2, y2 = x1 + width, y1 + height

                x_delta = x2 - screen_width
                if x_delta < 0:
                    x_delta = 0

                y_delta = y2 - screen_height
                if y_delta < 0:
                    y_delta = 0

                offscreen = (x_delta, y_delta) != (0,0)

                if offscreen:
                    if x_delta:
                        x1 = mouse_x - tip_delta[0] - width

                    if y_delta:
                        y1 = mouse_y - tip_delta[1] - height

                offscreen_again = y1 < 0

                if offscreen_again:
                    y1 = 0

                return x1, y1
            except:
                x = y = 0
                x, y, cx, cy = self.widget.bbox("insert")
                x += self.w.winfo_rootx() + 25
                y += self.w.winfo_rooty() + 20
                
                return x, y
                
        
        self.topwindow = tk.Toplevel(self.widget)
        self.topwindow.wm_overrideredirect(True)

        label_tip = tk.Label(self.topwindow, text=self.text, justify='left', background="#ffffff", relief="solid",
                            borderwidth=1, wraplength = self.wraplength)
        label_tip.grid(ipadx = 4, ipady = 4, sticky = 'nsew')
        
        x, y = tip_position(self.widget, label_tip)
        
        self.topwindow.wm_geometry("+%d+%d" %(x, y))
        
    def undisplay_tip(self):
        topwindow = self.topwindow
        self.topwindow = None
        if topwindow: 
            topwindow.destroy()
