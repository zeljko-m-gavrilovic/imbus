import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import tkinter.constants as tc
import windy.service.environment_variables_service as envvarservice
import windy.gui.env_variable_editor as guieditor
import windy.gui.env_variable_import as guiimport 


class Application(tk.Frame):
    def __init__(self, root):
        ttk.Frame.__init__(self, root)
        self.root = root
        self.winUserEnvVarService = envvarservice.EnvironmentVariableService("user")
        self.winSystemEnvVarService = envvarservice.EnvironmentVariableService("system")
        self.header = ["Scope", "Name", "Value"]
        self.createGui()
        self.refresh()
        self.restricted = False
        try:
            self.winSystemEnvVarService.getEnvVariable("PATH")
        except WindowsError:
            # print("System environment variables can't be loaded because you need to run the application in the admin mode...")
            self.restricted = True
            mb.showwarning("System environment variables permission", "You have started the application with NO ADMIN RIGHTS. In order to change the system environment variables you need to open the application in the admin mode. Otherwise you are allowed to edit only user environment varialbes..")
    
    def createGui(self):
        separatorLabel = ttk.Label(text="Environment variables", anchor="nw")
        separatorLabel.pack(fill="x")
        
        container = ttk.Frame()
        container.pack(fill='both', expand=True)
        self.tree = ttk.Treeview(columns=self.header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        
        importButton = ttk.Button(text="Import...", command=self.importEnvVars)
        importButton.pack(side="right")
         
        importButton = ttk.Button(text="Remove", command=self.remove)
        importButton.pack(side="right")
         
        importButton = ttk.Button(text="Edit", command=self.edit)
        importButton.pack(side="right")
         
        addButton = ttk.Button(text="Add new", command=self.addNew)
        addButton.pack(side="right")
    
    def refresh(self):
        self.envVariables = self.winUserEnvVarService.getAllEnvVariable()
        try:
            systemVars = self.winSystemEnvVarService.getAllEnvVariable()
            self.envVariables.extend(systemVars)
        except WindowsError:
            pass  # user already informed about the lack of the permissions when the application has first started
                
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in self.envVariables:
            self.tree.insert('', 'end', values=item)
        
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
        guieditor.EnvironmentVariableEditor(newWindow, self, scope="user", mode="add").pack(side="top", fill="both", expand=True)
        self.after(1, lambda: newWindow.focus_force())    

    def getSelected(self):
        curItem = self.tree.focus()
        selected = self.tree.item(curItem)
        scope = selected["values"][0]
        name = selected["values"][1]
        value = selected["values"][2]
        return name, value, scope

    def edit(self):
        try:
            name, value, scope = self.getSelected()
        except IndexError:
            tk.messagebox.showinfo("Environment variable selection", "Please select a row to be edited")   
            return;
        newWindow = tk.Toplevel(self)
        guieditor.EnvironmentVariableEditor(newWindow, self, name, value, scope, "edit").pack(side="top", fill="both", expand=True)
        self.after(1, lambda: newWindow.focus_force())
    
    def remove(self):
        try:
            name, value, scope = self.getSelected()
        except IndexError:
            tk.messagebox.showinfo("Environment variable selection", "Please select a row to be removed")   
            return;
        
        result = tk.messagebox.askquestion("Delete", "Are you sure you want to remove the environment variable " + name + "?", icon="warning")
        if result != "yes":
            return
        if(scope == "user"):
            self.winUserEnvVarService.removeEnvVariable(name)
        else:
            self.winSystemEnvVarService.removeEnvVariable(name)
        self.refresh()
        
    def importEnvVars(self):
        newWindow = tk.Toplevel(self)
        guiimport.EnvironmentVariableImport(newWindow, self).pack(side="top", fill="both", expand=True)
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
