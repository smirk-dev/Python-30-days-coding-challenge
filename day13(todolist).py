import tkinter as tk
from tkinter import messagebox
def save_credentials(username, password):
    with open("credentials.txt", "a") as file:
        file.write(f"{username},{password}\n")
def validate_credentials(username, password):
    try:
        with open("credentials.txt", "r") as file:
            credentials = file.readlines()
            for cred in credentials:
                user, pwd = cred.strip().split(",")
                if user == username and pwd == password:
                    return True
        return False
    except FileNotFoundError:
        return False
def login():
    username = login_username.get()
    password = login_password.get()
    if validate_credentials(username, password):
        login_window.destroy()
        open_main_window()
    else:
        messagebox.showerror("Login Error", "Invalid Username or Password.")
def signup():
    username = login_username.get()
    password = login_password.get()
    if username and password:
        save_credentials(username, password)
        messagebox.showinfo("Signup Sucessful", "Account created successfully!")
    else:
        messagebox.showwarning("Input Error", "Please enter both username and password.")
def update_status_bar():
    total_tasks = listbox_tasks.size()
    completed_tasks = sum("[Completed]" in task for task in listbox_tasks.get(0, tk.END))
    status_var.set(f"Completed: {completed_tasks} / Total: {total_tasks}")
def add_task():
    task = entry_task.get()
    time = entry_time.get()
    category = entry_category.get()
    if task and time and category:
        listbox_tasks.insert(tk.END, f"{task} | {time} | {category}")
        entry_task.delete(0, tk.END)
        entry_time.delete(0, tk.END)
        entry_category.delete(0, tk.END)
        update_status_bar()
    else:
        messagebox.showwarning("Input Error", "All fields are required.")
def delete_task():
    try:
        selected_task = listbox_tasks.curselection()[0]
        listbox_tasks.delete(selected_task)
        update_status_bar()
    except IndexError:
        messagebox.showwarning("Selection Error", "Select a task to delete.")
def clear_all():
    listbox_tasks.delete(0, tk.END)
    update_status_bar()
def mark_completed():
    try:
        selected_task_index = listbox_tasks.curselection()[0]
        task = listbox_tasks.get(selected_task_index)
        listbox_tasks.delete(selected_task_index)
        listbox_tasks.insert(tk.END, f"{task} [Completed]")
        update_status_bar()
    except IndexError:
        messagebox.showwarning("Selection Error", "Select a task to mark as completed.")
def sort_tasks():
    tasks = list(listbox_tasks.get(0, tk.END))
    tasks.sort()
    listbox_tasks.delete(0, tk.END)
    for task in tasks:
        listbox_tasks.insert(tk.END, task)
def save_tasks():
    tasks = list(listbox_tasks.get(0, tk.END))
    with open("tasks.txt", "w") as file:
        for task in tasks:
            file.write(task + "\n")
    messagebox.showinfo("Save Successful", "Tasks saved to tasks.txt")
def open_main_window():
    root = tk.Tk()
    root.title("Enhanced To-Do List")
    root.geometry("500x600")
    root.resizable(False, False)
    header_frame = tk.Frame(root, bg="orange", height=50)
    header_frame.pack(fill=tk.X)
    header_label = tk.Label(header_frame, text="GOALS", bg="orange", fg="white", font=("Arial", 18, "bold"))
    header_label.pack(pady=10)
    task_list_frame = tk.Frame(root)
    task_list_frame.pack(pady=10)
    tasks_label = tk.Label(task_list_frame, text="TASKS", font=("Arial", 14, "bold"))
    tasks_label.pack()
    global listbox_tasks
    listbox_tasks = tk.Listbox(task_list_frame, width=60, height=10)
    listbox_tasks.pack()
    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)
    global entry_task, entry_time, entry_category
    entry_task = tk.Entry(input_frame, width=40, font=("Arial", 12))
    entry_task.grid(row=0, column=1, padx=5, pady=5)
    tk.Label(input_frame, text="Task Description").grid(row=0, column=0, padx=5, pady=5)
    entry_time = tk.Entry(input_frame, width=40, font=("Arial", 12))
    entry_time.grid(row=1, column=1, padx=5, pady=5)
    tk.Label(input_frame, text="Time (e.g., 12:00)").grid(row=1, column=0, padx=5, pady=5)
    entry_category = tk.Entry(input_frame, width=40, font=("Arial", 12))
    entry_category.grid(row=2, column=1, padx=5, pady=5)
    tk.Label(input_frame, text="Category").grid(row=2, column=0, padx=5, pady=5)
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    btn_add = tk.Button(button_frame, text="Add Task", bg="orange", fg="white", font=("Arial", 10), command=add_task)
    btn_add.grid(row=0, column=0, padx=5, pady=5)
    btn_delete = tk.Button(button_frame, text="Delete Task", bg="red", fg="white", font=("Arial", 10), command=delete_task)
    btn_delete.grid(row=0, column=1, padx=5, pady=5)
    btn_clear = tk.Button(button_frame, text="Clear All", bg="gray", fg="white", font=("Arial", 10), command=clear_all)
    btn_clear.grid(row=0, column=2, padx=5, pady=5)
    btn_mark = tk.Button(button_frame, text="Mark Completed", bg="green", fg="white", font=("Arial", 10), command=mark_completed)
    btn_mark.grid(row=0, column=3, padx=5, pady=5)
    btn_sort = tk.Button(button_frame, text="Sort Tasks", bg="yellow", font=("Arial", 10), command=sort_tasks)
    btn_sort.grid(row=1, column=0, columnspan=2, pady=5)
    btn_save = tk.Button(button_frame, text="Save Tasks", bg="blue", fg="white", font=("Arial", 10), command=save_tasks)
    btn_save.grid(row=1, column=2, columnspan=2, pady=5)
    global status_var
    status_var = tk.StringVar()
    status_var.set("Completed: 0 / Total: 0")
    status_bar = tk.Label(root, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    root.mainloop()
login_window = tk.Tk()
login_window.title("Login or Signup")
login_window.geometry("300x200")
login_window.resizable(False, False)
login_username = tk.Entry(login_window, width=30)
login_username.pack(pady=10)
login_username.insert(0, "Username")
login_password = tk.Entry(login_window, width=30, show="*")
login_password.pack(pady=10)
login_password.insert(0, "Password")
login_button = tk.Button(login_window, text="Login", command=login)
login_button.pack(pady=5)
signup_button = tk.Button(login_window, text="Signup", command=signup)
signup_button.pack(pady=5)
login_window.mainloop()