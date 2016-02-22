'''
Created on Feb 22, 2016

@author: zeljko.gavrilovic
'''
from tkFileDialog import askopenfilename

import Tkinter as tk
from WinRegistryService import WinRegistryService


#from WinRegistryService import WinRegistryService 
class AddNewGui(tk.Frame):
    def __init__(self, root, parent, name="", value=""):
        tk.Frame.__init__(self, root)
        self.root = root
        self.parent = parent
        
        self.nameModel = tk.StringVar()
        self.nameModel.set(name)
        self.valueModel = tk.StringVar()
        self.valueModel.set(value)
        
        self.populate()
                
        appSize = (600, 400)
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()

        x = w / 2 - appSize[0] / 2
        y = h / 2 - appSize[1] / 2
        self.root.geometry("%dx%d+%d+%d" % (appSize + (x, y)))
        self.root.update_idletasks()  # Force geometry update

    def populate(self):
        separatorLabel = tk.Label(self.root, text=u"Enter the new environment variable",
                                  anchor="w", fg="white", bg="gray")
        separatorLabel.grid(column=0, row=0, sticky="W", columnspan=4)
        separatorLabel.pack(fill="x")
        
        self.nameLabel = tk.Label(self, text="Name", anchor="nw")
        self.nameLabel.grid(column=0, row=1, sticky='EW')
        
        self.nameEntry = tk.Entry(self, textvariable=self.nameModel)
        self.nameEntry.grid(column=1, row=1, sticky='EW', columnspan=4)
        
        
        self.valueLabel = tk.Label(self, text="Value", anchor="nw")
        self.valueLabel.grid(column=0, row=2, sticky='EW')
        
        self.valueEntry = tk.Entry(self, textvariable=self.valueModel)
        self.valueEntry.grid(column=1, row=2, sticky='EW', columnspan=4)
        
        button = tk.Button(self, text=u"Save", command=self.save)
        button.grid(column=2, row=4, sticky='WE')

        button = tk.Button(self, text=u"Cancel", command=self.quit)
        button.grid(column=3, row=4, sticky='WE')

        button = tk.Button(self, text=u"Close", command=self.quit)
        button.grid(column=4, row=4, sticky='WE')

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=7)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

    def clearContent(self):
        self.txt.delete("0.0", "end")

    def openFile(self):
        filename = askopenfilename(parent=self)
        if filename:
            f = open(filename, "r")
            content = f.read()
            print(content)
            self.clearContent();
            self.txt.insert("0.0", content)
            f.close()
    def save(self):
        name = self.nameModel.get()
        value = self.valueModel.get()
        self.parent.winRegistryService.addEnvVariable(name, value)
        self.parent.refresh()

    def quit(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    AddNewGui(root, None).pack(side="top", fill="both", expand=True)
    root.mainloop()