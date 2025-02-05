'''Main program for the tkinter PyRand application.'''

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from ast import literal_eval
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

# CENTER THE GUI WINDOW
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
WINDOW_WIDTH = 592
WINDOW_HEIGHT = 625
center_x = int((screen_width / 2) - (WINDOW_WIDTH / 2))
center_y = int((screen_height / 2) - (WINDOW_HEIGHT / 2))

root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{center_x}+{center_y}')

# SET WINDOW SIZE AND ATTRIBUTE CONSTRAINTS
root.attributes("-topmost", 1)
root.columnconfigure(0, weight=3)
root.columnconfigure(1, weight=1)

# FUNCTIONS
def generate_password():
    '''
    Gathers the data entered into the GUI window then instantiates
    a password object. The text field where the password is displayed
    is unlocked, cleared of previous input, then filled with the randomly 
    generated password. The text field is made uneditable afterward.
    
    Args:
        None

    Returns:
        None
    '''
    gather_gui_data()
    # FIXME: make password obj generate only once upon launch of the app. The obj's functions are reusable. 
    # Currently, a new obj is created everytime this function is called, which is a waste on memory.
    password_obj = PyClient.Password(PASSWORD_LENGTH, TOTAL_NUMS,
                                     TOTAL_SYMBS, CAPITAL_BOOL, LOWERCASE_BOOL)

    # handles the event that the length of the password is set to be longer than the available number of characters
    # try:
    #     password_obj.randomize()
    # except passExcept.LengthError:
    #     showinfo(title="Notice", message="Since there will be no letter characters, the total password length cannot "
    #                                      "exceed the sum of the symbols and numbers")
    pass_text["state"] = "normal"
    pass_text.delete("1.0", "end")
    pass_text.insert("1.0", password_obj.parse_password())
    pass_text["state"] = "disabled"


def gather_gui_data():
    '''
    Gathers the boolean data for the first four GUI window prompts, 
    the totals for the numbers and symbols, and the desired password length.

    Args:
        None

    Returns:
        None
    '''
    try:
        get_booleans()
        get_minimums()
        set_password_length()
    except passExcept.UnsetButtonError:
        showinfo(title="Notice",
                 message="All True/False questions must be answered before proceeding")


def set_password_length():
    '''
    Changes the value of the numbers/symbols spinboxes to 0 if the numbers/symbols are toggled off.

    Args:
        None

    Return:
        None
    '''
    global PASSWORD_LENGTH
    PASSWORD_LENGTH = int(get_slider_value())

    if PASSWORD_LENGTH == 0:
        PASSWORD_LENGTH = int(current_ttl_num.get() + current_ttl_symbol.get())
        length_val_label.configure(text="Current Value: " + str(PASSWORD_LENGTH))


def get_booleans():
    '''
    Converts the "True/False" string stored within the radio buttons's variable into a boolean. 
    Global boolean variables are updated accordingly.

    Args:
        None

    Return:
        None
    '''
    try:
        global CAPITAL_BOOL, LOWERCASE_BOOL, NUMS_BOOL, SYMB_BOOL

        CAPITAL_BOOL = literal_eval(capital_radio_var.get())
        LOWERCASE_BOOL = literal_eval(lower_radio_var.get())
        NUMS_BOOL = literal_eval(number_radio_var.get())
        SYMB_BOOL = literal_eval(symbol_radio_var.get())
    except SyntaxError:
        raise passExcept.UnsetButtonError


def get_minimums():
    '''
    Updates the totals for numbers/symbols if its corresponding boolean variable is True. 
    If not, it sets the total to zero, sends a warning, and updates the global variable to zero.

    Args:
        None

    Return:
        None
    '''
    global TOTAL_NUMS, TOTAL_SYMBS

    if not NUMS_BOOL:
        showinfo(title="Notice",
            message="Due to 'Include Numbers?' being false, you will have no numeric characters.")
        current_ttl_num.set(0)
        TOTAL_NUMS = int('{:.0f}'.format(current_ttl_num.get()))
    else:
        TOTAL_NUMS = int('{:.0f}'.format(current_ttl_num.get()))

    if not SYMB_BOOL:
        showinfo(title="Notice",
            message="Due to 'Include Symbols?' being false, you will have no special symbols.")
        current_ttl_symbol.set(0)
        TOTAL_SYMBS = int('{:.0f}'.format(current_ttl_symbol.get()))
    else:
        TOTAL_SYMBS = int('{:.0f}'.format(current_ttl_symbol.get()))


def get_slider_value():
    '''
    Gets the value of the length slider

    Args:
        None

    Return:
        float: value of the length slider
    '''
    return '{: .0f}'.format(length_slider_var.get())


def slider_changed(event):
    '''
    When the length scale is interacted with, its minimum value is set to be the 
    sum of the total numbers and symbols. The length scale's label is then updated 
    to the value of the scale.

    Args:
        None
    
    Return:
        None
    '''
    length_slider.configure(from_=current_ttl_num.get() + current_ttl_symbol.get())
    length_val_label.configure(text="Current Value: " + str(get_slider_value()))


# WIDGETS
SUBGRID_COLUMN = 0
title_label = ttk.Label(root, text="Your Random Password is...",
                       font=("Times New Roman", 11, "bold"))
title_label.grid(column=0, row=0, columnspan=2, padx=5, pady=5)

# FIXME: insert however the password will be displayed here
# PASSWORD TEXT WIDGET
pass_text = tk.Text(root, height=1)
pass_text.grid(column=0, row=1, columnspan=2)


# CAPITAL LABEL/RADIO BUTTON LABEL FRAME
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


# LOWERCASE LABEL/RADIO BUTTON LABEL FRAME
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


# NUMBERS LABEL/RADIO BUTTON LABEL FRAME
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
# SYMBOLS LABEL/RADIO BUTTON LABEL FRAME
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


# TTL_NUMS'S LABEL AND SPINBOX
ttl_num_label = ttk.Label(root, text="Total Numbers?", font=("Times New Roman", 13))
ttl_num_label.grid(column=0, row=6, sticky=tk.W, padx=100)

current_ttl_num = tk.DoubleVar(value=0)
ttl_num_spinbox = ttk.Spinbox(root, from_=0, to=12, textvariable=current_ttl_num, wrap=True)
ttl_num_spinbox.grid(column=1, row=6, pady=10)


# TTL_SYMBOLS'S LABEL AND SPINBOX
ttl_symbol_label = ttk.Label(root, text="Total Symbols?", font=("Times New Roman", 13))
ttl_symbol_label.grid(column=0, row=7, sticky=tk.W, padx=100)

current_ttl_symbol = tk.DoubleVar(value=0)
ttl_symbol_spinbox = ttk.Spinbox(root, from_=0, to=12, textvariable=current_ttl_symbol, wrap=True)
ttl_symbol_spinbox.grid(column=1, row=7, pady=10)


# PASSWORD LENGTH LABEL AND SLIDER
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
# GENERATE PASSWORD BUTTON
gen_pass_bttn = ttk.Button(root, text="Generate Password", command=generate_password)
gen_pass_bttn.grid(column=0, row=9, sticky=tk.S, columnspan=2, ipadx=15, ipady=15)

# FIXME: Save Generated passwords so that they arte note generated twice. Hash passwords when they are saved so they cant be accessed
# FIXME: MD5, SHA, Hashing
# EVENT LOOP
root.mainloop()
