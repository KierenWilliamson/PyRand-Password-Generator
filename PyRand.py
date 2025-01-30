import tkinter as tk
import pyrand_client as PyClient
import pyrand_exceptions as passExcept
from tkinter import ttk
from tkinter.messagebox import showinfo

root = tk.Tk()
root.title("PyRand Password Generator")

# CONSTANTS & GLOBALS
RADIO_CHOICE = ("True", "False")
globalCapBool = False
globalLowerBool = False
globalNumsBool = False
globalSymBool = False
globalPassLength = 0
globalTtlNums = 0
globalTtlSyms = 0


# Center the GUI window on the screen
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
windowWidth = 592
windowHeight = 625
centerX = int((screenWidth / 2) - (windowWidth / 2))
centerY = int((screenHeight / 2) - (windowHeight / 2))

root.geometry(f'{windowWidth}x{windowHeight}+{centerX}+{centerY}')


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
    password_obj = PyClient.Password(globalPassLength, globalTtlNums, globalTtlSyms, globalCapBool, globalLowerBool)

# handles the event that the length of the password is set to be longer than the available number of characters
    try:
        password_obj.randomize()
    except passExcept.LengthError:
        showinfo(title="Notice", message="Since there will be no letter characters, the total password length cannot "
                                         "exceed the sum of the symbols and numbers")

    # unlock the text field, clears the text field of previous input then inputs the randomly generated password
    # afterward, the text field is made un-editable again
    passText["state"] = "normal"
    passText.delete("1.0", "end")
    passText.insert("1.0", password_obj.parse_password())
    passText["state"] = "disabled"


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
    global globalPassLength
    globalPassLength = int(get_slider_value())

    if globalPassLength == 0:
        globalPassLength = int(currentTtlNum.get() + currentTtlSymbol.get())
        lengthValLabel.configure(text="Current Value: " + str(globalPassLength))


# converts the "True/False" string stored within the radio buttons' variable into a boolean. This is then stored in the
# global variable for use in the password generator
def get_booleans():
    try:
        global globalCapBool, globalLowerBool, globalNumsBool, globalSymBool

        globalCapBool = eval(capitalRadioVar.get())
        globalLowerBool = eval(lowerRadioVar.get())
        globalNumsBool = eval(numberRadioVar.get())
        globalSymBool = eval(symbolRadioVar.get())
    except SyntaxError:
        raise passExcept.UnsetButtonError


# gathers the requested total nums/symbols and updates the corresponding global variable if the corresponding boolean
# variable was True. If not, it sets the total to zero, sends a warning, and updates the global variable to zero.
def get_minimums():
    global globalTtlNums, globalTtlSyms

    if not globalNumsBool:
        showinfo(title="Notice", message="Due to 'Include Numbers?' being false, you will have no numeric characters")
        currentTtlNum.set(0)
        globalTtlNums = int('{:.0f}'.format(currentTtlNum.get()))
    else:
        globalTtlNums = int('{:.0f}'.format(currentTtlNum.get()))

    if not globalSymBool:
        showinfo(title="Notice", message="Due to 'Include Symbols?' being false, you will have no special symbols")
        currentTtlSymbol.set(0)
        globalTtlSyms = int('{:.0f}'.format(currentTtlSymbol.get()))
    else:
        globalTtlSyms = int('{:.0f}'.format(currentTtlSymbol.get()))


# returns the value of the length scale
def get_slider_value():
    return '{: .0f}'.format(lengthSliderVar.get())


# When the length scale is interacted with, its minimum value is set to be the sum of the total numbers and symbols.
# Then, the length scale's label is updated to the value the scale is currently on
def slider_changed(event):
    lengthSlider.configure(from_=currentTtlNum.get() + currentTtlSymbol.get())
    lengthValLabel.configure(text="Current Value: " + str(get_slider_value()))


# WIDGETS
SUBGRID_COLUMN = 0

titleLabel = ttk.Label(root, text="Your Random Password is...", font=("Times New Roman", 11, "bold"))
titleLabel.grid(column=0, row=0, columnspan=2, padx=5, pady=5)

# FIXME: insert however the password will be displayed here
# Password's text widget
passText = tk.Text(root, height=1)
passText.grid(column=0, row=1, columnspan=2)

# Capital label and radio button label frame
capitalLabel = ttk.Label(root, text="Include Capitals?", font=("Times New Roman", 13))
capitalLabel.grid(column=0, row=2, sticky=tk.W, padx=100)

capitalRadioLf = ttk.LabelFrame(root, text="Ex. A, F, G, etc")
capitalRadioLf.grid(column=1, row=2, padx=50, pady=20)

capitalRadioVar = tk.StringVar()
for choice in RADIO_CHOICE:
    # create the radio buttons
    radio = ttk.Radiobutton(capitalRadioLf, text=choice, value=choice, variable=capitalRadioVar)
    radio.grid(column=SUBGRID_COLUMN, row=0, ipadx=10, ipady=10)
    SUBGRID_COLUMN += 1


# Lowercase label and radio button label frame
lowercaseLabel = ttk.Label(root, text="Include Lowercase?", font=("Times New Roman", 13))
lowercaseLabel.grid(column=0, row=3, sticky=tk.W, padx=100)

lowercaseRadioLf = ttk.LabelFrame(root, text="Ex. i, o, r, etc")
lowercaseRadioLf.grid(column=1, row=3, padx=50, pady=10)

lowerRadioVar = tk.StringVar()
for choice in RADIO_CHOICE:
    # create the radio buttons
    radio = ttk.Radiobutton(lowercaseRadioLf, text=choice, value=choice, variable=lowerRadioVar)
    radio.grid(column=SUBGRID_COLUMN, row=0, ipadx=10, ipady=10)
    SUBGRID_COLUMN += 1


# Numbers label and radio button label frame
numberLabel = ttk.Label(root, text="Include Numbers?", font=("Times New Roman", 13))
numberLabel.grid(column=0, row=4, sticky=tk.W, padx=100)

numberRadioLf = ttk.LabelFrame(root, text="Numbers 0-9")
numberRadioLf.grid(column=1, row=4, padx=50, pady=10)

numberRadioVar = tk.StringVar()
for choice in RADIO_CHOICE:
    # create the radio buttons
    radio = ttk.Radiobutton(numberRadioLf, text=choice, value=choice, variable=numberRadioVar)
    radio.grid(column=SUBGRID_COLUMN, row=0, ipadx=10, ipady=10)
    SUBGRID_COLUMN += 1

# FIXME: make sure spinboxes trigger a notification window if the input value is above 12, then reset the input value
# FIXME: to 12.
# Symbols label and radio button label frame
symbolLabel = ttk.Label(root, text="Include Symbols?", font=("Times New Roman", 13))
symbolLabel.grid(column=0, row=5, sticky=tk.W, padx=100)

symbolRadioLf = ttk.LabelFrame(root, text="Ex. &, #, $, etc")
symbolRadioLf.grid(column=1, row=5, padx=50, pady=10)

symbolRadioVar = tk.StringVar()
for choice in RADIO_CHOICE:
    # create the radio buttons
    radio = ttk.Radiobutton(symbolRadioLf, text=choice, value=choice, variable=symbolRadioVar)
    radio.grid(column=SUBGRID_COLUMN, row=0, ipadx=10, ipady=10)
    SUBGRID_COLUMN += 1


# TtlNum's label and spinbox
ttlNumLabel = ttk.Label(root, text="Total Numbers?", font=("Times New Roman", 13))
ttlNumLabel.grid(column=0, row=6, sticky=tk.W, padx=100)

currentTtlNum = tk.DoubleVar(value=0)
ttlNumSpinbox = ttk.Spinbox(root, from_=0, to=12, textvariable=currentTtlNum, wrap=True)
ttlNumSpinbox.grid(column=1, row=6, pady=10)


# TtlSymbol's label and spinbox
ttlSymbolLabel = ttk.Label(root, text="Total Symbols?", font=("Times New Roman", 13))
ttlSymbolLabel.grid(column=0, row=7, sticky=tk.W, padx=100)

currentTtlSymbol = tk.DoubleVar(value=0)
ttlSymbolSpinbox = ttk.Spinbox(root, from_=0, to=12, textvariable=currentTtlSymbol, wrap=True)
ttlSymbolSpinbox.grid(column=1, row=7, pady=10)


# Label and Slider for the length of the password
lengthLabel = ttk.Label(text="Password Length", font=("Times New Roman", 13))
lengthLabel.grid(column=0, row=8, sticky=tk.W, padx=100)

lengthSliderLf = ttk.LabelFrame(root)
lengthSliderLf.grid(column=1, row=8)

lengthSliderVar = tk.DoubleVar()
lengthSlider = ttk.Scale(lengthSliderLf, from_=0, to=35,
                         variable=lengthSliderVar, command=slider_changed)
lengthSlider.grid(column=0, row=0, sticky=tk.N)

lengthValLabel = ttk.Label(lengthSliderLf, text="Current Value: ")
lengthValLabel.grid(column=0, row=1, sticky=tk.N)


# FIXME: finish the functionality of the generate password button
genPassBttn = ttk.Button(root, text="Generate Password", command=generate_password)
genPassBttn.grid(column=0, row=9, sticky=tk.S, columnspan=2, ipadx=15, ipady=15)

# FIXME: Save Generated passwords so that they arte note generated twice. Hash passwords when they are saved so they cant be accessed
# FIXME: MD5, SHA, Hashing 
# EVENT LOOP
root.mainloop()