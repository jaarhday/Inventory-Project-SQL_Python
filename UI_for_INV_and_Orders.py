import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Database connection
def connect_db():
    return sqlite3.connect("inventory.db")

# Adds a new product to the Products table in the database
def add_product(name, quantity, price):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Products (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
    conn.commit()
    conn.close()

# Updates the quantity of a specific product by a given amount in the Products table
def update_quantity(product_id, amount):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Products SET quantity = quantity + ? WHERE product_id = ?", (amount, product_id))
    conn.commit()
    conn.close()

# Records an order in the Orders table and updates the product's quantity in the Products table
def record_order(product_id, quantity):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Orders (product_id, quantity) VALUES (?, ?)", (product_id, quantity))
    cursor.execute("UPDATE Products SET quantity = quantity - ? WHERE product_id = ?", (quantity, product_id))
    conn.commit()
    conn.close()

# User Interface
def add_product_ui():
    name = entry_name.get()
    quantity = int(entry_quantity.get())
    price = float(entry_price.get())
    add_product(name, quantity, price)
    messagebox.showinfo("Success", "Product added successfully!")

def view_inventory():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products")
    rows = cursor.fetchall()
    inventory_list.delete(1.0, tk.END)  # Clear current inventory list
    for row in rows:
        inventory_list.insert(tk.END, f"ID: {row[0]} | Name: {row[1]} | Quantity: {row[2]} | Price: ${row[3]:.2f}\n")
    conn.close()

# List to store orders
order_list = []

# Function to place an order
def make_order():
    try:
        # Get the selected product and quantity
        product_name = product_var.get()
        quantity = int(entry_order_quantity.get())
        
        if quantity <= 0:
            messagebox.showerror("Error", "Quantity must be greater than zero.")
            return

        # Fetch the product ID and current quantity from the database
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT product_id, quantity, price FROM Products WHERE name = ?", (product_name,))
        product = cursor.fetchone()

        if product is None:
            messagebox.showerror("Error", "Selected product not found.")
            return

        product_id, available_quantity, price = product

        # Record the order and update the inventory
        record_order(product_id, quantity)
        messagebox.showinfo("Success", f"Order for {quantity} {product_name}(s) placed successfully!")

        # Add the order to the order list
        order_list.append({
            "product_name": product_name,
            "quantity": quantity,
            "price": price,
            "total_price": quantity * price,
            "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        conn.close()

        # Save the order to a text file
        save_order_to_file(product_name, quantity, price)

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid quantity.")

# Function to save the order to a text file
def save_order_to_file(product_name, quantity, price):
    # Get the current date and time
    order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_price = quantity * price

    # Create or append to the file
    with open("order_history.txt", "a") as file:
        file.write(f"Order Date: {order_date}\n")
        file.write(f"Product: {product_name}\n")
        file.write(f"Quantity: {quantity}\n")
        file.write(f"Price per Item: ${price:.2f}\n")
        file.write(f"Total Price: ${total_price:.2f}\n")
        file.write("-" * 40 + "\n")

# Function to print the full order list
def print_order_list():
    if not order_list:
        messagebox.showinfo("No Orders", "No orders have been placed.")
        return

    order_details = "Order Summary:\n\n"
    for order in order_list:
        order_details += f"Product: {order['product_name']}\n"
        order_details += f"Quantity: {order['quantity']}\n"
        order_details += f"Total Price: ${order['total_price']:.2f}\n"
        order_details += f"Order Date: {order['order_date']}\n"
        order_details += "-" * 40 + "\n"

    # Display the full order list
    messagebox.showinfo("Order List", order_details)

# Function to clear the order history
def clear_order_history():
    global order_list
    order_list = []  # Clear the in-memory order list
    with open("order_history.txt", "w") as file:
        file.truncate(0)  # Clear the contents of the file
    messagebox.showinfo("Order History Cleared", "All orders have been cleared.")


# Clear database
def clear_database():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Orders")
    cursor.execute("DELETE FROM Products")
    conn.commit()
    conn.close()
    
def adjust_quantity(product_name, new_quantity):
    # Establish a connection to the database
    conn = connect_db()
    cursor = conn.cursor()

    # Update the quantity of the specified product
    cursor.execute("UPDATE Products SET quantity = ? WHERE name = ?", (new_quantity, product_name))
    conn.commit()

    # Check if the product exists
    if cursor.rowcount == 0:
        messagebox.showerror("Error", f"Product {product_name} not found.")
    else:
        messagebox.showinfo("Success", f"Quantity for {product_name} updated to {new_quantity}.")

    # Close the connection to the database
    conn.close()

def lookup_product(product_name):
    # Establish a connection to the database
    conn = connect_db()
    cursor = conn.cursor()

    # Lookup the product details by name
    cursor.execute("SELECT name, quantity, price FROM Products WHERE name = ?", (product_name,))
    product = cursor.fetchone()

    # Display the product details or an error if not found
    if product:
        details = f"Product: {product[0]}\nQuantity: {product[1]}\nPrice: ${product[2]:.2f}"
        messagebox.showinfo("Product Found", details)
    else:
        messagebox.showerror("Error", f"Product {product_name} not found.")

    # Close the connection to the database
    conn.close()

#####################################################################################################################

# GUI setup
root = tk.Tk()
root.title("Inventory Management")

# Set the window size
root.geometry("1000x600") 

# Create a frame for the left side 
frame_inventory = tk.Frame(root, width=500)
frame_inventory.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Fields for adding a product
tk.Label(frame_inventory, text="Product Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_name = tk.Entry(frame_inventory)
entry_name.grid(row=0, column=1, padx=10, pady=10)

tk.Label(frame_inventory, text="Quantity:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_quantity = tk.Entry(frame_inventory)
entry_quantity.grid(row=1, column=1, padx=10, pady=10)

tk.Label(frame_inventory, text="Price:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
entry_price = tk.Entry(frame_inventory)
entry_price.grid(row=2, column=1, padx=10, pady=10)

# Button to add a product
tk.Button(frame_inventory, text="Add Product", command=lambda: add_product(entry_name.get(), int(entry_quantity.get()), float(entry_price.get()))).grid(row=3, column=1, padx=10, pady=10)

# Button to view inventory
tk.Button(frame_inventory, text="View Inventory", command=view_inventory).grid(row=4, column=1, padx=10, pady=10)

# Button to clear the database
tk.Button(frame_inventory, text="Clear Database", command=clear_database).grid(row=5, column=1, padx=10, pady=10)

# GUI setup for adjusting quantity
tk.Label(frame_inventory, text="Product Name (Adjust Qty):").grid(row=6, column=0, padx=10, pady=10, sticky="w")
entry_adjust_name = tk.Entry(frame_inventory)
entry_adjust_name.grid(row=6, column=1, padx=10, pady=10)

tk.Label(frame_inventory, text="New Quantity:").grid(row=7, column=0, padx=10, pady=10, sticky="w")
entry_adjust_quantity = tk.Entry(frame_inventory)
entry_adjust_quantity.grid(row=7, column=1, padx=10, pady=10)

# Button to adjust quantity
tk.Button(frame_inventory, text="Adjust Quantity", command=lambda: adjust_quantity(entry_adjust_name.get(), int(entry_adjust_quantity.get()))).grid(row=8, column=1, padx=10, pady=10)

# GUI setup for product lookup
tk.Label(frame_inventory, text="Product Name (Lookup):").grid(row=9, column=0, padx=10, pady=10, sticky="w")
entry_lookup_name = tk.Entry(frame_inventory)
entry_lookup_name.grid(row=9, column=1, padx=10, pady=10)

# Button to lookup product
tk.Button(frame_inventory, text="Lookup Product", command=lambda: lookup_product(entry_lookup_name.get())).grid(row=10, column=1, padx=10, pady=10)

# Text box to display inventory
inventory_list = tk.Text(frame_inventory, height=20, width=40)
inventory_list.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Create a frame for the right side
frame_order = tk.Frame(root, width=500)
frame_order.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Section for making an order
tk.Label(frame_order, text="Select Product to Order:").grid(row=0, column=0, padx=10, pady=10, sticky="w")

# Fetch products for the dropdown
conn = connect_db()
cursor = conn.cursor()
cursor.execute("SELECT name FROM Products")
product_names = [row[0] for row in cursor.fetchall()]
conn.close()

product_var = tk.StringVar(root)
product_var.set(product_names[0])

product_menu = tk.OptionMenu(frame_order, product_var, *product_names)
product_menu.grid(row=0, column=1, padx=10, pady=10)

tk.Label(frame_order, text="Quantity to Order:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_order_quantity = tk.Entry(frame_order)
entry_order_quantity.grid(row=1, column=1, padx=10, pady=10)

# Button to make an order
tk.Button(frame_order, text="Make Order", command=make_order).grid(row=2, column=1, padx=10, pady=10)

# Button to view all orders
tk.Button(frame_order, text="View All Orders", command=print_order_list).grid(row=3, column=1, padx=10, pady=10)

# Button to clear order history
tk.Button(frame_order, text="Clear Order History", command=clear_order_history).grid(row=4, column=1, padx=10, pady=10)

# Start the GUI
root.mainloop()