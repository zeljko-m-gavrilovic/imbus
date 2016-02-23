'''
Created on Feb 22, 2016

@author: zeljko.gavrilovic
'''
from tkFileDialog import askopenfilename

import Tkinter as tk
import tkMessageBox
from ScrolledText import ScrolledText


# from WinRegistryService import WinUserRegistryService
# from WinRegistryService import WinRegistryService 
class EnvironmentVariableGui(tk.Frame):
    def __init__(self, root, parent, name="", value="", scope="user", mode="new"):
        tk.Frame.__init__(self, root)
        self.root = root
        self.parent = parent
        
        self.nameModel = tk.StringVar()
        self.nameModel.set(name)
        
        self.valueModel = tk.StringVar()
        self.valueModel.set(value)
        
        self.scopeModel = tk.IntVar()
        if scope == "user":
            self.scopeModel.set(0)
        else: 
            self.scopeModel.set(1)
        
        self.mode = mode
        self.populate()
                
        appSize = (600, 400)
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()

        x = w / 2 - appSize[0] / 2
        y = h / 2 - appSize[1] / 2
        self.root.geometry("%dx%d+%d+%d" % (appSize + (x, y)))
        self.root.update_idletasks()  # Force geometry update

    #def pathNotification(self, value):
    #    self.notification = "Please note that you can't edit the PATH environment variable like the other ones. You can only append a value to it because it is much safer not to destroy something ...\n\nPATH=" + value
        
    def populate(self):
        separatorLabel = tk.Label(self, text=u"Enter the new environment variable",
                                  anchor="nw", fg="white", bg="gray")
        separatorLabel.grid(column=0, row=0, sticky="EW", columnspan=6)
        
        self.nameLabel = tk.Label(self, text="Name", anchor="nw")
        self.nameLabel.grid(column=0, row=1, sticky='EW')
        
        self.nameEntry = tk.Entry(self, textvariable=self.nameModel)
        self.nameEntry.grid(column=1, row=1, sticky='EW', columnspan=5)
        
        self.valueLabel = tk.Label(self, text="Value", anchor="nw")
        self.valueLabel.grid(column=0, row=2, sticky='NW')
        
        self.txt = ScrolledText(self, undo=True)
        self.txt.grid(column=1, row=2, sticky="EWNS", columnspan=5)
        self.txt.configure(state='normal')
        self.txt.delete("0.0", "end")
        self.txt.insert("0.0", self.valueModel.get())
        #self.txt.configure(state='disabled')
        
        self.scopeCheckbox = tk.Checkbutton(self, text="System", variable=self.scopeModel,
                 onvalue=1, offvalue=0)
        self.scopeCheckbox.grid(column=1, row=3, sticky='W')
        
        button = tk.Button(self, text=u"Save", command=self.save)
        button.grid(column=2, row=4, sticky='WE')

        button = tk.Button(self, text=u"New", command=self.new)
        button.grid(column=3, row=4, sticky='WE')

        button = tk.Button(self, text=u"Cancel", command=self.quit)
        button.grid(column=4, row=4, sticky='WE')

        button = tk.Button(self, text=u"Close", command=self.quit)
        button.grid(column=5, row=4, sticky='WE')
        
        if self.mode == "edit":
            self.nameEntry.configure(state='disabled')
            self.scopeCheckbox.configure(state='disabled')

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=7)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(5, weight=1)
            
    def new(self):
        self.nameModel.set("")
        self.nameEntry.configure(state='normal')
        self.txt.delete("0.0", "end")
        self.scopeModel.set(0)
        self.txt.configure(state='normal')
        self.scopeCheckbox.configure(state='normal')
            
    def save(self):
        name = self.nameModel.get()
        value = self.txt.get(1.0, "end")
        if(self.scopeModel.get() == 0):
            self.parent.winUserRegistryService.addEnvVariable(name, value)
            self.nameEntry.configure(state='disabled')
            self.scopeCheckbox.configure(state='disabled')
            self.parent.refresh()
        else:
            try:
                self.parent.winSystemRegistryService.addEnvVariable(name, value)
                self.nameEntry.configure(state='disabled')
                self.scopeCheckbox.configure(state='disabled')
                self.parent.refresh()
            except WindowsError:
                tkMessageBox.showwarning("Add/update Environment variable", "Cannot persist changes. You need to open the application in the admin mode in order to change the system environment variables..."
        )

    def quit(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    EnvironmentVariableGui(root, None).pack(side="top", fill="both", expand=True)
    root.mainloop()
