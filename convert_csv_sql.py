import pandas as pd
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def csv_to_db(csv_file, db_name, table_name):
    try:
        # อ่านข้อมูลจากไฟล์ CSV ด้วย encoding แบบ utf-8
        df = pd.read_csv(csv_file, encoding='utf-8')

        # สร้างการเชื่อมต่อกับฐานข้อมูล SQLite
        conn = sqlite3.connect(db_name+'.db')
        
        # นำข้อมูลจาก DataFrame ไปใส่ในตารางของฐานข้อมูล
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        
        # ปิดการเชื่อมต่อ
        conn.close()
        filename = os.path.basename(csv_file)
        messagebox.showinfo("Convert Success", f"CSV name : {filename}\n!!!!Convert to File Name!!!!\nDatabase name : {db_name+'.db'} \nTable name : {table_name}")
    except FileNotFoundError:
        messagebox.showerror("Error", f"The file {filename} does not exist.")
    except UnicodeDecodeError as e:
        messagebox.showerror("Error", f"Error decoding file: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def browse_csv_file():
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filename:
        csv_file_entry.delete(0, tk.END)
        csv_file_entry.insert(0, filename)

def convert():
    csv_file = csv_file_entry.get()
    db_name = db_name_entry.get()
    table_name = table_name_entry.get()
    
    if not csv_file or not db_name or not table_name:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return
    
    csv_to_db(csv_file, db_name, table_name)

# สร้างหน้าต่างหลักของ tkinter
root = tk.Tk()
root.title("CSV to SQLite Converter")

# เพิ่ม Label และ Entry สำหรับการใส่ข้อมูลต่าง ๆ
tk.Label(root, text="CSV File:").grid(row=0, column=0, padx=10, pady=10)
csv_file_entry = tk.Entry(root, width=50)
csv_file_entry.grid(row=0, column=1, padx=10, pady=10)
browse_button = tk.Button(root, text="Browse", command=browse_csv_file)
browse_button.grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Database Name:").grid(row=1, column=0, padx=10, pady=10)
db_name_entry = tk.Entry(root, width=50)
db_name_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Table Name:").grid(row=2, column=0, padx=10, pady=10)
table_name_entry = tk.Entry(root, width=50)
table_name_entry.grid(row=2, column=1, padx=10, pady=10)

# เพิ่มปุ่ม Convert
convert_button = tk.Button(root, text="Convert", command=convert)
convert_button.grid(row=3, column=0, columnspan=3, pady=20)

# เริ่มต้น main loop ของ tkinter
root.mainloop()
