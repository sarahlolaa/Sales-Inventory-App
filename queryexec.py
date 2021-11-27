try:
    from tkinter import messagebox
except ImportError:
    from Tkinter import messagebox


import sqlite3
from sqlite3 import Error


class queryExecution():
    def create_connection(self, path = "SalesIR.db"):
        data_connect = None
        try:
            data_connect = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES |
                                                                sqlite3.PARSE_COLNAMES)        
        except Error as e:
            messagebox.showerror("CONNECTION ERROR", "An error occurred while connecting. Try again")
            print(f"Error {e} occurred")
        return data_connect

    def insert_query (self, connection, query, values):
        cursor = connection.cursor()
        try:
            cursor.execute(query, values)
            connection.commit()
        except sqlite3.IntegrityError as e:
            messagebox.showerror("INPUT ERROR", f"{str(e)[36:].capitalize()} already exists.")
            return "do_not_submit"


    def execute_query(self, connection, query):
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        try: 
            records = cursor.execute(query)
            records = cursor.fetchall()
            record_store = []

            if records:
                row_names = records[0].keys()
                record_store.append(row_names)

            for row in records:
                record_store.append(list(row))
            return record_store

            
        except Error as e:
            print(f"Error {e} occurred")

    def execute_query_norownames(self, connection, query, value = None):
        cursor = connection.cursor()
        try: 
            if (value is None):
                records = cursor.execute(query)
            else:
                records = cursor.execute(query, value)
            records = cursor.fetchall()
        except Error as e:
            messagebox.showerror("QUERY ERROR", "An error occurred while executing query. Try again.")
            print(f"Error {e} occurred")
        return records 

    def execute_query_delete(self, connection, query):
        cursor = connection.cursor()
        try: 
            cursor.execute(query)
            connection.commit()
        except Error as e:
            messagebox.showerror("DELETE ERROR", "An error occurred while executing query. Try again.")
            print(f"Error {e} occurred")

    def close_query(self, connection):
        connection.close()

