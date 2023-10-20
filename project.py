import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview

# Создание таблицы сотрудников в базе данных
def create_table():
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS employees
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 name TEXT NOT NULL, 
                 phone TEXT NOT NULL, 
                 email TEXT NOT NULL, 
                 salary INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

# Добавление нового сотрудника
def add_employee():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    salary = salary_entry.get()
    
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute("INSERT INTO employees (name, phone, email, salary) VALUES (?, ?, ?, ?)",
              (name, phone, email, salary))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Добавление сотрудника", "Сотрудник успешно добавлен.")
    
    clear_entries()
    load_employees()

# Изменение существующего сотрудника
def update_employee():
    selected_item = employees_treeview.selection()
    
    if not selected_item:
        messagebox.showwarning("Ошибка", "Выберите сотрудника для изменения.")
        return
    
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    salary = salary_entry.get()
    
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    employee_id = employees_treeview.item(selected_item)['values'][0]
    c.execute("UPDATE employees SET name=?, phone=?, email=?, salary=? WHERE id=?",
              (name, phone, email, salary, employee_id))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Изменение сотрудника", "Сотрудник успешно изменен.")
    
    clear_entries()
    load_employees()

# Удаление сотрудника
def delete_employee():
    selected_item = employees_treeview.selection()
    
    if not selected_item:
        messagebox.showwarning("Ошибка", "Выберите сотрудника для удаления.")
        return
    
    if messagebox.askyesno("Удаление сотрудника", "Вы уверены, что хотите удалить выбранного сотрудника?"):
        conn = sqlite3.connect('employees.db')
        c = conn.cursor()
        employee_id = employees_treeview.item(selected_item)['values'][0]
        c.execute("DELETE FROM employees WHERE id=?", (employee_id,))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Удаление сотрудника", "Сотрудник успешно удален.")
        
        clear_entries()
        load_employees()

# Поиск сотрудника по ФИО
def search_employee():
    search_name = search_entry.get()
    
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute("SELECT * FROM employees WHERE name LIKE ?", ('%'+search_name+'%',))
    employees = c.fetchall()
    conn.close()
    
    employees_treeview.delete(*employees_treeview.get_children())
    
    for employee in employees:
        employees_treeview.insert('', 'end', values=employee)

# Загрузка сотрудников из базы данных
def load_employees():
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute("SELECT * FROM employees")
    employees = c.fetchall()
    conn.close()
    
    employees_treeview.delete(*employees_treeview.get_children())
    
    for employee in employees:
        employees_treeview.insert('', 'end', values=employee)

# Очистка полей ввода
def clear_entries():
    name_entry.delete(0, 'end')
    phone_entry.delete(0, 'end')
    email_entry.delete(0, 'end')
    salary_entry.delete(0, 'end')
    search_entry.delete(0, 'end')

# Создание графического интерфейса
root = Tk()
root.title("Список сотрудников компании")

# Фрейм для записей сотрудников
employees_frame = Frame(root)
employees_frame.pack(pady=10)

# Виджет Treeview для вывода сотрудников
employees_treeview = Treeview(employees_frame, columns=(1, 2, 3, 4, 5), show="headings", height=10)
employees_treeview.pack(side="left")

scrollbar = Scrollbar(employees_frame, orient="vertical")
scrollbar.configure(command=employees_treeview.yview)
scrollbar.pack(side="right", fill="y")

employees_treeview.configure(yscrollcommand=scrollbar.set)
employees_treeview.heading(1, text="ID")
employees_treeview.heading(2, text="ФИО")
employees_treeview.heading(3, text="Телефон")
employees_treeview.heading(4, text="Email")
employees_treeview.heading(5, text="Зарплатная плата")

# Фрейм для кнопок и полей ввода
inputs_frame = Frame(root)
inputs_frame.pack(pady=10)

name_label = Label(inputs_frame, text="ФИО:")
name_label.grid(row=0, column=0, pady=5)
name_entry = Entry(inputs_frame)
name_entry.grid(row=0, column=1, pady=5)

phone_label = Label(inputs_frame, text="Телефон:")
phone_label.grid(row=1, column=0, pady=5)
phone_entry = Entry(inputs_frame)
phone_entry.grid(row=1, column=1, pady=5)

email_label = Label(inputs_frame, text="Email:")
email_label.grid(row=2, column=0, pady=5)
email_entry = Entry(inputs_frame)
email_entry.grid(row=2, column=1, pady=5)

salary_label = Label(inputs_frame, text="Заработная плата:")
salary_label.grid(row=3, column=0, pady=5)
salary_entry = Entry(inputs_frame)
salary_entry.grid(row=3, column=1, pady=5)

# Кнопки
add_button = Button(inputs_frame, text="Добавить", command=add_employee)
add_button.grid(row=0, column=2, padx=10)

update_button = Button(inputs_frame, text="Изменить", command=update_employee)
update_button.grid(row=1, column=2, padx=10)

delete_button = Button(inputs_frame, text="Удалить", command=delete_employee)
delete_button.grid(row=2, column=2, padx=10)

search_label = Label(inputs_frame, text="Поиск по ФИО:")
search_label.grid(row=3, column=2, pady=5)
search_entry = Entry(inputs_frame)
search_entry.grid(row=4, column=2, pady=5)

search_button = Button(inputs_frame, text="Найти", command=search_employee)
search_button.grid(row=4, column=1, padx=10)

clear_button = Button(inputs_frame, text="Очистить", command=clear_entries)
clear_button.grid(row=4, column=0, padx=10)

# Создание таблицы и загрузка сотрудников
create_table()
load_employees()

root.mainloop()

