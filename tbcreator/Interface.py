from .Misc import ClassType, ClassObj, Signal

class InterfaceType(ClassType):

    def __init__(self, typeName, isRead, isWrite):
        ClassType.__init__(self, typeName)
        self.signals = []
        self.params = []
        self.trType = None
        self.isRead = isRead
        self.isWrite = isWrite
        self.drv = None
        self.mon = None
        self.addSignal(Signal("bit","clk","special"))
        self.addSignal(Signal("bit","rst","special"))

    def createObj(self, name):
        return InterfaceObj(self, name)

    def addSignal(self, sig):
        self.signals.append(sig)
    
    def addParameter(self, param):
        self.params.append(param)

    def addRelatedTransaction(self, trType):
        self.trType = trType

    def createFile(self, packageName):
        r = "import "+packageName+"::*;\n\n"
        if(self.params != []):
            r += "interface "+self.typeName+"#("
            for i in range (0, len(self.params)):
                r += "parameter "+self.params[i].type + " "
                if(i == len(self.params)-1):
                    r += self.params[i].name
                else:
                    r += self.params[i].name+", "
            r+=");\n"
        else:
            r += "interface "+self.typeName+";\n"

        for sig in self.signals:
            r+="\t"+sig.declare()

        r += "endinterface\n"
        super(InterfaceType, self).createFile(r)


class InterfaceObj(ClassObj):

    def __init__(self, classType, name):
        ClassObj.__init__(self, classType, name)
        self.drv = None
        self.mon = None
        self.paramNames = []
        self.paramValues = []

    def setParamValue(self, paramName, paramValue):
        self.paramNames.append(paramName)
        self.paramValues.append(paramValue)


    def connectToDriver(self, drvObj):
        self.drv = drvObj

    def connectToMonitor(self, monObj):
        self.mon = monObj

    def instantiate(self):
        r = ""
        if(self.paramValues == []):
            return self.classType.typeName + " "+ self.name+"();\n"
        else:
            r = self.classType.typeName + "#(\n"
            for i in range(0, len(self.paramNames)):
                r += "\t"+"."+self.paramNames[i]+" ("+self.paramValues[i]+")"
                if(i == len(self.paramNames) -1):
                    r += "\n)"
                else:
                    r += ",\n"
            r += self.name+"();\n"
        return r


