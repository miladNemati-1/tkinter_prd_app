import customtkinter
from tkinter import *

app = Tk()


tabview = customtkinter.CTkTabview(app)
tabview.pack(padx=20, pady=20)

tabview.add("tab 1")  # add tab at the end
tabview.add("tab 2")  # add tab at the end
tabview.set("tab 2")  # set currently visible tab

button_1 = customtkinter.CTkButton(tabview.tab("tab 1"), text="arshia")
button_1.pack(padx=20, pady=20)
app.mainloop()