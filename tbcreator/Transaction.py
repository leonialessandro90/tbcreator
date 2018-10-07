from .Misc import ClassType, ClassObj

class TransactionType(ClassType):

    def __init__(self, typeName):
        ClassType.__init__(self, typeName)
        self.attributes = []

    def addAttribute(self, attr):
        self.attributes.append(attr)

    def createFile(self):
        r = "class "+self.typeName+";\n\n"
        for attr in self.attributes:
            r += attr.declare()

        r += "\nfunction new();\n"
        for attr in self.attributes:
            r += "    "+attr.initialize()
        r += "endfunction\n\n"
        r += "endclass"
        super(TransactionType, self).createFile(r)
