#
# Starter GUI 2
#

import tkinter as tk

window = tk.Tk()
window.title("GUI of the month")

greeting = tk.Label(text="Hello Tkinter").grid(column=0, row=0) # W/O pack

frm_button = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_quit = tk.Button(frm_button, text="Quit", command=window.destroy)

btn_quit.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

frm_button.grid(row=1, column=1, sticky="ns")

#greeting.pack()

window.mainloop()
