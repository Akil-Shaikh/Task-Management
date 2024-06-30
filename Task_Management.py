import sqlite3
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from datetime import datetime 

conn=sqlite3.connect('Task_Management.db')
cur=conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS tasks 
            (id INTEGER PRIMARY KEY,
            name TEXT,
            due_date DATE,
            completion_date DATE,
            condition INTEGER
            )''')
conn.commit()

def get_details():
    try:
        tname=task_details_entry.get()
        tdate=due_date_entry.get()
        if tname and tdate:
            if val_date(tdate):
                add_details(tname,tdate)
                task_details_entry.delete(0,END)
                due_date_entry.delete(0,END)
        else:
            messagebox.showerror("Error","Enter both fields")
    except Exception as e:
        messagebox.showerror("Error",e)

def val_date(da):
    try:
        v_date=datetime.strptime(da,"%Y-%m-%d")
        c_date=datetime.now()
        if v_date<c_date:
            messagebox.showwarning("Error","Enter Upcomming Dates")
            due_date_entry.delete(0,END)
            return False
        return True
    except Exception as e:
        messagebox.showerror("Error",e)
        due_date_entry.delete(0,END)

def add_details(tname,d_date):
    try:
        cur.execute("INSERT INTO tasks(name,due_date,condition) VALUES(?,?,?)",(tname,d_date,0))
        conn.commit()
        messagebox.showinfo("Sucessful","Task Added Sucessfully")
        display_incomplete()
    except Exception as e:
        messagebox.showerror("Error",e)

def mark_complete(id):
    try:
        currrent_date=datetime.now().strftime('%Y-%m-%d')
        cur.execute("UPDATE tasks SET completion_date=?,condition=1 WHERE id=?",(currrent_date,id))
        conn.commit()
        display_incomplete()
        display_complete()
    except Exception as e:
        messagebox.showerror("Error",e)

def display_complete():
    for widget in task_complete_display.winfo_children():
        widget.destroy()
    task_complete_label=ttk.Label(task_complete_display,text=f"Completed Tasks",font='Courier 22 bold')
    task_complete_label.grid(column=0,row=0,padx=2,pady=10,columnspan=2)
    tasks=cur.execute("SELECT * FROM tasks WHERE condition=1")
    for task in tasks:
        id,tname,ddate,cdate=task[0],task[1],task[2],task[3]
        if cdate<ddate:
            task_complete_label=ttk.Label(task_complete_display,text=tname,font='Ariel 12 bold',foreground="GREEN")
            task_complete_date=ttk.Label(task_complete_display,text=cdate,font='Ariel 12 bold')
        else:
            late=(datetime.strptime(cdate,"%Y-%m-%d")-datetime.strptime(ddate,"%Y-%m-%d")).days
            task_complete_label=ttk.Label(task_complete_display,text=tname,font='Ariel 12 bold',foreground="RED")
            task_complete_date=ttk.Label(task_complete_display,text=f"({cdate}, Late :{late} Days)",font='Ariel 12 bold')
            
        task_complete_label.grid(column=0,row=id+1,pady=5)
        task_complete_date.grid(column=1,row=id+1,pady=5)

def display_incomplete():
    for widget in task_incomplete_display.winfo_children():
        widget.destroy()
    task_incomplete_label=ttk.Label(task_incomplete_display,text=f"Pending Tasks",font='Courier 22 bold')
    task_incomplete_label.grid(column=0,row=0,pady=10,padx=2,columnspan=3)
    tasks=cur.execute("SELECT * FROM tasks WHERE condition=0")
    for task in tasks:
        id,tname,ddate=task[0],task[1],task[2]
        task_incomplete_label=ttk.Label(task_incomplete_display,text=tname,font='Ariel 12 bold')
        task_incomplete_label.grid(column=0,row=id+1,pady=5)
        task_incomplete_label=ttk.Label(task_incomplete_display,text=f"({ddate})",font='Ariel 12 bold')
        task_incomplete_label.grid(column=1,row=id+1,pady=5)
        task_incomplete_button=ttk.Button(task_incomplete_display,text="Complete",command=lambda a=id:mark_complete(a))
        task_incomplete_button.grid(column=2,row=id+1)
root=Tk()
root.title("Task Management System")
root.geometry('800x700')
style = ttk.Style()
style.theme_use('classic')
main_frame=ttk.Frame(root)
main_frame.pack(fill="both")

task_details_frame=ttk.Frame(main_frame)
task_details_frame.pack()

task_details_label=ttk.Label(task_details_frame,text="Task Name : ",font='Courier 15 bold')
task_details_label.grid(column=0,row=0,padx=20,pady=20)
task_details_entry=ttk.Entry(task_details_frame,width=40,font="Sans-Serif 12 bold")
task_details_entry.grid(column=1,row=0)

due_date_label=ttk.Label(task_details_frame,text="Due Date (YYYY-MM-DD): ",font='Courier 15 bold')
due_date_label.grid(column=0,row=1)
due_date_entry=ttk.Entry(task_details_frame,width=40,font="Sans-Serif 12 bold")
due_date_entry.grid(column=1,row=1)

accept_button=ttk.Button(main_frame,text="Add Task",width=20,command=get_details)
accept_button.pack(pady=20)

task_display_frame=ttk.Frame(main_frame)
task_display_frame.pack()

task_incomplete_display=ttk.Frame(task_display_frame,padding=30)
task_incomplete_display.grid(column=0,row=0)
task_complete_display=ttk.Frame(task_display_frame,padding=30)
task_complete_display.grid(column=1,row=0)


display_complete()
display_incomplete()
root.mainloop()