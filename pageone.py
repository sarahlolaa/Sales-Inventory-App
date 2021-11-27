try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

from adminpage import AdminPage 

class PageOne(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.color_three = "gray80"
        self.shown_frame = None

        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 1)
        
        self.nav_button_frame = tk.Frame(self)
        self.nav_button_frame.grid(row = 0, sticky = 'ew')
       
        
        self.logout_btn = tk.Button(self.nav_button_frame, text = "Logout", width = 10, font = ("Helvetica", 10, "bold"),
                                    bg = self.color_three, command = self.logout) 
        self.staff_rec_btn = tk.Button(self.nav_button_frame, text = "Staff", width = 10, font = ("Helvetica", 10, "bold"),
                                    bg = self.color_three)        
        self.purchase_rec_btn = tk.Button(self.nav_button_frame, text = "Purchase", width = 10, font = ("Helvetica", 10, "bold"),
                                    bg = self.color_three)
        self.sales_rec_btn = tk.Button(self.nav_button_frame, text = "Sales", width = 10, font = ("Helvetica", 10, "bold"),
                                    bg = self.color_three)
        self.product_rec_btn = tk.Button(self.nav_button_frame, text = "Products", width = 10, font = ("Helvetica", 10, "bold"),
                                    bg = self.color_three)        
        self.login_rec_btn = tk.Button(self.nav_button_frame, text = "Shifts", width = 10, font = ("Helvetica", 10, "bold"),
                                    bg = self.color_three)
        
        self.logout_btn.grid(row = 0, column = 0, sticky = 'e')
        self.staff_rec_btn.grid(row = 0, column = 1, sticky = 'e')
        self.purchase_rec_btn.grid(row = 0, column = 2, sticky = 'e')  
        self.sales_rec_btn.grid(row = 0, column = 3, sticky = 'e')
        self.product_rec_btn.grid(row = 0, column = 4, sticky = 'e')
        self.login_rec_btn.grid(row = 0, column = 5, sticky = 'e')
        
        self.btnlist = (self.staff_rec_btn, self.purchase_rec_btn, self.sales_rec_btn,
                       self.product_rec_btn, self.login_rec_btn)
        
        self.show_frame(AdminPage)
        
        self.load_commands()
        
    def logout(self):
        from startpage import StartPage
        response = tk.messagebox.askyesno("", "Do you want to logout?")
        if response:
            self.parent.switchframe(StartPage)
            
    def show_frame(self, shown_frame_class):
        new_entry_frame = shown_frame_class(self, self)
        if self.shown_frame is not None:
            self.shown_frame.destroy()
        self.shown_frame = new_entry_frame
        self.shown_frame.configure(border = 5, relief = 'sunken')
        self.shown_frame.grid(row=1, sticky = 'nswe')
        
    def load_commands(self):
        self.staff_rec_btn.config(command = self.shown_frame.show_staff_frame)
        self.purchase_rec_btn.config(command = self.shown_frame.show_purchase_frame)
        self.sales_rec_btn.config(command = self.shown_frame.show_sales_frame)
        self.product_rec_btn.config(command = self.shown_frame.show_product_frame)
        self.login_rec_btn.config(command = self.shown_frame.show_login_frame)


