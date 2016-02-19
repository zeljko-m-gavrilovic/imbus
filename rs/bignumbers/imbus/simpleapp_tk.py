#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter


class simpleapp_tk(Tkinter.Tk):
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.t = [("n1", "v1"), ("n2", "v2"), ("n3", "v3"), ("n4", "v4")]
        self.cells = []
        self.initialize()

    def initialize(self):
        self.grid()

        self.nameModel = Tkinter.StringVar()
        self.nameModel.set(u"Enter name of the variable here.")
        self.nameEntry = Tkinter.Entry(self, textvariable=self.nameModel)
        self.nameEntry.grid(column=0, row=0, sticky='EW')
        self.nameEntry.bind("<Return>", self.OnPressEnter)

        self.valueModel = Tkinter.StringVar()
        self.valueModel.set(u"Enter the value of the variable here.")
        self.valueEntry = Tkinter.Entry(self, textvariable=self.valueModel)
        self.valueEntry.grid(column=1, row=0, sticky='EW')
        self.valueEntry.bind("<Return>", self.OnPressEnter)

        button = Tkinter.Button(self, text=u"Add new",
                                command=self.OnButtonClick)
        button.grid(column=2, row=0)

        self.separatorModel = Tkinter.StringVar()
        separatorLabel = Tkinter.Label(self, textvariable=self.separatorModel,
                              anchor="w", fg="white", bg="gray")
        separatorLabel.grid(column=0, row=1, columnspan=2, sticky='EW')
        self.separatorModel.set(u"System environment variables")
        print "initialize method len(self.t)" + str(len(self.t))

        for i in range(len(self.t)):
            print "kkkkkkkkkkkkk"
            cellNameModel = Tkinter.StringVar()
            cellNameModel.set(self.t[i][0])
            nameCell = Tkinter.Entry(self, textvariable=cellNameModel)
            nameCell.grid(row=i + 2, column=0, sticky='EW')

            cellValueModel = Tkinter.StringVar()
            cellValueModel.set(self.t[i][1])
            valueCell = Tkinter.Entry(self, textvariable=cellValueModel)
            valueCell.grid(row=i + 2, column=1, sticky='EW')
            self.cells.append((nameCell, valueCell))

        self.grid_columnconfigure(0, weight=1)
        self.resizable(True, True)
        self.update()
        self.geometry(self.geometry())
        self.nameEntry.focus_set()
        self.nameEntry.selection_range(0, Tkinter.END)

    def OnButtonClick(self):
        self.t.append((self.nameModel.get(), self.valueModel.get()))
        self.initialize();
        print len(self.t)

        self.separatorModel.set(self.valueModel.get() + " (You clicked the button)")
        self.nameEntry.focus_set()
        self.nameEntry.selection_range(0, Tkinter.END)
        self.nameModel.set("")
        self.valueModel.set("")

    def OnPressEnter(self, event):
        self.separatorModel.set(self.valueModel.get() + " (You pressed ENTER)")
        self.valueEntry.focus_set()
        self.valueEntry.selection_range(0, Tkinter.END)


if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('Imbus')
    app.mainloop()
