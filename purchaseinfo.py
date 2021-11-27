try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    import Tkinter as tk
    from Tkinter import messagebox

from scrollframe import ScrollableFrame
from queryexec import queryExecution

class PurchaseInformation(tk.Frame):
    def __init__(self, parent, container):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.container = container
        self.info_label = None
        self.last_widget = None

        
        self.purchaseid_entry = tk.Entry(self, width = 30, borderwidth = 2, state = "disabled")
        self.productname_entry = tk.Entry(self, width = 30, borderwidth = 2)
        self.category_entry = tk.Entry(self, width = 30, borderwidth = 2)
        self.purc_quantity_entry = tk.Entry(self, width = 30, borderwidth = 2)
        self.purcdate_entry = tk.Entry(self, width = 30, borderwidth = 2, state = "disabled")
        
        self.purchaseid_entry.grid(row = 0, column = 1)
        self.productname_entry.grid(row = 1, column = 1)
        self.category_entry.grid(row = 2, column = 1)
        self.purc_quantity_entry.grid(row = 0, column = 3, padx = (0, 25))
        self.purcdate_entry.grid(row = 1, column = 3, padx = (0, 25))
        
        self.purchaseid_lbl = tk.Label(self, text = "Product Id:", font = ("Helvetica", 10, "bold"))
        self.productname_lbl = tk.Label(self, text = "Product Name:", font = ("Helvetica", 10, "bold"))
        self.category_lbl = tk.Label(self, text = "Product Category:", font = ("Helvetica", 10, "bold"))
        self.purc_quantity_lbl = tk.Label(self, text = "Quantity Purchased:", font = ("Helvetica", 10, "bold"))
        self.purcdate_lbl = tk.Label(self, text = "Date Purchased:", font = ("Helvetica", 10, "bold"))
        
        self.purchaseid_lbl.grid(row = 0, column = 0, padx = (25, 10), pady = 10, sticky = 'w')
        self.productname_lbl.grid(row = 1, column = 0, padx = (25, 10), pady = 10, sticky = 'w')
        self.category_lbl.grid(row = 2, column = 0, padx = (25, 10), pady = 10, sticky = 'w')
        self.purc_quantity_lbl.grid(row = 0, column = 2, padx = (25, 10), pady = 10, sticky = 'w')
        self.purcdate_lbl.grid(row = 1, column = 2, padx = (25, 10), pady = 10, sticky = 'w')


        self.entry_list = [self.purchaseid_entry, self.productname_entry, self.category_entry, 
                            self.purc_quantity_entry, self.purcdate_entry]

        self.entry_list_normal = [self.productname_entry, self.category_entry, self.purc_quantity_entry]

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

        for entry in range(4):
            self.entry_list[entry].config(state = "normal")
            self.entry_list[entry].delete(0, tk.END)
            self.entry_list[entry].insert(tk.END, selected_record[entry])
            self.entry_list[entry].config(state = "disabled")


    def clear_selection(self):
        if self.info_label:
            self.info_label.grid_remove()

        for entry in range(3):
            self.entry_list_normal[entry].delete(0, tk.END)

        self.entry_list_normal[0].focus()


    def insert_record(self):
        prod_name = self.productname_entry.get()
        prod_category = self.category_entry.get()
        prod_quantity = self.purc_quantity_entry.get()

        if (prod_name == '') or (prod_category == '') or (prod_quantity == ''):
            messagebox.showerror("INPUT ERROR", "Fill all the available fields")
        
        else:
            check_product_name = """SELECT product_id, product_name
                                FROM products
                                WHERE product_name = ?"""

            input_product = (prod_name,)

            connect_data = queryExecution().create_connection()
            check_inputted_product = queryExecution().execute_query_norownames(connect_data, check_product_name, input_product)
            queryExecution().close_query(connect_data)

        
            if (check_inputted_product):
                connect_data = queryExecution().create_connection()
                insert_purchase_query = """INSERT INTO 'purchases' (quantity, product_id, employee_id)
                            VALUES(?, ?, ?);"""
                new_purchase = (prod_quantity, check_inputted_product[0][0], self.parent.employee_logged_in)

                queryExecution().insert_query(connect_data, insert_purchase_query, new_purchase)
                queryExecution().close_query(connect_data)

                self.clear_selection()
                self.retrieve_records()

            
            elif (not check_inputted_product):
                insert_product_query = """INSERT INTO 'products' (product_name, product_category)
                            VALUES(?, ?)"""

                new_product = (prod_name, prod_category)

                connect_data = queryExecution().create_connection()

                queryExecution().insert_query(connect_data, insert_product_query, new_product)

                queryExecution().close_query(connect_data)


                connect_data = queryExecution().create_connection()

                check_product_id = """SELECT product_id FROM products
                                WHERE product_name = ?"""

                product_id = queryExecution().execute_query_norownames(connect_data, check_product_id,
                                                        input_product)

                insert_purchase_query = """INSERT INTO 'purchases' (quantity, product_id, employee_id)
                            VALUES(?, ?, ?);"""
                
                new_purchase = (prod_quantity, product_id[0][0], self.parent.employee_logged_in)
                
                queryExecution().insert_query(connect_data, insert_purchase_query, new_purchase)
                queryExecution().close_query(connect_data)

                self.clear_selection()
                self.retrieve_records()

            else:
                messagebox.showerror("INPUT ERROR", "Enter the correct category value for the \
                                                    product name entered.")



    def delete_selection(self):
        confirm_delete = tk.messagebox.askyesno("PURCHASES", "Do you want to delete this record?")

        if confirm_delete:
            del_query = "DELETE from purchases WHERE purchase_id = " + self.purchaseid_entry.get()

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

        for entry in range(3):
            self.entry_list_normal[entry].config(state = "normal")

        self.entry_list_normal[0].focus()


    def retrieve_records(self):
        query = """SELECT purchases.purchase_id
                ,products.product_name
                ,products.product_category
                ,purchases.quantity
                ,employees.first_name || ' ' || employees.last_name AS "staff_name"
                ,purchases.timestamp
                FROM ((purchases INNER JOIN products
                ON purchases.product_id = products.product_id)
                LEFT JOIN employees ON purchases.employee_id = employees.employee_id)
                """
        self.connect_data = queryExecution().create_connection()
        self.stored_rec = queryExecution().execute_query(self.connect_data, query)
      
        if (len(self.stored_rec) == 0):
            self.info_label = tk.Label(self.dataframe, text = "No Records Available.")
            self.info_label.grid()

            self.database_sheet.grid(row = 3, sticky = "nsew")
        else:
            self.load_record_info()

        