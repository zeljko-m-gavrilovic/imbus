import Tkinter as tk
from tkFileDialog import askopenfilename
from ScrolledText import ScrolledText


class ImportGui(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.populate()

    def populate(self):
        # create a Text widget with a Scrollbar attached
        self.txt = ScrolledText(self, undo=True)
        # self.txt['font'] = ('consolas', '12')
        # self.txt.pack(expand=True, fill='both')
        self.txt.grid(column=0, row=0, sticky="EW", columnspan=4)

        button = tk.Button(self, text=u"Import", command=self.openFile)
        button.grid(column=0, row=1, sticky='WE')

        button = tk.Button(self, text=u"Clear content", command=self.clearContent)
        button.grid(column=1, row=1, sticky='WE')

        button = tk.Button(self, text=u"Save", command=self.save)
        button.grid(column=2, row=1, sticky='WE')

        button = tk.Button(self, text=u"Close", command=self.quit)
        button.grid(column=3, row=1, sticky='WE')

        #self.grid_columnconfigure(0, weight=9)
        self.grid_rowconfigure(0, weight=9)
        self.grid_rowconfigure(1, weight=1)
        #self.grid_columnconfigure(1, weight=1)


    def clearContent(self):
        self.txt.delete("0.0", "end")

    def openFile(self):
        filename = askopenfilename(parent=self)
        if filename:
            f = open(filename, "r")
            content = f.read()
            print content
            self.clearContent();
            self.txt.insert("0.0", content)
            f.close()
    def save(self):
        pass

    def quit(self):
         self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    ImportGui(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
