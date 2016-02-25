import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd


class EnvironmentVariableImport(ttk.Frame):
    def __init__(self, root, parent):
        ttk.Frame.__init__(self, root)
        self.root = root
        self.parent = parent
        
        self.createGui()
        self.refresh()
        
        appSize = (600, 400)
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()

        x = w / 2 - appSize[0] / 2
        y = h / 2 - appSize[1] / 2
        self.root.geometry("%dx%d+%d+%d" % (appSize + (x, y)))
        self.root.update_idletasks()  # Force geometry update


    def createGui(self):
        separatorLabel = ttk.Label(self.root, text="Content to be imported", anchor="w")
        separatorLabel.grid(column=0, row=0, sticky="W", columnspan=6)
        separatorLabel.pack(fill="x")
        
        self.txt = tk.scrolledtext.ScrolledText(self, undo=True)
        self.txt.grid(column=0, row=1, sticky="EWNS", columnspan=6)
        
        self.scopeModel = tk.IntVar(0)
        self.scopeCheckbox = ttk.Checkbutton(self, text="System", variable=self.scopeModel,
                 onvalue=1, offvalue=0)
        self.scopeCheckbox.grid(column=0, row=2, sticky='W')

        button = ttk.Button(self, text="From file...", command=self.openFile)
        button.grid(column=2, row=3, sticky='E')

        button = ttk.Button(self, text="Clear content", command=self.clearContent)
        button.grid(column=3, row=3, sticky='E')

        button = ttk.Button(self, text="Save", command=self.save)
        button.grid(column=4, row=3, sticky='E')

        button = ttk.Button(self, text="Close", command=self.quit)
        button.grid(column=5, row=3, sticky='E')

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        
        self.grid_columnconfigure(2, weight=1)
    
    def refresh(self, content=""):
        self.txt.delete("0.0", "end")
        self.txt.insert("0.0", content)
        
        if self.parent.restricted:
            self.scopeCheckbox.configure(state='disabled')

    def clearContent(self):
        #self.txt.delete("0.0", "end")
        self.refresh()

    def openFile(self):
        filename = fd.askopenfilename(parent=self)
        if filename:
            with open(filename, "r") as f:
                content = f.read()
            self.refresh(content);    
    
    def save(self):
        content = self.txt.get(1.0, "end").strip()
        
        valid = len(content) > 0
        if not valid:
            tk.messagebox.showinfo("Empty content not allowed", "Empty content for the import is not allowed. Please add some environment variables.")
            return
        
        lines = [s.strip() for s in content.splitlines()]
        for line in lines:
            try :
                name, value = line.split("=")
            except ValueError:
                tk.messagebox.showinfo("Bad format or empty value", "Bad format or empty entries for the line {line}. Please use name=value format.".format(line=line))
                break
            
            name = name.strip()
            value = value.strip()
            if name and value:
                if self.scopeModel.get() == 0:
                    self.parent.winUserEnvVarService.addEnvVariable(name, value)
                else:
                    try:
                        self.parent.winSystemUserEnvVarService.addEnvVariable(name, value)
                    except WindowsError:
                        tk.messagebox.showwarning("Import environment variables", "Cannot persist changes. You need to open the application in the admin mode in order to change system environment variables...")
                        break    
        self.parent.refresh()
                
    def quit(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    EnvironmentVariableImport(root, None).pack(side="top", fill="both", expand=True)
    root.mainloop()