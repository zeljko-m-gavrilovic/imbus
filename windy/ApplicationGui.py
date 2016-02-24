from tkinter.constants import END, YES, BOTH, X

from EnvironmentVariableGui import EnvironmentVariableGui
from ImportGui import ImportGui
from WinRegistryEnvironmentVariables import WinRegistryEnvironmentVariables
import tkinter.font as tkFont
import tkinter as tk
import tkinter.ttk as ttk


class Application(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.winUserRegistryService = WinRegistryEnvironmentVariables("user")
        self.winSystemRegistryService = WinRegistryEnvironmentVariables("system")
        self.header = ["Scope", "Name", "Value"]
        self.createGui()
        self.refresh()
        try:
            self.winSystemRegistryService.getEnvVariable("PATH")
        except WindowsError:
            # print("System environment variables can't be loaded because you need to run the application in the admin mode...")
            self.restricted = True
            tk.messagebox.showwarning("System environment variables permission", "You have started the application with NO ADMIN RIGHTS. In order to change the system environment variables you need to open the application in the admin mode. Otherwise you are allowed to edit only user environment varialbes..")
    
    def createGui(self):
        separatorLabel = tk.Label(text=u"Environment variables", anchor="nw", fg="white", bg="gray")
        separatorLabel.pack(fill="x")
        
        container = ttk.Frame()
        container.pack(fill='both', expand=True)
        # create a treeview with vertical scrollbar
        self.tree = ttk.Treeview(columns=self.header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        #self.tree.bind("<Double-1>", self.edit())
        
        importButton = tk.Button( text=u"Import...", command=self.importEnv)
        importButton.pack(side="right")
         
        importButton = tk.Button(text=u"Remove", command=self.remove)
        importButton.pack(side="right")
         
        importButton = tk.Button(text=u"Edit", command=self.edit)
        importButton.pack(side="right")
         
        addButton = tk.Button(text=u"Add new", command=self.addNew)
        addButton.pack(side="right")
    
    def refresh(self):
        self.envVariables = self.winUserRegistryService.getAllEnvVariable()
        try:
            systemVars = self.winSystemRegistryService.getAllEnvVariable()
            self.envVariables.extend(systemVars)
        except WindowsError:
            pass  # user already informed about the lack of the permissions when the application has first started
        
#         for col in self.header:
#             self.tree.heading(col, text=col.title(),
#                 command=lambda c=col: self.sortby(self.tree, c, 0))
#             # adjust the column's width to the header string
#             self.tree.column(col, width=tkFont.Font().measure(col.title()))
        
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in self.envVariables:
            self.tree.insert('', 'end', values=item)
            #Note: I found this buggy because it messed up border around the widgetadjust column's width if necessary to fit each value
#             for ix, val in enumerate(item):
#                 col_w = tkFont.Font().measure(val)
#                 if self.tree.column(self.header[ix], width=None) < col_w:
#                     self.tree.column(self.header[ix], width=col_w)
    
    def sortby(self, tree, col, descending):
        """sort tree contents when a column header is clicked on"""
        # grab values to sort
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        # if the data to be sorted is numeric change to float
        # data =  change_numeric(data)
        # now sort the data in place
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            tree.move(item[1], '', ix)
        # switch the heading so it will sort in the opposite direction
        tree.heading(col, command=lambda col=col: self.sortby(tree, col, int(not descending)))
    
    def addNew(self):
        newWindow = tk.Toplevel(self)
        EnvironmentVariableGui(newWindow, self, scope="user", mode="add").pack(side="top", fill="both", expand=True)
        self.after(1, lambda: newWindow.focus_force())
    

    def getSelected(self):
        curItem = self.tree.focus()
        selected = self.tree.item(curItem)
        scope = selected["values"][0]
        name = selected["values"][1]
        value = selected["values"][2]
        return name, value, scope

    def edit(self):
        name, value, scope = self.getSelected()
        
        newWindow = tk.Toplevel(self)
        EnvironmentVariableGui(newWindow, self, name, value, scope, mode="edit").pack(side="top", fill="both", expand=True)
        self.after(1, lambda: newWindow.focus_force())
    
    def remove(self):
        name, value, scope = self.getSelected()
        
        result = tk.messagebox.askquestion("Delete", "Are you sure you want to delete the environment variable " + name + "?", icon="warning")
        if result != "yes":
            return
        if(scope == "user"):
            self.winUserRegistryService.removeEnvVariable(name)
        else:
            self.winSystemRegistryService.removeEnvVariable(name)
        self.refresh()
        
    def importEnv(self):
        newWindow = tk.Toplevel(self)
        ImportGui(newWindow, self).pack(side="top", fill="both", expand=True)
        self.after(1, lambda: newWindow.focus_force())

if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("Windy - Editor for Windows environment variables")
    appSize = (800, 600)
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
 
    x = w / 2 - appSize[0] / 2
    y = h / 2 - appSize[1] / 2
    root.geometry("%dx%d+%d+%d" % (appSize + (x, y)))
    root.update_idletasks()  # Force geometry update

    Application(root)#.pack(side="top", fill="both", expand=True)
    root.mainloop()
