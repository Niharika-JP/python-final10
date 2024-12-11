import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox  # to have a messagebox pop-up

root = Tk()
root.title('Currency Conversion')
root.geometry("600x600")
root.configure(bg="lightblue")

# Create tabs
my_notebook = ttk.Notebook(root)
my_notebook.pack(pady=5)

# Creating two frames
currency_frame = Frame(my_notebook, width=550, height=550, bg="white")
conversion_frame = Frame(my_notebook, width=550, height=550, bg="white")

currency_frame.pack(fill="both", expand=1)
conversion_frame.pack(fill="both", expand=1)

# Add tabs
my_notebook.add(currency_frame, text="Currencies")
my_notebook.add(conversion_frame, text="Convert")

# Style for highlighting active tab
style = ttk.Style()
style.configure("TNotebook", background="lightblue")
style.configure("TNotebook.Tab", background="lightgray", foreground="black")
style.map("TNotebook.Tab", background=[("selected", "cyan")], foreground=[("selected", "black")])

# Disable 2nd tab
my_notebook.tab(1, state='disabled')

# Available currencies 
# (United States Dollar, Euro, British pound Sterling, Indian Rupee, Australian Dollar, Canadian Dollar, Japanese Yen, Chinese Yuan)
currencies = ["USD", "EUR", "GBP", "INR", "AUD", "CAD", "JPY", "CNY"]

###########
# Currency
###########

def lock():
    if not home_currency.get() or not conversion_currency.get() or not rate_entry.get():
        messagebox.showwarning("WARNING!", "You didn't fill out all the fields ")
    else:
        # Disable dropdowns and entry boxes
        home_menu.config(state="disabled")
        conversion_menu.config(state="disabled")
        rate_entry.config(state="disabled")
        # Enable tab
        my_notebook.tab(1, state='normal')
        # Change tab fields
        amount_label.config(text=f'Amount of {home_currency.get()} To Convert to {conversion_currency.get()}')
        converted_label.config(text=f'Equals This Many {conversion_currency.get()}')
        convert_button.config(text=f'Convert from {home_currency.get()}')

def unlock():
    # Enable dropdowns and entry boxes
    home_menu.config(state="normal")
    conversion_menu.config(state="normal")
    rate_entry.config(state="normal")
    # Disable tab
    my_notebook.tab(1, state='disabled')

def swap():
    # Swap the selected currencies
    home_currency.set(conversion_currency.get())
    conversion_currency.set(home_currency.get())

# Home currency dropdown
home = LabelFrame(currency_frame, text="Home Currency", bg="white")
home.pack(pady=20)

# Create a StringVar to store the selected currency value
home_currency = StringVar()
home_currency.set(currencies[0])  # Default value
home_menu = OptionMenu(home, home_currency, *currencies)
home_menu.pack(pady=10, padx=10)

# Conversion currency dropdown
conversion = LabelFrame(currency_frame, text="Conversion Currency", bg="white")
conversion.pack(pady=20)

# Create a StringVar to store the selected currency value
conversion_currency = StringVar()
conversion_currency.set(currencies[1])  # Default value
conversion_menu = OptionMenu(conversion, conversion_currency, *currencies)
conversion_menu.pack(pady=10, padx=10)

# Conversion rate entry
rate_label = Label(conversion, text="Currency Conversion Rate...", bg="white")
rate_label.pack(pady=10)
rate_entry = Entry(conversion, font=("Monospace Text", 24))
rate_entry.pack(pady=10, padx=10)

# Button frame
button_frame = Frame(currency_frame, bg="white")
button_frame.pack(pady=20)

# Creating buttons
lock_button = Button(button_frame, text="Lock", bg="green", fg="white", command=lock)
lock_button.grid(row=0, column=0, padx=20)

unlock_button = Button(button_frame, text="Unlock", bg="red", fg="white", command=unlock)
unlock_button.grid(row=0, column=1, padx=20)

swap_button = Button(button_frame, text="Swap", bg="blue", fg="white", command=swap)
swap_button.grid(row=0, column=2, padx=20)

##############
# Conversion
##############

def convert():
    # Clear converted entry box
    converted_entry.delete(0, END)

    # Convert
    conversion = float(rate_entry.get()) * float(amount_entry.get())
    # Convert to two decimals
    conversion = round(conversion, 2)
    # Add commas
    conversion = '{:,}'.format(conversion)
    # Update entry box
    converted_entry.insert(0, conversion)

def clear():
    amount_entry.delete(0, END)
    converted_entry.delete(0, END)

amount_label = LabelFrame(conversion_frame, text="Amount to Convert", bg="white")
amount_label.pack(pady=20)

# Entry box for amount
amount_entry = Entry(amount_label, font=("Monospace Text", 24))
amount_entry.pack(pady=10, padx=10)

# Convert button
convert_button = Button(amount_label, text="Convert", bg="green", fg="white", command=convert)
convert_button.pack(pady=20)

# Equals frame
converted_label = LabelFrame(conversion_frame, text="Converted Currency", bg="white")
converted_label.pack(pady=20)

# Converted entry
converted_entry = Entry(converted_label, font=("Monospace Text", 24), bd=0, bg="lightgray")
converted_entry.pack(pady=10, padx=10)

# Clear frame
clear_button = Button(conversion_frame, text="Clear", bg="orange", fg="white", command=clear)
clear_button.pack(pady=20)

# Fake label for spacing
spacer = Label(conversion_frame, text="", width=68, bg="white")
spacer.pack()

root.mainloop()
