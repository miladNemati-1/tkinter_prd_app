from tkinter import *
from customtkinter import *
import tkinter as tk
root = tk.Tk() #create the tkinter window
frame1 = Frame(root, bg='blue', width=100, height=100)
frame1.pack(pady=10)

frame2 = Frame(root, bg='red', width=100, height=100)
frame2.pack(pady=10, padx=(10, 0))

root.mainloop()