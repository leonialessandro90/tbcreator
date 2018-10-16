from .Misc import ClassType
import os

class DUT(ClassType):
    
    def __init__(self, typeName):
        ClassType.__init__(self, typeName)
        self.dutItfName = []
        self.itfs = []
        self.params = []
        self.paramValues = []
        self.itfIsMaster = []

    def addParameter(self, param, value):
        self.params.append(param)
        self.paramValues.append(value)

    def connectInterface(self, dutItfName, itfObj, isMaster):
        self.dutItfName.append(dutItfName)
        self.itfs.append(itfObj)
        if(isMaster == "Master"):
            self.itfIsMaster.append(True)
        else:
            self.itfIsMaster.append(False)

    def instantiate(self):
        r = ""
        if(self.params == []):
            r += self.typeName + " dut (\n"
        else:
            r += self.typeName + "#(\n"
            for i in range(0, len(self.params)):
                r += "\t"+"."+self.params[i].name+" ("+self.paramValues[i]+")"
                if(i == len(self.params)-1):
                    r += "\n)"
                else:
                    r += ",\n"
            r += "dut (\n"
        
        for i in range(0, len(self.dutItfName)):
            if(self.itfIsMaster[i]):
                r += "\t"+"."+self.dutItfName[i]+" ("+self.itfs[i].name+".master),\n"
            else:
                r += "\t"+"."+self.dutItfName[i]+" ("+self.itfs[i].name+".slave),\n"
        r += "\t"+".clk (clk),\n"
        r += "\t"+".rst (rst)\n"
        r += "\t"+"//USER: CHECK IF CLK AND RESET ARE OK THIS WAY!\n"
        r += ");\n\n"    
        return r
    
    def createDummyFile(self):
        oldDir = ClassType.outputDir
        db = os.path.split(ClassType.outputDir)[0]
        ClassType.outputDir = os.path.join(db,"src")
        if(not os.path.exists(ClassType.outputDir)):
            os.makedirs(ClassType.outputDir)

        r = ""
        itfTypeList = []
        for itf in self.itfs:
            if itf.classType.typeName not in itfTypeList:
                itfTypeList.append(itf.classType.typeName)
        for itfType in itfTypeList:
            r += "`include \"../tb/"+itfType+".sv\"\n"

        r += "module "+self.typeName
        if(self.params == []):
            r += "(\n"
        else:
            r += "#(\n"
            for i in range(0, len(self.params)):
                r += self.params[i].type + " "+ self.params[i].name
                if i == len(self.params)-1:
                    r+=")\n"
                else:
                    r+=",\n"
            r+="(\n"

            
        for i in range(0, len(self.itfs)):
            if(self.itfIsMaster[i]):
                r += self.itfs[i].classType.typeName + ".master "+ self.dutItfName[i] + ",\n"
            else:
                r += self.itfs[i].classType.typeName + ".slave "+ self.dutItfName[i] + ",\n"

        
        r += "input logic clk,\ninput logic rst);\n"

        r += "endmodule"
    
        super(DUT, self).createFile(r)
        ClassType.outputDir = oldDir
