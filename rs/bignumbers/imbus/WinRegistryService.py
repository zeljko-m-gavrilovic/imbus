'''
Created on Feb 22, 2016

@author: zeljko.gavrilovic
'''

from _winreg import *
import os, sys  # , win32gui, win32con


class WinRegistryService:
    PATH_SEPARATOR = ';'
    PATH = r'\CurrentControlSet\Control\Session Manager\Environment'
    SYSTEM_PATH = r'SYSTEM' + PATH;
    USER_PATH = r'USER' + PATH;
    
    def __init__(self):
        self.path = self.USER_PATH;
        # self.reg = ConnectRegistry(None, HKEY_USERS)
        # self.key = OpenKey(self.reg, self.path, 0, KEY_ALL_ACCESS)
        self.key = OpenKeyEx(HKEY_CURRENT_USER, 'Environment', 0, KEY_ALL_ACCESS)
        
    
    def getAllEnvVariable(self):
        result = []
        for i in range(QueryInfoKey(self.key)[1]):
            name, value, type = EnumValue(self.key, i)
            result.append((type, name, value))
        return result    
            
    def getEnvVariable(self, name):
        answer = QueryValueEx(self.key, name)
        result = (answer[1], answer, answer[0])
        return result
    
    def addEnvVariable(self, name, value):
        self.updateEnvVariable(name, value);
    
    def updateEnvVariable(self, name, newValue):
        value = newValue
        if name.upper() == 'PATH':
            value = self.getEnvVariable(name) + self.PATH_SEPARATOR + newValue
        if value:
            SetValueEx(self.key, name, 0, REG_EXPAND_SZ, value)
            
    def removeEnvVariable(self, name):
        DeleteValue(self.key, name)

    def printVars(self, tuples):
        for t in tuples:
            self.printVar(t)
    
    def printVar(self, tuple):
        print("%s = %s" % (tuple[1], tuple[2]))
        
if __name__ == "__main__":
    wrs = WinRegistryService()
    print "all variables" 
    wrs.printVars(wrs.getAllEnvVariable())
    
    print "TMP variable" 
    wrs.printVar(wrs.getEnvVariable("TMP"))
    
    print wrs.addEnvVariable("testDevEnv", 'c:\\dev')
    print "you should see the variable testDevEnv"
    wrs.printVars(wrs.getAllEnvVariable())
    
    print wrs.updateEnvVariable("testDevEnv", 'c:\\dev\wrong')
    print "you should see the variable testDevEnv=c:\\dev\wrong"
    wrs.printVars(wrs.getAllEnvVariable())
    
    print wrs.removeEnvVariable("testDevEnv")
    print "you should not see the variable testDevEnv"
    wrs.printVars(wrs.getAllEnvVariable())
    
