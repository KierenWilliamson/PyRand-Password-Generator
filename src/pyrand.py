import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import pyrand_client as PyClient
import pyrand_exceptions as passExcept

root = tk.Tk()
root.title("PyRand Password Generator")

# CONSTANTS & GLOBALS
RADIO_CHOICE = ("True", "False")
CAPITAL_BOOL = False
LOWERCASE_BOOL = False
NUMS_BOOL = False
SYMB_BOOL = False
PASSWORD_LENGTH = 0
TOTAL_NUMS = 0
TOTAL_SYMBS = 0


# Center the GUI window on the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
WINDOW_WIDTH = 592
WINDOW_HEIGHT = 625
center_x = int((screen_width / 2) - (WINDOW_WIDTH / 2))
center_y = int((screen_height / 2) - (WINDOW_HEIGHT / 2))

root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{center_x}+{center_y}')


# Set the size constraints and attributes of the window
# root.resizable(False, False)
root.attributes("-topmost", 1)
root.columnconfigure(0, weight=3)
root.columnconfigure(1, weight=1)


# FUNCTIONS
# gathers the data entered into the GUI window then inputs that data into the instantiated password object to create
# the random password
def generate_password():
    gather_gui_data()
    password_obj = PyClient.Password(PASSWORD_LENGTH, TOTAL_NUMS, TOTAL_SYMBS, CAPITAL_BOOL, LOWERCASE_BOOL)

# handles the event that the length of the password is set to be longer than the available number of characters
    # try:
    #     password_obj.randomize()
    # except passExcept.LengthError:
    #     showinfo(title="Notice", message="Since there will be no letter characters, the total password length cannot "
    #                                      "exceed the sum of the symbols and numbers")

    # unlock the text field, clears the text field of previous input then inputs the randomly generated password
    # afterward, the text field is made un-editable again
    pass_text["state"] = "normal"
    pass_text.delete("1.0", "end")
    pass_text.insert("1.0", password_obj.parse_password())
    pass_text["state"] = "disabled"


# gathers the boolean data for the first four GUI window questions, the totals for the nums and symbols, and the desired
# length of the password. It will handle the possible exceptions for each process
def gather_gui_data():
    try:
        get_booleans()
        get_minimums()
        set_password_length()
    except passExcept.UnsetButtonError:
        showinfo(title="Notice", message="All True/False questions must be answered before proceeding")


# changes the value of the spinboxes (totals for nums and symbols) to 0 if numbers/symbols are toggled off
def set_password_length():
    global PASSWORD_LENGTH
    PASSWORD_LENGTH = int(get_slider_value())

    if PASSWORD_LENGTH == 0:
        PASSWORD_LENGTH = int(current_ttl_num.get() + current_ttl_symbol.get())
        length_val_label.configure(text="Current Value: " + str(PASSWORD_LENGTH))


# converts the "True/False" string stored within the radio buttons' variable into a boolean. This is then stored in the
# global variable for use in the password generator
def get_booleans():
    try:
        global CAPITAL_BOOL, LOWERCASE_BOOL, NUMS_BOOL, SYMB_BOOL

        CAPITAL_BOOL = eval(capital_radio_var.get())
        LOWERCASE_BOOL = eval(lower_radio_var.get())
        NUMS_BOOL = eval(number_radio_var.get())
        SYMB_BOOL = eval(symbol_radio_var.get())
    except SyntaxError:
        raise passExcept.UnsetButtonError


# gathers the requested total nums/symbols and updates the corresponding global variable if the corresponding boolean
# variable was True. If not, it sets the total to zero, sends a warning, and updates the global variable to zero.
def get_minimums():
    global TOTAL_NUMS, TOTAL_SYMBS

    if not NUMS_BOOL:
        showinfo(title="Notice", message="Due to 'Include Numbers?' being false, you will have no numeric characters")
        current_ttl_num.set(0)
        TOTAL_NUMS = int('{:.0f}'.format(current_ttl_num.get()))
    else:
        TOTAL_NUMS = int('{:.0f}'.format(current_ttl_num.get()))

    if not SYMB_BOOL:
        showinfo(title="Notice", message="Due to 'Include Symbols?' being false, you will have no special symbols")
        current_ttl_symbol.set(0)
        TOTAL_SYMBS = int('{:.0f}'.format(current_ttl_symbol.get()))
    else:
        TOTAL_SYMBS = int('{:.0f}'.format(current_ttl_symbol.get()))


# returns the value of the length scale
def get_slider_value():
    return '{: .0f}'.format(length_slider_var.get())


# When the length scale is interacted with, its minimum value is set to be the sum of the total numbers and symbols.
# Then, the length scale's label is updated to the value the scale is currently on
def slider_changed(event):
    length_slider.configure(from_=current_ttl_num.get() + current_ttl_symbol.get())
    length_val_label.configure(text="Current Value: " + str(get_slider_value()))


# WIDGETS
SUBGRID_COLUMN = 0

title_label = ttk.Label(root, text="Your Random Password is...",
                       font=("Times New Roman", 11, "bold"))
title_label.grid(column=0, row=0, columnspan=2, padx=5, pady=5)

# FIXME: insert however the password will be displayed here
# Password's text widget
pass_text = tk.Text(root, height=1)
pass_text.grid(column=0, row=1, columnspan=2)

# Capital label and radio button label frame
capital_label = ttk.Label(root, text="Include Capitals?", font=("Times New Roman", 13))
capital_label.grid(column=0, row=2, sticky=tk.W, padx=100)

capital_radio_lf = ttk.LabelFrame(root, text="Ex. A, F, G, etc")
capital_radio_lf.grid(column=1, row=2, padx=50, pady=20)

capital_radio_var = tk.StringVar()
for choice in RADIO_CHOICE:
    # create the radio buttons
    radio = ttk.Radiobutton(capital_radio_lf, text=choice, value=choice, variable=capital_radio_var)
    radio.grid(column=SUBGRID_COLUMN, row=0, ipadx=10, ipady=10)
    SUBGRID_COLUMN += 1


# Lowercase label and radio button label frame
lowercase_label = ttk.Label(root, text="Include Lowercase?", font=("Times New Roman", 13))
lowercase_label.grid(column=0, row=3, sticky=tk.W, padx=100)

lowercase_radio_lf = ttk.LabelFrame(root, text="Ex. i, o, r, etc")
lowercase_radio_lf.grid(column=1, row=3, padx=50, pady=10)

lower_radio_var = tk.StringVar()
for choice in RADIO_CHOICE:
    # create the radio buttons
    radio = ttk.Radiobutton(lowercase_radio_lf, text=choice, value=choice, variable=lower_radio_var)
    radio.grid(column=SUBGRID_COLUMN, row=0, ipadx=10, ipady=10)
    SUBGRID_COLUMN += 1


# Numbers label and radio button label frame
number_label = ttk.Label(root, text="Include Numbers?", font=("Times New Roman", 13))
number_label.grid(column=0, row=4, sticky=tk.W, padx=100)

number_radio_lf = ttk.LabelFrame(root, text="Numbers 0-9")
number_radio_lf.grid(column=1, row=4, padx=50, pady=10)

number_radio_var = tk.StringVar()
for choice in RADIO_CHOICE:
    # create the radio buttons
    radio = ttk.Radiobutton(number_radio_lf, text=choice, value=choice, variable=number_radio_var)
    radio.grid(column=SUBGRID_COLUMN, row=0, ipadx=10, ipady=10)
    SUBGRID_COLUMN += 1

# FIXME: make sure spinboxes trigger a notification window if the input value is above 12, then reset the input value
# FIXME: to 12.
# Symbols label and radio button label frame
symbol_label = ttk.Label(root, text="Include Symbols?", font=("Times New Roman", 13))
symbol_label.grid(column=0, row=5, sticky=tk.W, padx=100)

symbol_radio_lf = ttk.LabelFrame(root, text="Ex. &, #, $, etc")
symbol_radio_lf.grid(column=1, row=5, padx=50, pady=10)

symbol_radio_var = tk.StringVar()
for choice in RADIO_CHOICE:
    # create the radio buttons
    radio = ttk.Radiobutton(symbol_radio_lf, text=choice, value=choice, variable=symbol_radio_var)
    radio.grid(column=SUBGRID_COLUMN, row=0, ipadx=10, ipady=10)
    SUBGRID_COLUMN += 1


# TtlNum's label and spinbox
ttl_num_label = ttk.Label(root, text="Total Numbers?", font=("Times New Roman", 13))
ttl_num_label.grid(column=0, row=6, sticky=tk.W, padx=100)

current_ttl_num = tk.DoubleVar(value=0)
ttl_num_spinbox = ttk.Spinbox(root, from_=0, to=12, textvariable=current_ttl_num, wrap=True)
ttl_num_spinbox.grid(column=1, row=6, pady=10)


# TtlSymbol's label and spinbox
ttl_symbol_label = ttk.Label(root, text="Total Symbols?", font=("Times New Roman", 13))
ttl_symbol_label.grid(column=0, row=7, sticky=tk.W, padx=100)

current_ttl_symbol = tk.DoubleVar(value=0)
ttl_symbol_spinbox = ttk.Spinbox(root, from_=0, to=12, textvariable=current_ttl_symbol, wrap=True)
ttl_symbol_spinbox.grid(column=1, row=7, pady=10)


# Label and Slider for the length of the password
length_label = ttk.Label(text="Password Length", font=("Times New Roman", 13))
length_label.grid(column=0, row=8, sticky=tk.W, padx=100)

length_slider_lf = ttk.LabelFrame(root)
length_slider_lf.grid(column=1, row=8)

length_slider_var = tk.DoubleVar()
length_slider = ttk.Scale(length_slider_lf, from_=0, to=35,
                         variable=length_slider_var, command=slider_changed)
length_slider.grid(column=0, row=0, sticky=tk.N)

length_val_label = ttk.Label(length_slider_lf, text="Current Value: ")
length_val_label.grid(column=0, row=1, sticky=tk.N)


# FIXME: finish the functionality of the generate password button
gen_pass_bttn = ttk.Button(root, text="Generate Password", command=generate_password)
gen_pass_bttn.grid(column=0, row=9, sticky=tk.S, columnspan=2, ipadx=15, ipady=15)

# FIXME: Save Generated passwords so that they arte note generated twice. Hash passwords when they are saved so they cant be accessed
# FIXME: MD5, SHA, Hashing
# EVENT LOOP
root.mainloop()
