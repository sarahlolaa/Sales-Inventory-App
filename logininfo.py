try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

from scrollframe import ScrollableFrame
from queryexec import queryExecution

class LoginInformation(tk.Frame):
    def __init__(self, parent, container):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.container = container


        self.database_sheet = ScrollableFrame(self.parent)
        self.database_sheet.configure(bd = 1, relief = "raised") 
        
        self.dataframe = self.database_sheet.canvas_frame

        self.retrieve_records()

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

    def delete_selection(self):
        """The login information does not allow the manual deletion of records."""

    def cancel_selection(self):
        """The login information does not allow the manual selection of records."""

    def retrieve_records(self):
        query = """SELECT shifts.shift_id
                ,employees.first_name
                ,employees.last_name
                ,employees.email
                ,shifts.timestamp
                FROM shifts INNER JOIN employees
                ON shifts.employee_id = employees.employee_id"""

        self.connect_data = queryExecution().create_connection() 
        self.stored_rec = queryExecution().execute_query(self.connect_data, query)

    def insert_record(self):
        """The login information page does not allow the manual insertion of records."""