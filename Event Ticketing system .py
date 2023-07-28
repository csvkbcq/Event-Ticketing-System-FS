import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

root = Tk()
root.title("Event Ticketing System")
root.geometry("1080x720")
my_tree = ttk.Treeview(root)
storeName = "Event Ticketing System"

# Login Function
def login():
    # Retrieve the username and password from the entry fields
    username = entryUsername.get()
    password = entryPassword.get()

    # Check if the username and password are correct
    if username == "nithpraj" and password == "123123":
        messagebox.showinfo("Success", "Login successful")
        login_window.destroy()
        initialize_app()
    else:
        messagebox.showerror("Error", "Invalid credentials")

# Initialize App Function
def initialize_app():
    global entryId, entryName, entryPrice, entryQuantity, my_tree

    # Heading Label
    heading = Label(root, text=storeName, font=("Helvetica", 20, "bold"), pady=20)
    heading.pack()

    # Data Entry Frame
    data_frame = LabelFrame(root, text="Enter Ticket Details")
    data_frame.pack(fill="both", expand="yes", padx=20, pady=20)

    # Labels
    labelId = Label(data_frame, text="Cutsomer ID")
    labelId.grid(row=0, column=0, padx=10, pady=10)
    entryId = Entry(data_frame, width=30)
    entryId.grid(row=0, column=2, padx=10, pady=10)

    labelName = Label(data_frame, text="Product Name")
    labelName.grid(row=1, column=0, padx=10, pady=10)
    entryName = Entry(data_frame, width=30)
    entryName.grid(row=1, column=2, padx=10, pady=10)

    labelPrice = Label(data_frame, text="Price")
    labelPrice.grid(row=2, column=0, padx=10, pady=10)
    entryPrice = Entry(data_frame, width=30)
    entryPrice.grid(row=2, column=2, padx=10, pady=10)

    labelQuantity = Label(data_frame, text="Quantity")
    labelQuantity.grid(row=3, column=0, padx=10, pady=10)
    entryQuantity = Entry(data_frame, width=30)
    entryQuantity.grid(row=3, column=2, padx=10, pady=10)

    # Buttons
    insertBtn = Button(data_frame, text="Insert Ticket", command=insert_data)
    insertBtn.grid(row=5, column=0, padx=10, pady=10)
    deleteBtn = Button(data_frame, text="Delete Ticket", command=delete_data)
    deleteBtn.grid(row=5, column=1, padx=10, pady=10)
    updateBtn = Button(data_frame, text="Update Ticket", command=update_data)
    updateBtn.grid(row=5, column=2, padx=10, pady=10)

    # Treeview Frame
    tree_frame = Frame(root)
    tree_frame.pack(pady=20)

    # Treeview Scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # Treeview
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
    my_tree.pack()

    # Configure the Scrollbar
    tree_scroll.config(command=my_tree.yview)

    # Define Columns
    my_tree['columns'] = ("CustomerID", "ProductName", "Price", "Quantity")

    # Format Columns
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("CustomerID", anchor=W, width=140)
    my_tree.column("ProductName", anchor=W, width=140)
    my_tree.column("Price", anchor=W, width=140)
    my_tree.column("Quantity", anchor=W, width=140)

    # Create Headings
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("CustomerID", text="Customer ID", anchor=W)
    my_tree.heading("ProductName", text="Product Name", anchor=W)
    my_tree.heading("Price", text="Price", anchor=W)
    my_tree.heading("Quantity", text="Quantity", anchor=W)

    # Refresh Table Data
    refresh_table()

    root.mainloop()

# Database Functions
def reverse(tuples):
    new_tup = tuples[::-1]
    return new_tup

def insert(id, name, price, quantity):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS 
    inventory(itemId TEXT, itemName TEXT, itemPrice TEXT, itemQuantity TEXT)""")

    cursor.execute("INSERT INTO inventory VALUES ('" + str(id) + "','" + str(name) + "','" + str(price) + "','" + str(quantity) + "')")
    conn.commit()
    conn.close()

def delete(data):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS 
        inventory(itemId TEXT, itemName TEXT, itemPrice TEXT, itemQuantity TEXT)""")

    cursor.execute("DELETE FROM inventory WHERE itemId = '" + str(data) + "'")
    conn.commit()
    conn.close()

def update(id, name, price, quantity, idName):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS 
        inventory(itemId TEXT, itemName TEXT, itemPrice TEXT, itemQuantity TEXT)""")

    cursor.execute("UPDATE inventory SET itemId = '" + str(id) + "', itemName = '" + str(name) + "', itemPrice = '" + str(price) + "', itemQuantity = '" + str(quantity) + "' WHERE itemId='"+str(idName)+"'")
    conn.commit()
    conn.close()

def read():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS 
        inventory(itemId TEXT, itemName TEXT, itemPrice TEXT, itemQuantity TEXT)""")

    cursor.execute("SELECT * FROM inventory")
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results

def insert_data():
    itemId = str(entryId.get())
    itemName = str(entryName.get())
    itemPrice = str(entryPrice.get())
    itemQuantity = str(entryQuantity.get())

    if itemId == "" or itemName == "" or itemPrice == "" or itemQuantity == "":
        messagebox.showerror("Error", "Please fill in all fields")
        return

    insert(itemId, itemName, itemPrice, itemQuantity)

    entryId.delete(0, END)
    entryName.delete(0, END)
    entryPrice.delete(0, END)
    entryQuantity.delete(0, END)

    refresh_table()

    save_data()

    messagebox.showinfo("Success", "Ticket data inserted successfully")

def delete_data():
    selected_item = my_tree.selection()[0]
    deleteData = str(my_tree.item(selected_item)['values'][0])
    delete(deleteData)

    refresh_table()

    save_data()

    messagebox.showinfo("Success", "Ticket data deleted successfully")

def update_data():
    selected_item = my_tree.selection()[0]
    update_name = my_tree.item(selected_item)['values'][0]
    update(entryId.get(), entryName.get(), entryPrice.get(), entryQuantity.get(), update_name)

    entryId.delete(0, END)
    entryName.delete(0, END)
    entryPrice.delete(0, END)
    entryQuantity.delete(0, END)

    refresh_table()

    save_data()

    messagebox.showinfo("Success", "Ticket data updated successfully")

def refresh_table():
    records = my_tree.get_children()
    for element in records:
        my_tree.delete(element)
    for row in read():
        my_tree.insert(parent='', index='end', text='', values=(row[0], row[1], row[2], row[3]))

def save_data():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    results = cursor.fetchall()
    conn.close()

    with open("ticket_data.txt", "w") as file:
        for result in results:
            file.write(f"ID: {result[0]}\t|\t")
            file.write(f"Name: {result[1]}\t|\t")
            file.write(f"Price: {result[2]}\t|\t")
            file.write(f"Quantity: {result[3]}\n")
            file.write("------------------------------\n")

# Login Window
login_window = Toplevel()
login_window.title("Login")
login_window.geometry("300x150")

# Labels
labelUsername = Label(login_window, text="Username:")
labelUsername.pack()
labelPassword = Label(login_window, text="Password:")
labelPassword.pack()

# Entry Fields
entryUsername = Entry(login_window)
entryUsername.pack()
entryPassword = Entry(login_window, show="*")
entryPassword.pack()

# Login Button
loginBtn = Button(login_window, text="Login", command=login)
loginBtn.pack()

root.mainloop()
