
from .Misc import ClassType, ClassObj

class MonitorType(ClassType):
    
    def __init__(self, typeName, trType, mbType, itfType):
        ClassType.__init__(self, typeName)
        self.mbType = mbType
        self.trType = trType
        self.itfType = itfType

    def createObj(self, name):
        return MonitorObj(self, name)

    def createFile(self):
        r = "class "+self.typeName+";\n\n"
        r += "virtual "+self.itfType.typeName+" itf;\n"
        r += self.mbType.typeName+" mb;\n"
        r += self.trType.typeName+" tr;\n\n"

        r += "function new();\n"
        r += "endfunction\n\n"

        r += "function void setMailbox("+self.mbType.typeName+" mb);\n"
        r += "\t"+"this.mb = mb;\n"
        r += "endfunction\n\n"

        r += "function void setInterface(virtual " + self.itfType.typeName+" itf);\n"
        r += "\t"+"this.itf = itf;\n"
        r += "endfunction\n\n"

        r += "task run();\n"
        r += "\t"+"forever begin\n"
        r += "\t"+"\t"+"@(posedge itf.clk);\n"
        r += "\t"+"\t"+"tr = new();\n"
        r += "\n\t"+"\t"+"//USER: Transaction fields to fill:\n"
        for attr in self.trType.attributes:
            r += "\t"+"\t"+"//tr."+attr.name+" ("+attr.type+")\n"
        r += "\n\t"+"\t"+"//USER: Inteface signals:\n"
        for sig in self.itfType.signals:
            if sig.direction != "special":
                r += "\t"+"\t"+"//itf."+sig.name+" ("+sig.type+", "+sig.direction+")\n"
        r += "\n\t"+"\t"+"mb.put(tr);\n"
        r += "\n\t"+"\t"+"//USER: perhaps your transaction requires more clock cycles/has multiple data?\n"
        r += "\t"+"end\n"
        r += "endtask\n\n"
        r += "endclass\n"
        super(MonitorType, self).createFile(r)

class MonitorObj(ClassObj):

    def __init__(self, classType, name):
        ClassObj.__init__(self, classType, name)
        self.itf = None
        self.mb = None

    def connectToInterface(self, itfObj):
        self.itf = itfObj

    def connectToMailbox(self, mbObj):
        self.mb = mbObj