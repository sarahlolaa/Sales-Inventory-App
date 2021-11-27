try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    import Tkinter as tk
    from Tkinter import messagebox

from queryexec import queryExecution
from pageone import PageOne

class UserLogIn(tk.Frame):
    def __init__(self, parent, container):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.container = container
        self.color_one = self.container.color_one
        self.configure(bg = self.color_one)        
        
        #Set the variables for entry fields and checkbutton.
        self.username = tk.StringVar()
        self.passcode = tk.StringVar()
        self.check = tk.IntVar()
    
             
        #Create text label for login page.
        self.frame_label = tk.Label(self, text = "LOGIN", font = ("Helvetica", 13, "bold"), bg = self.color_one)
                
        #Create entry boxes for name and password.
        self.name = tk.Entry(self, text = self.username, width = 35, borderwidth = 2)
        self.password = tk.Entry(self, text = self.passcode, width = 35, borderwidth = 2, show = "*")
        
        #Create checkbox to show or hide password.
        password_check = tk.Checkbutton(self, text = "Show Password", bg = self.color_one, variable = self.check,
                                       command = self.show_password)
        
        
        self.frame_label.grid(row = 0, column = 0, columnspan = 2, pady = 2)
        self.name.grid(row = 1, column = 1, pady = 2)
        self.password.grid(row = 2, column = 1, padx = 10, pady = 2)
        password_check.grid(row = 3, column = 0, columnspan = 2)
        
        #Create text labels for name and password entry boxes.
        self.name_lbl = tk.Label(self, text = "Username", font = ("Helvetica", 10, "bold"), bg = self.color_one)        
        self.password_lbl = tk.Label(self, text = "Password", font = ("Helvetica", 10, "bold"), bg = self.color_one)
        
        self.name_lbl.grid(row = 1, column = 0)
        self.password_lbl.grid(row = 2, column = 0)
        
        
    def show_password(self):
        """Displays or hides entered password depending on whether the 
        checkbutton state is one or zero."""
        check_var = self.check.get()
        pass_word = self.password.get()
        if check_var == 0:
            self.password.config(show = "*")
            self.passcode.set(pass_word)
            
        elif check_var == 1:
            self.password.config(show = "")
            self.passcode.set(pass_word)   
            
    def reset(self):
        """Resets both name and password entry fields to an empty state.
        Moves the cursor to the start of the name entry field."""
        self.username.set("")
        self.passcode.set("")
        self.name.focus()
        
    def login(self):
        """Validates both name and password entered into the entry fields.
        Displays a warning if only one field is completed or if either username 
        or password is invalid.
        Enables log in if user details are corrected entered."""
        user_name = self.name.get()
        pass_word = self.password.get()
        

        if user_name == "" or pass_word == "":
            tk.messagebox.showinfo("LOGIN PAGE", "Enter both username and password")
        
        else:
            connect_data = queryExecution().create_connection()

            count_employees = "SELECT COUNT(employee_id) FROM employees"

            stored_rec = queryExecution().execute_query(connect_data, count_employees)

            queryExecution().close_query(connect_data)          
            
            
            if (stored_rec[1][0] > 0):
                check_employees = """SELECT employee_id, email, 
                                    password FROM employees 
                                    WHERE email = ? and password = ?"""
                
                check_values = (user_name, pass_word)

                connect_data = queryExecution().create_connection()
                
                record = queryExecution().execute_query_norownames(connect_data, check_employees, check_values)
                
                queryExecution().close_query(connect_data)

                if len(record) == 1:
                    connect_data = queryExecution().create_connection()

                    insert_shift_record = "INSERT INTO 'shifts' (employee_id) VALUES(?);"
                    shift_record = (record[0][0],)
                    
                    queryExecution().insert_query(connect_data, insert_shift_record, shift_record)
                    queryExecution().close_query(connect_data)

                    self.name.delete(0, tk.END)
                    self.password.delete(0, tk.END)

                    PageOne.employee_logged_in = shift_record[0]
                    self.container.parent.switchframe(PageOne)
                    

                else:
                    tk.messagebox.showerror("LOGIN PAGE", "Invalid username or password")
            else:
                tk.messagebox.showerror("LOGIN PAGE", "Enter your registration details and try again")