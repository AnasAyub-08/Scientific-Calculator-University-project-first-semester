import customtkinter as ctk
import math

# Base canvas setup for the app
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Scientific Calculator")
root.geometry("340x456")
root.resizable(False, False)

try:
    root.iconbitmap("calculator-24.ico")
except:
    pass

# Expression Display (Displaying the expression being typed)
expression = ""
expression_text = ""
expression_var = ctk.StringVar()

expression_frame = ctk.CTkFrame(root, height=25, width=320, fg_color="transparent")
expression_frame.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=10, pady=(10, 5))
expression_frame.grid_propagate(False)

expression_canvas = ctk.CTkCanvas(expression_frame, height=25, width=320, bg="#242424", bd=0, highlightthickness=0)
expression_canvas.pack(fill="both", expand=True)

text_id = expression_canvas.create_text(
    315, 12,
    anchor="e",
    font=("Consolas", 14),
    fill="#A0A0A0",
    text=""
)

def update_expression_display(text):
    global expression_text
    expression_text = text
    expression_canvas.itemconfig(text_id, text=text)
    bbox = expression_canvas.bbox(text_id)
    if bbox:
        text_width = bbox[2] - bbox[0]
        x_offset = max(0, text_width - 310)
        expression_canvas.xview_moveto(x_offset / text_width if text_width > 0 else 0)

# Display for the result after calculation
result_var = ctk.StringVar()

result_entry = ctk.CTkEntry(
    root,
    textvariable=result_var,
    justify="right",
    font=("Consolas", 28),
    width=320,
    height=50
)
result_entry.grid(row=1, column=0, columnspan=5, pady=(0, 10), padx=10)
result_entry.configure(state="readonly")

# Function for inserting functions and numbers 
def insert_function(symbol):
    global expression
    func_map = {
        "π": str(math.pi),
        "e": str(math.e),
        "x²": "**2",
        "⅟x": "**-1",
        "²√x": "**0.5",
        "|x|": "abs(",
        "exp": "math.exp(",
        "mod": "%",
        "n!": "math.factorial(",
        "xʸ": "**",
        "10ˣ": "10**",
        "log": "math.log10(",
        "ln": "math.log(",
    }
    expression += func_map.get(symbol, symbol)
    update_expression_display(expression)

# Function for updating the expression when a button is pressed
def update_expression(value):
    global expression
    expression += value
    update_expression_display(expression)

# Function for clearing the expression and result
def clear():
    global expression
    expression = ""
    update_expression_display(expression)
    result_var.set("")

# Function for backspacing the last character in the expression
def backspace():
    global expression
    expression = expression[:-1]
    update_expression_display(expression)

# Function for calculating the result of the expression (Also handles errors)
def calculate():
    global expression
    try:
        # Close all unclosed functions like abs( or math.log(
        open_parens = expression.count("(")
        close_parens = expression.count(")")
        expression += ")" * (open_parens - close_parens)

        result = eval(expression)
        result_var.set(result)
    except:
        result_var.set("Error")
    update_expression_display(expression)

# Function for toggling the sign of the last number in the expression
# (e.g., changing 5 to -5 or -5 to 5)
def toggle_sign():
    global expression
    if expression and expression[-1].isdigit():
        # Add minus sign to the beginning or toggle it
        if expression.startswith("-"):
            expression = expression[1:]
        else:
            expression = "-" + expression
    update_expression_display(expression)

# Creating the basic layout of the buttons for the calculator
buttons = [
    ["2ⁿᵈ", "π", "e", "C", "⌫"],
    ["x²", "⅟x", "|x|", "exp", "mod"],
    ["²√x", "(", ")", "n!", "÷"],
    ["xʸ", "7", "8", "9", "x"],
    ["10ˣ", "4", "5", "6", "-"],
    ["log", "1", "2", "3", "+"],
    ["ln", "+/-", "0", ".", "="]
]

symbol_map = {"÷": "/", "x": "*"}

# Creating the buttons and assigning functions to them
for i, row in enumerate(buttons):
    for j, btn_text in enumerate(row):
        if btn_text == "":
            continue
        if btn_text == "C":
            action = clear
        elif btn_text == "⌫":
            action = backspace
        elif btn_text == "=":
            action = calculate
        elif btn_text == "+/-":
            action = toggle_sign
        elif btn_text in "0123456789." or btn_text in "()":
            action = lambda x=btn_text: update_expression(x)
        elif btn_text in symbol_map:
            action = lambda x=symbol_map[btn_text]: update_expression(x)
        else:
            action = lambda x=btn_text: insert_function(x)

        ctk.CTkButton(
            master=root,
            text=btn_text,
            command=action,
            width=60,
            height=45,
            font=("Consolas", 16)
        ).grid(row=i+2, column=j, padx=1, pady=3)

root.mainloop()
