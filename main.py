import Tkinter as tk
import MainFrame


root = tk.Tk()

mf = MainFrame.MainFrame(root)
mf.pack(fill=tk.BOTH, expand=1)

root.update()
root.minsize(root.winfo_width(), root.winfo_height())

root.mainloop()