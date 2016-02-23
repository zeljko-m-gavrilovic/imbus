from Tkconstants import END, YES, BOTH, X
import tkMessageBox

from EnvironmentVariableGui import EnvironmentVariableGui
from ImportGui import ImportGui
from MultiListbox import MultiListbox
import Tkinter as tk
from WinRegistryService import WinRegistryEnvironmentVariables


class Application(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.winUserRegistryService = WinRegistryEnvironmentVariables("user")
        self.winSystemRegistryService = WinRegistryEnvironmentVariables("system")
        self.createGui()
        self.refresh()
        
        try:
            pathVar = self.winSystemRegistryService.getEnvVariable("PATH")
        except WindowsError:
            print "System environment variables can't be loaded because you need to run the application in the admin mode..."
            tkMessageBox.showwarning("System environment variables permission", "You have started the application with NO ADMIN RIGHTS. In order to change the system environment variables you need to open the application in the admin mode. Otherwise you are allowed to edit only user environment varialbes..")
            
    def refresh(self):
        self.envVariables = self.winUserRegistryService.getAllEnvVariable()
        try:
            systemVars = self.winSystemRegistryService.getAllEnvVariable()
            self.envVariables.extend(systemVars)
        except WindowsError:
            pass # user already informed about the lack of the permissions when the application has first started
        
        self.mlb.delete(0, self.mlb.size())
        for i in range(len(self.envVariables)):
            scope = self.envVariables[i][0]
            name = self.envVariables[i][1]
            value = self.envVariables[i][2]
            self.mlb.insert(END,(scope, name, value))    
    
    def createGui(self):
        separatorLabel = tk.Label(self, text=u"Environment variables", anchor="nw", fg="white", bg="gray")
        separatorLabel.pack(fill="x")
        
        self.mlb = MultiListbox(self, (('Scope', 20), ('Name', 40), ('Value', 60)))
        self.mlb.pack(expand=YES, fill=BOTH)    
        
        importButton = tk.Button(self, text=u"Import...", command=self.importEnv)
        importButton.pack(side="right", expand=YES, fill=X)
        
        importButton = tk.Button(self, text=u"Remove", command=self.remove)
        importButton.pack(side="right", expand=YES, fill=X)
        
        importButton = tk.Button(self, text=u"Edit", command=self.edit)
        importButton.pack(side="right", expand=YES, fill=X)
        
        addButton = tk.Button(self, text=u"Add new", command=self.addNew)
        addButton.pack(side="right", expand=YES, fill=X)
        
#     def onFrameResize(self, event):
#         '''Reset the scroll region to encompass the inner frame'''
#         self.canvas.configure(scrollregion=self.canvas.bbox("all"))
#         self.canvas.itemconfig(self._frame_id, height=event.height, width=event.width)

    def addNew(self):
        newWindow = tk.Toplevel(self)
        EnvironmentVariableGui(newWindow, self, scope="user", mode="add").pack(side="top", fill="both", expand=True)
        self.after(1, lambda: newWindow.focus_force())
    
    def edit(self):
        selected = self.mlb.get(self.mlb.curselection())
        scope = selected[0]
        name = selected[1]
        value = selected[2]
        
        newWindow = tk.Toplevel(self)
        EnvironmentVariableGui(newWindow, self, name, value, scope, mode="edit").pack(side="top", fill="both", expand=True)
        self.after(1, lambda: newWindow.focus_force())
    
    def remove(self):
        selected = self.mlb.get(self.mlb.curselection())
        scope = selected[0]
        name = selected[1]
        
        result = tkMessageBox.askquestion("Delete", "Are you sure you want to delete the environment variable " + name + "?", icon="warning")
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
    root.title("Windy - Editor for Windows environment variables")
    appSize = (800, 600)
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()

    x = w / 2 - appSize[0] / 2
    y = h / 2 - appSize[1] / 2
    root.geometry("%dx%d+%d+%d" % (appSize + (x, y)))
    root.update_idletasks()  # Force geometry update

    Application(root).pack(side="top", fill="both", expand=True)
    root.mainloop()