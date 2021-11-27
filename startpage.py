try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

from userlogin import UserLogIn
from userregister import UserRegister

#first window frame: startPage
class StartPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.entry_frame = None
        self.login_btn = None
        self.color_one = "gray86"
        self.color_two = "gray80"     
    
        # Create a container frame
        self.container_frame = tk.Frame(self, bg = self.color_one)
        self.container_frame.pack(pady = 50)
        
        
        self.page_btn_frame = tk.Frame(self.container_frame, bg = self.color_one)
        self.page_btn_frame.grid(row=0, column=0)
        
        self.show_login()

        
        self.entry_btn_frame = tk.Frame(self.container_frame, bg = self.color_one)
        self.entry_btn_frame.grid(row=2, column=0)
        
        
#         #Create login page and register page buttons.
        self.login_page_btn = tk.Button(self.page_btn_frame, text = "LOGIN", width = 16, bg = self.color_two, 
                                   font = ("Helvetica", 10, "bold"), command = self.show_login)  
        
        self.register_btn = tk.Button(self.page_btn_frame, text = "REGISTER", width = 16, bg = self.color_two,
                                   font = ("Helvetica", 10, "bold"), command = self.show_register)
        
          #Create login/register and reset buttons.
        self.login_btn = tk.Button(self.entry_btn_frame, text = "Login", width = 16, bg = self.color_two, 
                                   font = ("Helvetica", 10, "bold"), command = self.entry_frame.login)
        
        self.reset_btn = tk.Button(self.entry_btn_frame, text = "Reset", width = 16, bg = self.color_two,
                                   font = ("Helvetica", 10, "bold"), command = self.reset)
        
        
        self.login_page_btn.grid(row = 0, column = 0, padx = (20, 10))
        self.register_btn.grid(row = 0, column = 1, padx = (10, 20))
        self.login_btn.grid(row = 0, column = 0, padx =  (20, 10))
        self.reset_btn.grid(row = 0, column = 1, padx = (10, 20))
        
        

    def switch_content_frame(self, entry_frame_class):
        new_entry_frame = entry_frame_class(self.container_frame, self)
        if self.entry_frame is not None:
            self.entry_frame.destroy()
        self.entry_frame = new_entry_frame
        self.entry_frame.grid(row=1, column=0)
        
    def show_register(self):
        self.switch_content_frame(UserRegister)
        if self.login_btn is not None:
            self.login_btn.config(text="Register")
            self.login_btn.config(command=self.entry_frame.register)
        
        
    def show_login(self):
        self.switch_content_frame(UserLogIn) 
        if self.login_btn is not None:
            self.login_btn.config(text="Login")
            self.login_btn.config(command=self.entry_frame.login)        
            
            
    def reset(self):
        """Resets both name and password entry fields to an empty state.
        Moves the cursor to the start of the name entry field."""
        self.entry_frame.reset()

    
