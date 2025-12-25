import tkinter as tk
from tkinter import messagebox,ttk
import sqlite3




def dbConnect():
    conn = sqlite3.connect('studentsRecords.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            roll_number INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            branch TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

class StudentRecordApp:
    def __init__(self,master):
        self.master=master
        self.master.title("Student Record Management")

        self.roll_var=tk.IntVar()
        self.name_var=tk.StringVar()
        self.branch_var=tk.StringVar()

        self.setup_input_fields(master)
        self.setup_buttons(master)
        self.setup_data_tree(master)

        self.load_data()    
    
    def setup_input_fields(self,master):
        input_frame=ttk.Frame(master,padding='10')
        input_frame.pack(padx=10,pady=10,fill='x')

        ttk.Label(input_frame,text="Roll Number:").grid(row=0,column=0,sticky='w',padx=5,pady=5)
        ttk.Entry(input_frame,textvariable=self.roll_var).grid(row=0,column=1,sticky='ew',padx=5,pady=5)

        ttk.Label(input_frame,text="Name:").grid(row=1,column=0,sticky='w',padx=5,pady=5)
        ttk.Entry(input_frame,textvariable=self.name_var).grid(row=1,column=1,sticky='ew',padx=5,pady=5)

        ttk.Label(input_frame,text="Branch:").grid(row=2,column=0,sticky='w',padx=5,pady=5)
        ttk.Entry(input_frame,textvariable=self.branch_var).grid(row=2,column=1,padx=5,pady=5)

    def setup_buttons(self,master):
        button_frame=ttk.Frame(master)
        button_frame.pack(padx=10,pady=(0),fill='x')

        ttk.Button(button_frame,text="Create",command=self.add_student).grid(row=0,column=0,padx=5,pady=5)
        ttk.Button(button_frame,text="Read",command=self.load_data).grid(row=0,column=1,padx=5,pady=5)
        ttk.Button(button_frame,text="Update",command=self.update_student_gui).grid(row=0,column=2,padx=5,pady=5)
        ttk.Button(button_frame,text="Delete",command=self.delete_student_gui).grid(row=0,column=3,padx=5,pady=5)
    
    def setup_data_tree(self,master):
        self.tree=ttk.Treeview(master,columns=('Roll Number', 'Name', 'Branch'), show='headings')
        self.tree.heading('Roll Number', text='Roll Number')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Branch', text='Branch')
        self.tree.pack(padx=10,pady=10,fill='both',expand=True)
    
    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        conn = sqlite3.connect('studentsRecords.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        for row in rows:
            self.tree.insert('',tk.END, values=row)
        conn.close()
    
    def add_student(self):
        roll = self.roll_var.get()
        name = self.name_var.get()
        branch = self.branch_var.get()

        if not (roll and name and branch):
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        conn = sqlite3.connect('studentsRecords.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO students (roll_number, name, branch) VALUES (?, ?, ?)", (roll, name, branch))
            conn.commit()
            messagebox.showinfo("Success", "Student record added successfully.")
            self.load_data()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Roll number already exists.")
        finally:
            conn.close()
    
    def update_student_gui(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a student record to update.")
            return
        
        roll = self.roll_var.get()
        name = self.name_var.get()
        branch = self.branch_var.get()

        if not (roll and name and branch):
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        conn = sqlite3.connect('studentsRecords.db')
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE students SET name=?, branch=? WHERE roll_number=?", (name, branch, roll))
            conn.commit()
            messagebox.showinfo("Success", "Student record updated successfully.")
            self.load_data()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Roll number already exists.")
        finally:
            conn.close()
    
    def delete_student_gui(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a student record to delete.")
            return
        
        roll = self.roll_var.get()

        conn = sqlite3.connect('studentsRecords.db')
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM students WHERE roll_number=?", (roll,))
            conn.commit()
            messagebox.showinfo("Success", "Student record deleted successfully.")
            self.load_data()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            conn.close()
    



if __name__ == "__main__":
    dbConnect()
    root=tk.Tk()
    app=StudentRecordApp(root)
    root.mainloop()