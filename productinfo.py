try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

from scrollframe import ScrollableFrame
from queryexec import queryExecution
from tiptool import TipTool

class ProductInformation(tk.Frame):
    def __init__(self, parent, container):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.container = container
       
        self.info_label = None
        self.last_widget = None

        
        self.productid_entry = tk.Entry(self, width = 30, borderwidth = 2, state = "readonly")
        self.productname_entry = tk.Entry(self, width = 30, borderwidth = 2, state = "readonly")
        self.category_entry = tk.Entry(self, width = 30, borderwidth = 2, state = "readonly")
        self.min_stock_frame = tk.Frame(self, width = 30, borderwidth = 2)   
        self.min_stock_info_frame = tk.Frame(self)     
        
        self.productid_entry.grid(row = 0, column = 1)
        self.productname_entry.grid(row = 1, column = 1)
        self.category_entry.grid(row = 0, column = 3, padx = (0, 25))
        self.min_stock_frame.grid(row = 1, column = 3, sticky = "w")
        self.min_stock_info_frame.grid(row = 3, column = 3, sticky = "w")

        self.min_stock_entry = tk.Entry(self.min_stock_frame, width = 10, borderwidth = 2)
        self.min_stock_reg_btn = tk.Button(self.min_stock_frame, text = "+", width = 3, 
                                            command = self.insert_min_stock_amount)

        self.min_stock_entry.grid(row = 0, column = 0)
        self.min_stock_reg_btn.grid(row = 0, column = 1, padx = 10)
        
        self.productid_lbl = tk.Label(self, text = "Product Id:", font = ("Helvetica", 10, "bold"))
        self.productname_lbl = tk.Label(self, text = "Product Name:", font = ("Helvetica", 10, "bold"))
        self.category_lbl = tk.Label(self, text = "Product Category:", font = ("Helvetica", 10, "bold"))
        self.min_stock_lbl = tk.Label(self, text = "Mininum Stock:", font = ("Helvetica", 10, "bold")) 
        
        self.productid_lbl.grid(row = 0, column = 0, padx = (25, 10), pady = 10, sticky = 'w')
        self.productname_lbl.grid(row = 1, column = 0, padx = (25, 10), pady = 10, sticky = 'w')
        self.category_lbl.grid(row = 0, column = 2, padx = (25, 10), pady = 10, sticky = 'w')
        self.min_stock_lbl.grid(row = 1, column = 2, padx = (25, 10), pady = 10, sticky = 'w')

        self.min_stock_val_lbl = tk.Label(self.min_stock_info_frame, text = self.retrieve_min_stock_val(), 
                                        font = ("Helvetica", 10, "bold"))
        self.min_stock_info_lbl = tk.Label(self.min_stock_info_frame, text="?", font = ("Helvetica", 10, "bold"))
        
        self.min_stock_tip = TipTool(self.min_stock_info_lbl, self.container, \
                                            "This is the minimum value of stock allowed.  \
                                            If stock reaches this value, you will get a warning.  \
                                            This value can be changed in the entry box above.")

        self.min_stock_val_lbl.grid(row = 1, column = 0)
        self.min_stock_info_lbl.grid(row = 1, column = 1, ipadx= 5)

        self.entry_list = [self.productid_entry, self.productname_entry, self.category_entry]

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

        for entry in range(2):
            self.entry_list[entry].config(state = "normal")
            self.entry_list[entry].delete(0, tk.END)
            self.entry_list[entry].insert(tk.END, selected_record[entry])
            self.entry_list[entry].config(state = "disabled")


    def insert_min_stock_amount(self):
        min_stock_query = """UPDATE minstock 
                            SET min_stock_val = ?
                            WHERE oid = 1"""

        min_stock_val_entry = self.min_stock_entry.get()

        if (min_stock_val_entry.isdigit()):
            connect_data = queryExecution().create_connection() 
            queryExecution().insert_query(connect_data, min_stock_query, (min_stock_val_entry,))
            queryExecution().close_query(connect_data)

            self.min_stock_entry.delete(0, tk.END)
            self.min_stock_val_lbl.config(text = str(min_stock_val_entry))

            self.min_stock_val = [(int(min_stock_val_entry),)]

            self.calc_product_in_store()
        else:
            tk.messagebox.showerror("QUERY ERROR", "Invalid entry")


    def insert_record(self):
        """The product information page does not allow the manual insertion of records."""


    def delete_selection(self):
        confirm_delete = tk.messagebox.showwarning("PRODUCTS", "Deleting this product record will also \ndelete it's sale and purchase information.")

        if confirm_delete:
            del_query = "DELETE from products WHERE product_id = " + self.productid_entry.get()

            self.connect_data = queryExecution().create_connection() 
            self.stored_rec = queryExecution().execute_query_delete(self.connect_data, del_query)
            queryExecution().close_query(self.connect_data)
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

        for entry in range(2):
            self.entry_list[entry].config(state = "normal")
            self.entry_list[entry].delete(0, tk.END)
            self.entry_list[entry].config(state = "disabled")


    def calc_product_in_store(self):
        product_low = ""
        for i in range(1, self.product_rec_length):
            if self.stored_rec[i][3] <= self.min_stock_val[0][0]:
                product_low += "\n" + self.stored_rec[i][1]

        if len(product_low) > 0:
            tk.messagebox.showinfo("PRODUCT NOTIFICATION", f"The following products are low in supply: {product_low}")

    
    def retrieve_min_stock_val(self):
        stock_val_query = """SELECT min_stock_val
                            FROM minstock"""
        
        connect_data = queryExecution().create_connection() 
        self.min_stock_val = queryExecution().execute_query_norownames(connect_data, stock_val_query)
        queryExecution().close_query(connect_data)

        return self.min_stock_val[0][0]

    
    def retrieve_records(self):
        product_query = """SELECT pur_total.product_id
                    ,prod.product_name
                    ,product_category
                    ,total_quantity - COALESCE(sales_tot, 0) AS quantity_available
                    FROM (SELECT pur.product_id, SUM(pur.quantity) as total_quantity
                            FROM purchases pur
                            GROUP BY pur.product_id) pur_total
                    
                    LEFT JOIN (SELECT sal.product_id, SUM(sal.quantity) as sales_tot
                            FROM sales sal
                            GROUP BY sal.product_id) AS sal_total
                    ON  pur_total.product_id = sal_total.product_id

                    LEFT JOIN (SELECT products.product_id, products.product_name, products.product_category
                                FROM products) prod
                    ON  pur_total.product_id = prod.product_id """

        self.connect_data = queryExecution().create_connection() 
        self.stored_rec = queryExecution().execute_query(self.connect_data, product_query)

        self.product_rec_length = len(self.stored_rec)
  
        if (self.product_rec_length == 0):
            self.info_label = tk.Label(self.dataframe, text = "No Records Available.")
            self.info_label.grid()

            self.database_sheet.grid(row = 3, sticky = "nsew")
        else:
            self.load_record_info()
            self.calc_product_in_store()

            

   