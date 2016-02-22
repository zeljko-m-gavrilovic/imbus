

from AddNewVariableGui import AddNewGui
from ImportGui import ImportGui
import Tkinter as tk
from WinRegistryService import WinUserRegistryService


class Application(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.winUserRegistryService = WinUserRegistryService()
        self.winSystemRegistryService = WinSystemRegistryService()
        self.populate()
    def refresh(self):
        if self.header:
            self.header.destroy()
        if self.tableCanvas:
            self.tableCanvas.destroy()
        if self.buttons:
            self.buttons.destroy()
        self.populate()    
    def populate(self):

        self.envVariables = self.winUserRegistryService.getAllEnvVariable()
        try:
            systemVars = self.winSystemRegistryService.getAllEnvVariable()
            self.envVariables.extend(systemVars)
        except EnvironmentError:
            pass


        # header panel
        self.header = tk.Canvas(root)
        separatorLabel = tk.Label(self.header, text=u"Environment variables",
                                  anchor="nw", fg="white", bg="gray")
        separatorLabel.pack(fill="x")
        self.header.pack(fill="x")
        
        # table panel        
        self.tableCanvas = tk.Canvas(root)
        self.tableCanvas.pack(fill="both", expand=True)
        self.tableFrame = tk.Frame(self.tableCanvas, background="yellow")
        
        self.canvas = tk.Canvas(self.tableCanvas, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(self.tableCanvas, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self._frame_id = self.canvas.create_window(0, 0, window=self.frame, anchor="nw")
        self.canvas.bind("<Configure>", self.onFrameResize)

        for i in range(len(self.envVariables)):
            cellTypeModel = tk.StringVar()
            cellTypeModel.set(self.envVariables[i][0])
            typeCell = tk.Entry(self.frame, textvariable=cellTypeModel)
            typeCell.grid(row=i + 1, column=0, sticky='EW')

            cellNameModel = tk.StringVar()
            cellNameModel.set(self.envVariables[i][1])
            nameCell = tk.Entry(self.frame, textvariable=cellNameModel)
            nameCell.grid(row=i + 1, column=1, sticky='EW')

            cellValueModel = tk.StringVar()
            cellValueModel.set(self.envVariables[i][2])
            valueCell = tk.Entry(self.frame, textvariable=cellValueModel)
            valueCell.grid(row=i + 1, column=2, sticky='EW')
            # self.cells.append((nameCell, valueCell))
            
            editButton = tk.Button(self.frame, text=u"Edit", command=lambda: self.edit(self.envVariables[i][1], self.envVariables[i][2]))
            editButton.grid(row=i + 1, column=3, sticky='EW')
            
            removeButton = tk.Button(self.frame, text=u"Remove", command=lambda: self.remove(self.envVariables[i][1]))
            removeButton.grid(row=i + 1, column=4, sticky='EW')

            self.frame.grid_columnconfigure(0, weight=1)
            self.frame.grid_columnconfigure(1, weight=2)
            self.frame.grid_columnconfigure(2, weight=6)
            self.frame.grid_columnconfigure(3, weight=1)
            self.frame.grid_columnconfigure(4, weight=1)
            
        # buttons panel
        self.buttons = tk.Canvas(root)
        importButton = tk.Button(self.buttons, text=u"Import", command=self.importEnv)
        importButton.pack(side="right")
        
        addButton = tk.Button(self.buttons, text=u"Add new", command=self.addNew)
        addButton.pack(side="right")
        
        self.buttons.pack(fill="x")
        
    def onFrameResize(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.itemconfig(self._frame_id, height=event.height, width=event.width)

    def OnButtonClick(self):
        self.envVariables.append(("SYSTEM", self.nameModel.get(), self.valueModel.get()))
        self.populate();

        self.separatorModel.set(self.valueModel.get() + " (You clicked the button)")
        self.nameEntry.focus_set()
        self.nameEntry.selection_range(0, tk.END)
        self.nameModel.set("")
        self.valueModel.set("")

    def OnPressEnter(self, event):
        self.separatorModel.set(self.valueModel.get() + " (You pressed ENTER)")
        self.valueEntry.focus_set()
        self.valueEntry.selection_range(0, tk.END)

    def addNew(self):
        newWindow = tk.Toplevel(self)
        AddNewGui(newWindow, self).pack(side="top", fill="both", expand=True)
        self.after(1, lambda: newWindow.focus_force())
    
    def edit(self, name, value):
        newWindow = tk.Toplevel(self)
        AddNewGui(newWindow, self, name, value).pack(side="top", fill="both", expand=True)
        self.after(1, lambda: newWindow.focus_force())
    
    def remove(self, name):
        self.winRegistryService.removeEnvVariable(name)
        self.refresh()
        
    def importEnv(self):
        newWindow = tk.Toplevel(self)
        ImportGui(newWindow, self).pack(side="top", fill="both", expand=True)
        self.after(1, lambda: newWindow.focus_force())


if __name__ == "__main__":
    root = tk.Tk()

    appSize = (800, 600)
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()

    x = w / 2 - appSize[0] / 2
    y = h / 2 - appSize[1] / 2
    root.geometry("%dx%d+%d+%d" % (appSize + (x, y)))
    root.update_idletasks()  # Force geometry update

    Application(root)  # .pack(side="top", fill="both", expand=True)
    root.mainloop()
