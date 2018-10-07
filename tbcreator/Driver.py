from .Misc import ClassType, ClassObj


class DriverType(ClassType):

    def __init__(self, typeName, trType, mbType, itfType):
        ClassType.__init__(self, typeName)
        self.mbType = mbType
        self.trType = trType
        self.itfType = itfType

    def createObj(self, name):
        return DriverObj(self, name)

    def createFile(self):
        r = ""
        r += "class "+self.typeName+";\n\n"
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

        r += "\t"+"//USER: Initialize signals of the interface:\n"
        for sig in self.itfType.signals:
            if sig.direction == "in":
                r += "\t"+"itf."+sig.name+" <= 0;\n"
        
        r += "\n\t"+"forever begin\n"
        r += "\t"+"\t"+"@(posedge itf.clk);\n"
        r += "\t"+"\t"+"mb.get(tr);\n"
        r += "\n\t"+"\t"+"//USER: Transaction fields to fill:\n"
        for attr in self.trType.attributes:
            r += "\t"+"\t"+"//tr."+attr.name+" ("+str(attr.type)+")\n"
        r += "\n\t"+"\t"+"//USER: Interface signals:\n"
        for sig in self.itfType.signals:
            if(sig.direction != "special"):
                r += "\t"+"\t"+"//itf."+sig.name+" ("+sig.type+" "+sig.direction+")\n"
        r += "\n\t"+"\t"+"//USER: perhaps your transaction requires more clock cycles/has multiple data?ss\n"
        r += "\t"+"end\n"
        r += "endtask\n\n"
        r += "endclass"
        super(DriverType, self).createFile(r)



class DriverObj(ClassObj):

    def __init__(self, classType, name):
        ClassObj.__init__(self, classType, name)
        self.itf = None
        self.mb = None

    def connectToInterface(self, itfObj):
        self.itf = itfObj

    def connectToMailbox(self, mbObj):
        self.mb = mbObj