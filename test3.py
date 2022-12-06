import tkinter as tk

root = tk.Tk()

def get_geometry():
    top = tk.Toplevel()
    top.geometry(f"+{root.winfo_x()}+{root.winfo_y()}")
    top.title("This is new toplevel")

tk.Button(root,text="Spawn new window",command=get_geometry).pack()

root.mainloop()