from ScrolledText import ScrolledText
from tkFileDialog import askopenfilename

import Tkinter as tk


class ImportGui(tk.Frame):
    def __init__(self, root, parent):
        tk.Frame.__init__(self, root)
        self.root = root
        self.parent = parent
        self.populate()
        
        appSize = (600, 400)
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()

        x = w / 2 - appSize[0] / 2
        y = h / 2 - appSize[1] / 2
        self.root.geometry("%dx%d+%d+%d" % (appSize + (x, y)))
        self.root.update_idletasks()  # Force geometry update


    def populate(self):
        separatorLabel = tk.Label(self.root, text=u"Content to be imported",
                                  anchor="w", fg="white", bg="gray")
        separatorLabel.grid(column=0, row=0, sticky="W", columnspan=4)
        separatorLabel.pack(fill="x")
        
        # create a Text widget with a Scrollbar attached
        self.txt = ScrolledText(self, undo=True)
        # self.txt['font'] = ('consolas', '12')
        # self.txt.pack(expand=True, fill='both')
        self.txt.grid(column=0, row=1, sticky="EWNS", columnspan=4)

        button = tk.Button(self, text=u"From file...", command=self.openFile)
        button.grid(column=0, row=2, sticky='WE')

        button = tk.Button(self, text=u"Clear content", command=self.clearContent)
        button.grid(column=1, row=2, sticky='WE')

        button = tk.Button(self, text=u"Save", command=self.save)
        button.grid(column=2, row=2, sticky='WE')

        button = tk.Button(self, text=u"Close", command=self.quit)
        button.grid(column=3, row=2, sticky='WE')

        #self.grid_columnconfigure(0, weight=9)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)


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
        content = self.txt.get(1.0, "end")
        lines = [s.strip() for s in content.splitlines()]
        for line in lines:
            name, value = line.split("=")
            if name and value:
                self.parent.winRegistryService.addEnvVariable(name, value)
        self.parent.refresh()        

    def quit(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    ImportGui(root, None).pack(side="top", fill="both", expand=True)
    root.mainloop()