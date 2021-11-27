try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

from scrollframe import ScrollableFrame
from queryexec import queryExecution


class StaffInformation(tk.Frame):
    def __init__(self, parent, container):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.container = container
        self.stored_rec = None
        self.connect_data = None
        self.last_widget = None
    
        
        self.staffid_entry = tk.Entry(self, width = 30, borderwidth = 2, state = "readonly")
        self.firstname_entry = tk.Entry(self, width = 30, borderwidth = 2, state = "readonly")
        self.lastname_entry = tk.Entry(self, width = 30, borderwidth = 2, state = "readonly")
        self.email_entry = tk.Entry(self, width = 30, borderwidth = 2, state = "readonly")
        self.date_entry = tk.Entry(self, width = 30, borderwidth = 2, state = "readonly")
        
        self.staffid_entry.grid(row = 0, column = 1)
        self.firstname_entry.grid(row = 1, column = 1)
        self.lastname_entry.grid(row = 2, column = 1)
        self.email_entry.grid(row = 0, column = 3, padx = (0, 25))
        self.date_entry.grid(row = 1, column = 3, padx = (0, 25))
        
        
        self.staffid_lbl = tk.Label(self, text = "Employee Id:", font = ("Helvetica", 10, "bold"))
        self.firstname_lbl = tk.Label(self, text = "First Name:", font = ("Helvetica", 10, "bold"))
        self.lastname_lbl = tk.Label(self, text = "Last Name:", font = ("Helvetica", 10, "bold"))
        self.email_lbl = tk.Label(self, text = "Email:", font = ("Helvetica", 10, "bold"))
        self.date_lbl = tk.Label(self, text = "Reg Date:", font = ("Helvetica", 10, "bold"))
        
        self.staffid_lbl.grid(row = 0, column = 0, padx = (25, 10), pady = 10, sticky = 'e')
        self.firstname_lbl.grid(row = 1, column = 0, padx = (25, 10), pady = 10, sticky = 'e')
        self.lastname_lbl.grid(row = 2, column = 0, padx = (25, 10), pady = 10, sticky = 'e')
        self.email_lbl.grid(row = 0, column = 2, padx = (25, 10), pady = 10, sticky = 'e')
        self.date_lbl.grid(row = 1, column = 2, padx = (25, 10), pady = 10, sticky = 'e')

        self.entry_list = [self.staffid_entry, self.firstname_entry, self.lastname_entry, self.email_entry,
                            self.date_entry]

        self.database_sheet = ScrollableFrame(self.parent)
        self.database_sheet.configure(bd = 1, relief = "raised") 
        
        self.dataframe = self.database_sheet.canvas_frame

        self.retrieve_records()

    def load_record_info(self):
        self.row_no = len(self.stored_rec)
        self.column_no = len(self.stored_rec[0])

        for i in range(self.row_no):
            if (i == 0):
                a = tk.Label(self.dataframe, width = 4, height = 2, bg = "gray86", 
                            bd = 0.5, relief = "solid")
                a.grid(row = i, column = 0)

                for j in range(self.column_no):
                    if (j == 0):
                        e = tk.Label(self.dataframe, width = 8, height = 2, bg = "gray86", 
                                    text = self.stored_rec[i][j], bd = 0.5, relief = "solid",
                                    anchor = "w")
                    else:
                        e = tk.Label(self.dataframe, width = 25, height = 2, text = self.stored_rec[i][j], 
                                    bg="gray86", bd = 0.5, relief= "solid",
                                    anchor = "w")
                    e.grid(row=i, column=(j+1), ipadx = 5, sticky = "e")
            else:
                a = tk.Label(self.dataframe, width = 4, height = 2, 
                bg = "gray86", bd = 0.5, relief = "solid")
                a.grid(row=i, column = 0)
                a.bind('<Button-1>', lambda event, row = i: self.highlight(event, row))

                for j in range(self.column_no):
                    if (j == 0):
                        e = tk.Label(self.dataframe, width = 8, height = 2, 
                                    text = self.stored_rec[i][j], bd = 0.5, relief = "solid",
                                    anchor = "w")
                    else:
                        e = tk.Label(self.dataframe, width = 25, height = 2, text = self.stored_rec[i][j], 
                                    bd = 0.5, relief= "solid",
                                    anchor = "w")
                    e.grid(row=i, column=(j+1), ipadx = 5, sticky = "e")

        queryExecution().close_query(self.connect_data)

        self.database_sheet.grid(row = 3, sticky = "nsew")

    
    def highlight(self, event, row_number):
        if self.last_widget is not None:
            self.last_widget.config(bg="gray86")
        event.widget.config(bg="thistle3")
        self.last_widget = event.widget
        
        selected_record = self.stored_rec[row_number]

        for entry in range(5):
            self.entry_list[entry].config(state = "normal")
            self.entry_list[entry].delete(0, tk.END)
            self.entry_list[entry].insert(tk.END, selected_record[entry])
            self.entry_list[entry].config(state = "disabled")


    def insert_record(self):
        """The staff information page does not allow the manual insertion of records."""
    

    def delete_selection(self):
        confirm_delete = tk.messagebox.showwarning("STAFFS", "Deleting this staff record will also delete \nall his/her log in information.")

        if confirm_delete:
            del_query = "DELETE from employees WHERE employee_id = " + self.staffid_entry.get()

            connect_data = queryExecution().create_connection() 
            self.stored_rec = queryExecution().execute_query_delete(connect_data, del_query)
            queryExecution().close_query(connect_data)
            self.cancel_selection()

            self.dataframe.destroy()
            self.database_sheet = ScrollableFrame(self.parent)
            self.database_sheet.configure(bd = 1, relief = "raised") 
            self.dataframe = self.database_sheet.canvas_frame

            self.retrieve_records()

    def cancel_selection(self):
        if self.last_widget is not None:
            self.last_widget.config(bg="gray86")
            self.last_widget = None  

        for entry in range(5):
            self.entry_list[entry].config(state = "normal")
            self.entry_list[entry].delete(0, tk.END)
            self.entry_list[entry].config(state = "disabled")    
            

    def retrieve_records(self):
        query = """SELECT employee_id
                ,first_name
                ,last_name
                ,email
                ,timestamp
                FROM employees"""
        self.connect_data = queryExecution().create_connection() 
        self.stored_rec = queryExecution().execute_query(self.connect_data, query)

        self.load_record_info()
