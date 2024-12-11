import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import pyttsx3
import requests 

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to fetch exchange rates from the API
def fetch_exchange_rate():
    """Fetch the exchange rate for the selected currencies."""
    source = source_currency.get()
    target = target_currency.get()

    if source == "Select Currency" or target == "Select Currency":
        messagebox.showwarning("Warning", "Please select both currencies.")
        return

    try:
        # api key
        api_key = "bc220c2a512c7990c424c285"
        url = f"https://v6.exchangerate-api.com/v6/bc220c2a512c7990c424c285/latest/"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            # Get the exchange rate for the target currency
            rate = data["conversion_rates"].get(target)
            if rate:
                rate_entry.delete(0, END)
                rate_entry.insert(0, round(rate, 4))  # Insert fetched rate
            else:
                messagebox.showerror("Error", "Currency not found in API response.")
        else:
            messagebox.showerror("Error", f"API request failed: {data['error-type']}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Tkinter GUI setup
root = Tk()
root.title('Currency Conversion')
root.geometry("600x600")

# Create tabs
my_notebook = ttk.Notebook(root)
my_notebook.pack(pady=5)

# Creating two frames
currency_frame = Frame(my_notebook, width=550, height=550)
conversion_frame = Frame(my_notebook, width=550, height=550)

currency_frame.pack(fill="both", expand=1)
conversion_frame.pack(fill="both", expand=1)

# Add tabs
my_notebook.add(currency_frame, text="Currencies")
my_notebook.add(conversion_frame, text="Convert")

# Disable 2nd tab
my_notebook.tab(1, state='disabled')

###########
# Currency Selection
###########

# List of currencies
currencies = ['USD', 'EUR', 'GBP', 'INR', 'JPY', 'AUD', 'CAD', 'CHF', 'CNY', 'NZD']

def lock():
    if not source_currency.get() or not target_currency.get() or not rate_entry.get():
        messagebox.showwarning("WARNING!", "You didn't fill out all the fields")
    else:
        # Disable dropdowns and entry box
        source_currency.config(state="disabled")
        target_currency.config(state="disabled")
        rate_entry.config(state="disabled")
        # Enable tab
        my_notebook.tab(1, state='normal')
        # Change tab labels
        amount_label.config(text=f'Amount of {source_currency.get()} to convert to {target_currency.get()}')
        converted_label.config(text=f'Equals this many {target_currency.get()}')
        convert_button.config(text=f'Convert from {source_currency.get()}')

def unlock():
    # Enable dropdowns and entry box
    source_currency.config(state="readonly")
    target_currency.config(state="readonly")
    rate_entry.config(state="normal")
    # Disable tab
    my_notebook.tab(1, state='disabled')

# Home Currency Dropdown
home = LabelFrame(currency_frame, text="Home Currency")
home.pack(pady=20)

source_currency = ttk.Combobox(home, values=currencies, state="readonly", font=("Monospace Text", 16))
source_currency.pack(pady=10, padx=10)
source_currency.set("Select Currency")

# Conversion Currency Dropdown
conversion = LabelFrame(currency_frame, text="Conversion Currency")
conversion.pack(pady=20)

target_currency = ttk.Combobox(conversion, values=currencies, state="readonly", font=("Monospace Text", 16))
target_currency.pack(pady=10, padx=10)
target_currency.set("Select Currency")

# Conversion Rate Entry
rate_label = Label(conversion, text="Currency Conversion Rate (Auto-Fetched)")
rate_label.pack(pady=20)

rate_entry = Entry(conversion, font=("Monospace Text", 24))
rate_entry.pack(pady=10, padx=10)

# Button frame
button_frame = Frame(currency_frame)
button_frame.pack(pady=20)

# Fetch Rate Button
fetch_rate_button = Button(button_frame, text="Fetch Rate", command=fetch_exchange_rate)
fetch_rate_button.grid(row=0, column=0, padx=20)

lock_button = Button(button_frame, text="Lock", command=lock)
lock_button.grid(row=0, column=1, padx=20)

unlock_button = Button(button_frame, text="Unlock", command=unlock)
unlock_button.grid(row=0, column=2, padx=20)

##############
# Conversion Tab
##############

def convert():
    # Clear converted entry box
    converted_entry.delete(0, END)
    # Convert
    try:
        conversion = float(rate_entry.get()) * float(amount_entry.get())
        conversion = round(conversion, 2)  # Convert to two decimals
        conversion = '{:,}'.format(conversion)  # Add commas
        # Update entry box
        converted_entry.insert(0, conversion)
        result = f"{amount_entry.get()} {source_currency.get()} equals {conversion} {target_currency.get()}"
        speak(result)
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")
        speak("Invalid input. Please enter valid numbers.")

def clear():
    amount_entry.delete(0, END)
    converted_entry.delete(0, END)

# Amount to Convert
amount_label = LabelFrame(conversion_frame, text="Amount to Convert")
amount_label.pack(pady=20)

amount_entry = Entry(amount_label, font=("Monospace Text", 24))
amount_entry.pack(pady=10, padx=10)

convert_button = Button(amount_label, text="Convert", command=convert)
convert_button.pack(pady=20)

# Equals Frame
converted_label = LabelFrame(conversion_frame, text="Converted Currency")
converted_label.pack(pady=20)

converted_entry = Entry(converted_label, font=("Monospace Text", 24), bd=0, bg="systembuttonface")
converted_entry.pack(pady=10, padx=10)

# Clear Button
clear_button = Button(conversion_frame, text="Clear", command=clear)
clear_button.pack(pady=20)

# Fake label for spacing
spacer = Label(conversion_frame, text="", width=68)
spacer.pack()

root.mainloop()
