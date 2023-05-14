from tkinter import *
from tkinter import ttk
root = Tk()
label = ttk.Label(root, text="Starting...")
label.grid()
label.bind('<Enter>', lambda e: label.configure(text='Moved␣mouse␣inside'))
label.bind('<Leave>', lambda e: label.configure(text='Moved␣mouse␣outside'))
label.bind('<ButtonPress-1>', lambda e: label.configure(text='Clicked␣left␣mouse␣button'))
label.bind('<3>', lambda e: label.configure(text='Clicked␣right␣mouse␣button'))
label.bind('<Double-1>', lambda e: label.configure(text='Double␣clicked'))
label.bind('<B3-Motion>', lambda e: label.configure(text='right␣button␣drag␣to␣%d,%d' % (e.x, e.y)))
root.mainloop()
