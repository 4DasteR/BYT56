from typing import Callable, Tuple
import tkinter as tk
from tkinter import ttk

class Handler:
    def __init__(self, operation: str, callback: Callable[[float, float], float], next = None):
        self.operation = operation
        self.callback = callback
        self.next = next

    def handle(self, operation: str, values: Tuple[float, float]) -> float | str | None:
        if operation == self.operation: return self.callback(*values)
        return self.next.handle(operation, values) if self.next is not None else None

def division(x: float, y: float):
    if y == 0: return 'Cannot divide by zero!'
    return x / y

div = Handler('/', division)
mul = Handler('*', lambda x, y: x * y, div)
sub = Handler('-', lambda x, y: x - y, mul)
add = Handler('+', lambda x, y: x + y, sub)

class CalculatorApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Simple Calculator")
        self.window.resizable(False, False)
        
        self.number_x_entry = tk.Entry(self.window, width=10)
        self.number_x_entry.grid(row=0, column=0, padx=10, pady=10)
        self.number_x_entry.config(validate="key", validatecommand=(self.window.register(self.validate_entry), '%P'))

        self.operations = ['+', '-', '*', '/']
        self.operation_combobox = ttk.Combobox(self.window, values=self.operations, state="readonly", width=5)
        self.operation_combobox.set(self.operations[0])
        self.operation_combobox.grid(row=0, column=1, padx=10, pady=10)
    
        self.number_y_entry = tk.Entry(self.window, width=10)
        self.number_y_entry.grid(row=0, column=2, padx=10, pady=10)
        self.number_y_entry.config(validate="key", validatecommand=(self.window.register(self.validate_entry), '%P'))

        self.calculate_button = tk.Button(self.window, text="=", command=self.calculate)
        self.calculate_button.grid(row=0, column=3, padx=10, pady=10)

        self.result_var = tk.StringVar()
        self.result_var.set("")
        self.result_entry = tk.Entry(self.window, textvariable=self.result_var, state="readonly", width=20)
        self.result_entry.grid(row=0, column=4, padx=10, pady=10)
        
        self.window.mainloop()
        
    def validate_entry(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False
        
    def calculate(self):
        try:
            x = float(self.number_x_entry.get())
            operation = self.operation_combobox.get()
            y = float(self.number_y_entry.get())

            result = add.handle(operation, (x, y))
            self.result_var.set(result)
        except ValueError:
            self.result_var.set("Invalid input")

if __name__ == "__main__":
    CalculatorApp()