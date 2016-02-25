'''
Created on Feb 22, 2016

@author: zeljko.gavrilovic
'''
import tkinter as tk
import tkinter.scrolledtext as sc
import tkinter.ttk as ttk

class EnvironmentVariableEditor(ttk.Frame):

    def __init__(self, root, parent, name="", value="", scope="user", mode="new"):
        ttk.Frame.__init__(self, root)
        self.root = root
        self.parent = parent
        self.mode = mode
        
        self.create_gui()
        self.refresh(name, value, mode, scope);
                
        appSize = (600, 400)
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()

        x = w / 2 - appSize[0] / 2
        y = h / 2 - appSize[1] / 2
        self.root.geometry("%dx%d+%d+%d" % (appSize + (x, y)))
        self.root.update_idletasks()  # Force geometry update

    def create_gui(self):
        separatorLabel = ttk.Label(self, text="Enter the new environment variable", anchor="nw")
        separatorLabel.grid(column=0, row=0, sticky="EW", columnspan=6)
        
        self.nameLabel = ttk.Label(self, text="Name", anchor="nw")
        self.nameLabel.grid(column=0, row=1, sticky='EW')
        
        self.nameModel = tk.StringVar()
        self.nameEntry = ttk.Entry(self, textvariable=self.nameModel)
        self.nameEntry.grid(column=1, row=1, sticky='EW', columnspan=5)
        
        self.valueLabel = ttk.Label(self, text="Value", anchor="nw")
        self.valueLabel.grid(column=0, row=2, sticky='NW')
        
        #self.valueModel = tk.StringVar()
        self.txt = sc.ScrolledText(self, undo=True)
        self.txt.grid(column=1, row=2, sticky="EWNS", columnspan=5)
        
        self.scopeModel = tk.IntVar()        
        self.scopeCheckbox = ttk.Checkbutton(self, text="System", variable=self.scopeModel,
                 onvalue=1, offvalue=0)
        self.scopeCheckbox.grid(column=1, row=3, sticky='W')
        
        button = ttk.Button(self, text="Save", command=self.save)
        button.grid(column=2, row=4, sticky='WE')

        button = ttk.Button(self, text="New", command=self.new)
        button.grid(column=3, row=4, sticky='WE')

        button = ttk.Button(self, text="Cancel", command=self.quit)
        button.grid(column=4, row=4, sticky='WE')

        button = ttk.Button(self, text="Close", command=self.quit)
        button.grid(column=5, row=4, sticky='WE')

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=7)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=0)
        self.grid_columnconfigure(5, weight=0)
    
    def refresh(self, name, value, mode="new", scope="user"):
        self.nameModel.set(name)
        
        self.txt.configure(state='normal')
        self.txt.delete("0.0", "end")
        self.txt.insert("0.0", value)
        
        if scope == "user":
            self.scopeModel.set(0)
        else: 
            self.scopeModel.set(1)
        
        if mode == "edit":
            self.nameEntry.configure(state='disabled')
            self.scopeCheckbox.configure(state='disabled')
        else:
            self.nameEntry.configure(state='normal')
            if  not self.parent.restricted:
                self.scopeCheckbox.configure(state='normal')
            else: 
                self.scopeCheckbox.configure(state='disabled')        
            
    def new(self):
        self.refresh("", "")
            
    def save(self):
        name = self.nameModel.get().strip()
        value = self.txt.get(1.0, "end").strip()
        valid = (len(name) > 0) and (len(value) > 0)
        if not valid:
            tk.messagebox.showinfo("Empty entry not allowed", "Please fill both the name and the value of the environment variable")
            return
        
        if(self.scopeModel.get() == 0):
            self.parent.winUserEnvVarService.addEnvVariable(name, value)
#             self.nameEntry.configure(state='disabled')
#             self.scopeCheckbox.configure(state='disabled')
            self.refresh(name, value, "edit", "user")
            self.parent.refresh()
        else:
            try:
                self.parent.winSystemUserEnvVarService.addEnvVariable(name, value)
#                 self.nameEntry.configure(state='disabled')
#                 self.scopeCheckbox.configure(state='disabled')
                self.refresh(name, value, "edit", "system")
                self.parent.refresh()
            except WindowsError:
                tk.messagebox.showwarning("Add/update Environment variable", "Cannot persist changes. You need to open the application in the admin mode in order to change the system environment variables..."
        )

    def quit(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    EnvironmentVariableEditor(root, None).pack(side="top", fill="both", expand=True)
    root.mainloop()