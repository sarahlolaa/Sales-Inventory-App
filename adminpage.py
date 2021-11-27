try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk


from staffinfo import StaffInformation
from purchaseinfo import PurchaseInformation
from productinfo import ProductInformation
from salesinfo import SalesInformation
from logininfo import LoginInformation

class AdminPage(tk.Frame):
    def __init__(self, parent, container):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.container = container
        self.color_one = "gray80"
        
        self.current_btn = None
        self.record_frame = None
        self.canvas_frame = None
        self.employee_logged_in = self.parent.employee_logged_in

        
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(3, weight = 1)
        
        
        self.title_lbl = tk.Label(self, font = ("Helvetica", 13, "bold"))
        self.title_lbl.grid(row = 0, sticky = 'ew')
        
        self.operations_frame = tk.Frame(self)
        self.operations_frame.grid(row = 1, sticky = "w")
        
        self.add_button = tk.Button(self.operations_frame, text = "+", width = 4, bg = self.color_one, font = ("Helvetica", 10, "bold"))
        self.remove_button = tk.Button(self.operations_frame, text = "-", width = 4, bg = self.color_one, font = ("Helvetica", 10, "bold"))
        self.cancel_button = tk.Button(self.operations_frame, text = "x", width = 4, bg = self.color_one, font = ("Helvetica", 10, "bold"))
        
        self.add_button.grid(row = 0, column = 0)
        self.remove_button.grid(row = 0, column = 1, padx = (0, 30))
        self.cancel_button.grid(row = 0, column = 2)

        
        self.show_staff_frame()

        
    def switch_content_frame(self, record_frame_class):
        new_entry_frame = record_frame_class(self, self.parent)
        if self.record_frame is not None:
            self.record_frame.destroy()
        self.record_frame = new_entry_frame
        self.record_frame.grid(row=2, sticky = 'ew')

    def load_commands(self):
        self.add_button.config(command = self.record_frame.insert_record)
        self.remove_button.config(command = self.record_frame.delete_selection)
        self.cancel_button.config(command = self.record_frame.cancel_selection)
        
    def disable_btn(self):
        if self.last_btn_click != self.current_btn:
            self.last_btn_click.config(state = "disabled")
            if self.current_btn != None:
                self.current_btn.config(state = "normal")
            self.current_btn = self.last_btn_click
        
    def show_staff_frame(self): 
        self.last_btn_click = self.parent.btnlist[0]
        self.disable_btn()
        self.title_lbl.config(text = "STAFF INFORMATION")
        self.switch_content_frame(StaffInformation) 
        self.load_commands()

    def show_purchase_frame(self):
        self.last_btn_click = self.parent.btnlist[1]
        self.disable_btn()
        self.title_lbl.config(text = "PURCHASE INFORMATION")
        self.switch_content_frame(PurchaseInformation)
        self.load_commands()
        
    def show_sales_frame(self):
        self.last_btn_click = self.parent.btnlist[2]
        self.disable_btn()
        self.title_lbl.config(text = "SALES INFORMATION")
        self.switch_content_frame(SalesInformation)
        self.load_commands()
    
    def show_product_frame(self):
        self.last_btn_click = self.parent.btnlist[3]
        self.disable_btn()
        self.title_lbl.config(text = "PRODUCT INFORMATION")
        self.switch_content_frame(ProductInformation)
        self.load_commands()
        
    def show_login_frame(self):
        self.last_btn_click = self.parent.btnlist[4]
        self.disable_btn()
        self.title_lbl.config(text = "STAFF LOG INFORMATION")
        self.switch_content_frame(LoginInformation)
        self.load_commands()