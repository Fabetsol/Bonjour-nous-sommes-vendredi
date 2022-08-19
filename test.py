import tkinter as tk
import tkinter.messagebox as mb

root = tk.Tk()
root.title("Height calculator tool")
root.grid()

space1 = tk.Label(root).grid(row=0,column=0)
space2 = tk.Label(root).grid(row=2, column=0)

label1 = tk.Label(root, text="Input your height ").grid(row=1,column=0)
entry = tk.Entry(root); entry.grid(row=1, column=1)
label2 = tk.Label(root, text="cm").grid(row=1,column=2)

def solve():
    global entry
    mb.showinfo("Result", f"Your height is {entry.get()} cm!")
    
button = tk.Button(root, text="Solve", command=solve).grid(row=3, column=2)

root.mainloop()