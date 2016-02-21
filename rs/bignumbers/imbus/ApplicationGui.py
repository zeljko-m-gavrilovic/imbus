import Tkinter as tk

from ImportGui import ImportGui


class Example(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.canvas = tk.Canvas(root, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self._frame_id = self.canvas.create_window(0, 0, window=self.frame, anchor="nw")
        self.canvas.bind("<Configure>", self.onFrameResize)

        self.envVariables = [("system", "PYTHON_HOME", "c:\\dev\python27"),
                             ("system", "JAVA_HOME", "c:\\dev\java8"),
                             ("system", "MYSQL_HOME", "c:\\dev\mysql5"),
                             ("system", "JAVA_HOME", "c:\\dev\java8"),
                             ("system", "MYSQL_HOME", "c:\\dev\mysql5"),
                             ("system", "JAVA_HOME", "c:\\dev\java8"),
                             ("system", "MYSQL_HOME", "c:\\dev\mysql5"),
                             ("system", "JAVA_HOME", "c:\\dev\java8"),
                             ("system", "MYSQL_HOME", "c:\\dev\mysql5"),
                             ("system", "JAVA_HOME", "c:\\dev\java8"),
                             ("system", "MYSQL_HOME", "c:\\dev\mysql5"),
                             ("system", "JAVA_HOME", "c:\\dev\java8"),
                             ("system", "MYSQL_HOME", "c:\\dev\mysql5"),
                             ("system", "JAVA_HOME", "c:\\dev\java8"),
                             ("system", "MYSQL_HOME", "c:\\dev\mysql5"),
                             ("system", "JAVA_HOME", "c:\\dev\java8"),
                             ("system", "MYSQL_HOME", "c:\\dev\mysql5"),
                             ("system", "JAVA_HOME", "c:\\dev\java8"),
                             ("system", "MYSQL_HOME", "c:\\dev\mysql5"),
                             ("system", "MVN_HOME", "c:\\dev\maven3")
                             ]

        self.populate()

    def populate(self):
        # self.nameModel = tk.StringVar()
        # self.nameModel.set(u"Enter name of the variable here.")
        # self.nameEntry = tk.Entry(self.frame, textvariable=self.nameModel)
        # self.nameEntry.grid(column=0, row=0, sticky='EW')
        # # self.nameEntry.bind("<Return>", self.OnPressEnter)
        #
        # self.valueModel = tk.StringVar()
        # self.valueModel.set(u"Enter the value of the variable here.")
        # self.valueEntry = tk.Entry(self.frame, textvariable=self.valueModel)
        # self.valueEntry.grid(column=1, row=0, sticky='EW')
        # self.valueEntry.bind("<Return>", self.OnPressEnter)

        button = tk.Button(self.frame, text=u"Add new", command=self.importEnv)
        button.grid(column=1, row=0, sticky='EW')

        button = tk.Button(self.frame, text=u"Import", command=self.importEnv)
        button.grid(column=2, row=0, sticky='EW')

        self.separatorModel = tk.StringVar()
        separatorLabel = tk.Label(self.frame, textvariable=self.separatorModel,
                                  anchor="w", fg="white", bg="gray")
        separatorLabel.grid(column=0, row=1, columnspan=3, sticky='EW')
        self.separatorModel.set(u"System environment variables")
        print "initialize method len(self.t)" + str(len(self.envVariables))

        for i in range(len(self.envVariables)):
            cellTypeModel = tk.StringVar()
            cellTypeModel.set(self.envVariables[i][0])
            typeCell = tk.Entry(self.frame, textvariable=cellTypeModel)
            typeCell.grid(row=i + 2, column=0, sticky='EW')

            cellNameModel = tk.StringVar()
            cellNameModel.set(self.envVariables[i][1])
            nameCell = tk.Entry(self.frame, textvariable=cellNameModel)
            nameCell.grid(row=i + 2, column=1, sticky='EW')

            cellValueModel = tk.StringVar()
            cellValueModel.set(self.envVariables[i][2])
            valueCell = tk.Entry(self.frame, textvariable=cellValueModel)
            valueCell.grid(row=i + 2, column=2, sticky='EW')
            # self.cells.append((nameCell, valueCell))

            self.frame.grid_columnconfigure(0, weight=1)
            self.frame.grid_columnconfigure(1, weight=8)
            self.frame.grid_columnconfigure(2, weight=1)

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

    def importEnv(self):
        newWindow = tk.Toplevel(self)
        # ImportGui(newWindow)
        ImportGui(newWindow).pack(side="top", fill="both", expand=True)
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

    Example(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
