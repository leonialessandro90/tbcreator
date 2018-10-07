from .Misc import Parameter, ClassType
import os

class Package(ClassType):

    def __init__(self, pkgName):
        ClassType.__init__(self, pkgName)
        self.params = []
        self.addParameter(Parameter("int","CLOCK_PERIOD","10","USER: Modify this at your pleasure"))
        self.files = []
        self.itfs = []

    def addParameter(self, param):
        self.params.append(param)

    def addIncludeFile(self, fileName):
        if fileName not in self.files:
            self.files.append(fileName)

    def addInterface(self, itfTypeName):
        self.itfs.append(itfTypeName)

    def createFile(self):
        r = ""
        r += "package " + self.typeName+";\n\n"

        for con in self.params:
            r += con.declare()
        
        for file in self.files:
            r += "`include \""+file+"\"\n"

        r += "endpackage"
        super(Package, self).createFile(r)

