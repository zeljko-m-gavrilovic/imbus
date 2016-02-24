'''
Created on Feb 22, 2016

@author: zeljko.gavrilovic
'''

#from winreg import *
from winreg import HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, OpenKeyEx, \
    KEY_ALL_ACCESS, QueryInfoKey, EnumValue, CloseKey, QueryValueEx, SetValueEx, \
    REG_EXPAND_SZ, DeleteValue


class WinRegistryEnvironmentVariables:
    """ This class is a service for CRUD operations on windows environment variables registry"""
    PATH_SEPARATOR = ';'
    
    def __init__(self, scope):
        assert scope in ('user', 'system')
        self.scope = scope
        if scope == 'user':
            self.root = HKEY_CURRENT_USER
            self.subkey = 'Environment'
        else:
            self.root = HKEY_LOCAL_MACHINE
            self.subkey = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'

    def getAllEnvVariable(self):
        result = []
        key = OpenKeyEx(self.root, self.subkey, 0, KEY_ALL_ACCESS)
        for i in range(QueryInfoKey(key)[1]):
            name, value, envType = EnumValue(key, i)
            result.append((self.scope, name, value))
        CloseKey(key)    
        return result
    
    def getEnvVariable(self, name):
        key = OpenKeyEx(self.root, self.subkey, 0, KEY_ALL_ACCESS)
        answer = QueryValueEx(key, name)
        result = (self.scope, name, answer[0])
        CloseKey(key)
        return result[2]

    def addEnvVariable(self, name, value):
        self.updateEnvVariable(name, value);

    def updateEnvVariable(self, name, value):
        if value:
            key = OpenKeyEx(self.root, self.subkey, 0, KEY_ALL_ACCESS)
            SetValueEx(key, name, 0, REG_EXPAND_SZ, value)
            CloseKey(key)

    def removeEnvVariable(self, name):
        key = OpenKeyEx(self.root, self.subkey, 0, KEY_ALL_ACCESS)
        DeleteValue(key, name)
        CloseKey(key)

    def printVars(self, tuples):
        for t in tuples:
            self.printVar(t)

    def printVar(self, envTuple):
        print("%s = %s" % (envTuple[1], envTuple[2]))

if __name__ == "__main__":
    wrs = WinRegistryEnvironmentVariables("user")
    print("all user variables")
    wrs.printVars(wrs.getAllEnvVariable())

    print("TMP variable")
    wrs.printVar(wrs.getEnvVariable("TMP"))

    wrs.addEnvVariable("testDevEnv", r'c:\\dev')
    print("you should see the variable testDevEnv")
    wrs.printVars(wrs.getAllEnvVariable())
    
    wrs.updateEnvVariable("testDevEnv", r'c:\\dev\updated')
    print(r"you should see the variable testDevEnv=c:\\dev\updated")
    wrs.printVars(wrs.getAllEnvVariable())

    wrs.removeEnvVariable("testDevEnv")
    print("you should not see the variable testDevEnv")
    wrs.printVars(wrs.getAllEnvVariable())