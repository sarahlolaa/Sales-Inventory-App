try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    from Tkinter import ttk

from tkinter.constants import INSERT
from scrollframe import ScrollableFrame
from queryexec import queryExecution

class SalesInformation(tk.Frame):
    def __init__(self, parent, container):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.container = container
        self.info_label = None
        self.last_widget = None
        
        
        self.salesid_entry = tk.Entry(self, width = 30, borderwidth = 2, state = "disabled")
        
        self.productname_entry = ttk.Combobox(self, values = self.load_product_name(), width = 27, 
                                    state = "readonly")
        
        self.productname_entry.current(0)

        self.category_entry = tk.Entry(self, width = 30, borderwidth = 2, state = "disabled")
        self.quantity_sold_entry = tk.Entry(self, width = 30, borderwidth = 2)
        self.date_entry = tk.Entry(self, width = 30, borderwidth = 2, state = "disabled")
        
        self.salesid_entry.grid(row = 0, column = 1)
        self.productname_entry.grid(row = 1, column = 1)
        self.category_entry.grid(row = 2, column = 1)
        self.quantity_sold_entry.grid(row = 0, column = 3, padx = (0, 25))
        self.date_entry.grid(row = 1, column = 3, padx = (0, 25))
        
        
        self.salesid_lbl = tk.Label(self, text = "Product Id:", font = ("Helvetica", 10, "bold"))
        self.productname_lbl = tk.Label(self, text = "Product Name:", font = ("Helvetica", 10, "bold"))
        self.category_lbl = tk.Label(self, text = "Product Category:", font = ("Helvetica", 10, "bold"))
        self.quantity_sold_lbl = tk.Label(self, text = "Quantity Sold:", font = ("Helvetica", 10, "bold"))
        self.date_lbl = tk.Label(self, text = "Date Sold:", font = ("Helvetica", 10, "bold"))
        
        self.salesid_lbl.grid(row = 0, column = 0, padx = (25, 10), pady = 10, sticky = 'w')
        self.productname_lbl.grid(row = 1, column = 0, padx = (25, 10), pady = 10, sticky = 'w')
        self.category_lbl.grid(row = 2, column = 0, padx = (25, 10), pady = 10, sticky = 'w')
        self.quantity_sold_lbl.grid(row = 0, column = 2, padx = (25, 10), pady = 10, sticky = 'w')
        self.date_lbl.grid(row = 1, column = 2, padx = (25, 10), pady = 10, sticky = 'w')

        self.entry_list = [self.salesid_entry, self.productname_entry, self.category_entry, 
                            self.quantity_sold_entry, self.date_entry]

        self.entry_list_normal = [self.productname_entry, self.quantity_sold_entry]

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

        for entry in range(2):
            self.entry_list_normal[entry].delete(0, tk.END)


    def insert_record(self):
        prod_name = self.productname_entry.get()
        prod_quantity = self.quantity_sold_entry.get()

        if (prod_name == '') or (prod_quantity == ''):
            tk.messagebox.showerror("INPUT ERROR", "Fill all the available fields")
        
        else:
            self.calc_products()

            for products in self.stored_products:
                if prod_name in products:
                    if products[2] > int(prod_quantity):
                        insert_sales_query = """INSERT INTO 'sales' (product_id, quantity, employee_id)
                            VALUES(?, ?, ?);"""
                
                        new_sale = (products[0], prod_quantity, self.parent.employee_logged_in)

                        connect_data = queryExecution().create_connection()
                        queryExecution().insert_query(connect_data, insert_sales_query, new_sale)
                        queryExecution().close_query(connect_data)

                        self.clear_selection()
                        self.retrieve_records()

                    else:
                        tk.messagebox.showerror("INPUT ERROR", "The quantity you entered is greater \nthan the available quantity.")

    def calc_products(self):
        product_query = """SELECT pur_total.product_id,
                    prod.product_name,
                    total_quantity - COALESCE(sales_tot, 0) AS purchase_total
                    FROM (SELECT pur.product_id, SUM(pur.quantity) as total_quantity
                            FROM purchases pur
                            GROUP BY pur.product_id) pur_total
                    
                    LEFT JOIN (SELECT sal.product_id, SUM(sal.quantity) as sales_tot
                            FROM sales sal
                            GROUP BY sal.product_id) AS sal_total
                    ON  pur_total.product_id = sal_total.product_id

                    LEFT JOIN (SELECT products.product_id, products.product_name
                                FROM products) prod
                    ON  pur_total.product_id = prod.product_id """

        self.connect_data = queryExecution().create_connection() 
        self.stored_products = queryExecution().execute_query_norownames(self.connect_data, product_query)
        queryExecution().close_query(self.connect_data)

    
    def load_product_name(self):
        query = "SELECT product_name FROM products" 
        connect_data = queryExecution().create_connection()
        product_options = queryExecution().execute_query_norownames(connect_data, query)
        
        queryExecution().close_query(connect_data)

        if (len(product_options) == 0):  
            return ["No product available"]
        else:
            products_available = []
            for product in product_options:
                products_available.append(product[0])  
            return products_available


    def delete_selection(self):
        confirm_delete = tk.messagebox.askyesno("SALES", "Do you want to delete this record?")

        if confirm_delete:
            del_query = "DELETE from sales WHERE sales_id = " + self.salesid_entry.get()

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

        for entry in range(2):
            self.entry_list_normal[entry].config(state = "normal")


    def retrieve_records(self):
        query = """SELECT sales.sales_id
                ,products.product_name
                ,products.product_category
                ,sales.quantity
                ,employees.first_name || ' ' || employees.last_name AS "staff_name"
                ,sales.timestamp
                FROM ((sales INNER JOIN products
                ON sales.product_id = products.product_id)
                LEFT JOIN employees ON sales.employee_id = employees.employee_id)
                """
        self.connect_data = queryExecution().create_connection()
        self.stored_rec = queryExecution().execute_query(self.connect_data, query)
        
        if (len(self.stored_rec) == 0):
            self.info_label = tk.Label(self.dataframe, text = "No Records Available.")
            self.info_label.grid()

            self.database_sheet.grid(row = 3, sticky = "nsew")
        else:
            self.load_record_info()