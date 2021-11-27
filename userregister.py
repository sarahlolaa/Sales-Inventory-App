try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

from queryexec import queryExecution
import re
from tiptool import TipTool


class UserRegister(tk.Frame):
    def __init__(self, parent, container):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.container = container
        self.color_one = self.container.color_one
        self.configure(bg = self.color_one) 
             
        #Set the variables for entry fields and checkbutton.
        self.firstname = tk.StringVar()
        self.lastname = tk.StringVar()
        self.email = tk.StringVar()
        self.password_one = tk.StringVar()
        self.password_two = tk.StringVar()
        
        self.check = tk.IntVar()
    
             
        #Create text label for login page.
        self.frame_label = tk.Label(self, text = "REGISTER", font = ("Helvetica", 13, "bold"), bg = self.color_one)
                
        #Create entry boxes for name and password.
        self.first_name = tk.Entry(self, text = self.firstname, width = 30, borderwidth = 2)
        self.last_name = tk.Entry(self, text = self.lastname, width = 30, borderwidth = 2)
        self.email_addr = tk.Entry(self, text = self.email, width = 30, borderwidth = 2)
        self.passcode_one = tk.Entry(self, text = self.password_one, width = 30, borderwidth = 2, show = "*")
        self.passcode_two = tk.Entry(self, text = self.password_two, width = 30, borderwidth = 2, show = "*")
        
        #Create checkbox to show or hide password.
        password_check_one = tk.Checkbutton(self, text = "Show Password", bg = self.color_one, variable = self.check,
                                       command = self.show_password)
        
        
        self.frame_label.grid(row = 0, column = 0, columnspan = 2, pady = 2)
        self.first_name.grid(row = 1, column = 1, pady = 2)
        self.last_name.grid(row = 2, column = 1, pady = 2)
        self.email_addr.grid(row = 3, column = 1, pady = 2)
        self.passcode_one.grid(row = 4, column = 1, pady = 2)
        password_check_one.grid(row = 5, column = 1, columnspan = 2, pady = 2)
        self.passcode_two.grid(row = 6, column = 1, pady = (2, 8))
        
        #Create entry boxes for name and password.
        self.first_name_lbl = tk.Label(self, text = "First Name", font = ("Helvetica", 10, "bold"), bg = self.color_one)
        self.last_name_lbl = tk.Label(self, text = "Last Name", font = ("Helvetica", 10, "bold"), bg = self.color_one)
        self.email_addr_lbl = tk.Label(self, text = "Email", font = ("Helvetica", 10, "bold"), bg = self.color_one)
        self.passcode_one_lbl = tk.Label(self, text = "Enter Password", font = ("Helvetica", 10, "bold"), bg = self.color_one,
                                        )
        self.passcode_two_lbl = tk.Label(self, text = "Confirm Password", font = ("Helvetica", 10, "bold"), bg = self.color_one)
        
    
        self.first_name_lbl.grid(row = 1, column = 0, sticky = "w", ipadx= 5)
        self.last_name_lbl.grid(row = 2, column = 0, sticky = "w", ipadx= 5)
        self.email_addr_lbl.grid(row = 3, column = 0, sticky = "w", ipadx= 5)
        self.passcode_one_lbl.grid(row = 4, column = 0, sticky = "w", ipadx= 5)
        self.passcode_two_lbl.grid(row = 6, column = 0, ipadx= 5)
        
        #Create text tool.
        self.passcode_tip_lbl = tk.Label(self, text="?", font = ("Helvetica", 10, "bold"), bg = self.color_one)
        
        self.passcode_tip_lbl.grid(row = 4, column = 3, ipadx= 5)
        
        self.passcode_tip = TipTool(self.passcode_tip_lbl, self.container, \
                                            "- Your password must be at least eight characters long.\
                                            - Your password should contain only letters and numbers.\
                                            - No special characters are allowed.")

        
    def show_password(self):
        """Displays or hides entered password depending on whether the 
        checkbutton state is one or zero."""
        check_var = self.check.get()
        pass_word = self.passcode_one.get()
        if check_var == 0:
            self.passcode_one.config(show = "*")
            self.password_one.set(pass_word)

        elif check_var == 1:
            self.passcode_one.config(show = "")
            self.password_one.set(pass_word)  
        
    def reset(self):
        self.first_name.delete(0, tk.END)
        self.last_name.delete(0, tk.END)
        self.email_addr.delete(0, tk.END)
        self.passcode_one.delete(0, tk.END)
        self.passcode_two.delete(0, tk.END)
            
            
    #Create submit function
    def register(self):
        f_name = self.firstname.get()
        l_name = self.lastname.get()
        email = self.email.get()
        password_1 = self.password_one.get()
        password_2 = self.password_two.get()


        if (f_name == "") or (l_name == "") or (email == "") or (password_1 == "") or (password_2 == ""):
            tk.messagebox.showerror("REGISTRATION PAGE", "Fill all available fields")
        else:
            if re.search('^(.{0,7})$|\W+|^[a-zA-Z]*$|^[0-9]*$|_+|\s+', password_1):
                tk.messagebox.showinfo("REGISTRATION PAGE", ("Your password must be at least eight characters long.\n"
                                   "Your password should contain only letters and numbers.\n"
                                   "No special characters are allowed."))
            else:
                if (password_1 != password_2):
                    tk.messagebox.showerror("REGISTRATION PAGE", "Reconfirm your password")
                    
                else:

                    connect_data = queryExecution().create_connection() 

                    new_insert_employees = """INSERT INTO 'employees' 
                                            (first_name, last_name, password, email)
                                            VALUES(?, ?, ?, ?);"""

                    entry_values = (f_name, l_name, password_1, email)
                    
                    entered_rec = queryExecution().insert_query(connect_data, new_insert_employees, entry_values)

                    if (entered_rec is None):
                        queryExecution().close_query(connect_data)
                        
                        self.first_name.delete(0, tk.END)
                        self.last_name.delete(0, tk.END)
                        self.email_addr.delete(0, tk.END)
                        self.passcode_one.delete(0, tk.END)
                        self.passcode_two.delete(0, tk.END)
                        self.first_name.focus()

                        tk.messagebox.showinfo("REGISTRATION PAGE", "Registration Successful")

