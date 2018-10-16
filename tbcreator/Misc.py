import os

class ClassType:
    
    outputDir = ""

    def __init__(self, typeName):
        self.typeName = typeName

    def createObj(self, name):
        return ClassObj(self, name)

    def createFile(self, content, additionalPath = ""):
        F = open(os.path.join(self.outputDir,additionalPath,self.typeName+".sv"), "w")
        F.write(content)
        F.close()
    
class ClassObj:

    def __init__(self, classType, name):
        self.classType = classType
        self.name = name
    
    def declare(self):
        return self.classType.typeName + " " + self.name + ";\n"

    def initialize(self):
        return self.name + " = new();\n"


class Parameter:

    def __init__(self, type, name, value = None, comment = ""):
        self.type = type
        self.name = name
        self.value = value
        self.comment = ""
        if(comment != ""):
            self.comment = "\t\t\t//"+comment

    def declare(self):
        return "parameter "+self.type+" "+self.name+" = "+self.value+";"+self.comment+"\n"

class Attribute:

    def __init__(self, type, name, postName, initValue, comment = ""):
        self.type = type
        self.name = name
        self.initValue = initValue
        self.comment = ""
        self.postName = postName
        if(comment != ""):
            self.comment = "\t\t\t//"+comment
    
    def declare(self):
        return self.type+" "+self.name+self.postName+";"+self.comment+"\n"

    def initialize(self):
        return self.name + " = "+self.initValue+";\n"


class Signal:

    def __init__(self, type, name, comment = ""):
        self.type = type
        self.name = name
        self.comment = ""
        if(comment != ""):
            self.comment = "\t\t\t//"+comment

    def declare(self):
        return self.type+" "+self.name+";"+self.comment+"\n"

    def initialize(self, name, value):
        return name + " = "+value+";\n"
