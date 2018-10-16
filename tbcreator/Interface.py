from .Misc import ClassType, ClassObj, Signal, Parameter

class InterfaceType(ClassType):

    def __init__(self, typeName):
        ClassType.__init__(self, typeName)
        self.signalMasterInput = []
        self.signalMasterOutput = []
        self.signalSlaveInput = []
        self.signalSlaveOutput = []

        self.signals = []
        self.params = []
        self.trType = None
        self.drv = None
        self.mon = None
        self.addSignal(Signal("logic","clk"), "special")
        self.addSignal(Signal("logic","rst"), "special")

    @staticmethod
    def createAXIFull():
        itfType = InterfaceType("axi_full_itf")

        itfType.addParameter(Parameter("int","M_AXI_ADDR_WIDTH","32"))
        itfType.addParameter(Parameter("int","M_AXI_DATA_WIDTH","32"))
        itfType.addParameter(Parameter("int","M_AXI_ID_WIDTH","1"))
        itfType.addParameter(Parameter("int","M_AXI_ARUSER_WIDTH","1"))
        itfType.addParameter(Parameter("int","M_AXI_RUSER_WIDTH","1"))
        itfType.addParameter(Parameter("int","M_AXI_AWUSER_WIDTH","1"))
        itfType.addParameter(Parameter("int","M_AXI_WUSER_WIDTH","1"))
        itfType.addParameter(Parameter("int","M_AXI_BUSER_WIDTH","1"))

        itfType.addSignal(Signal("logic[M_AXI_ID_WIDTH-1:0]","awid"), "isMasterOutput")
        itfType.addSignal(Signal("logic[M_AXI_ADDR_WIDTH-1:0]","awaddr"), "isMasterOutput")
        itfType.addSignal(Signal("logic[7:0]","awlen"), "isMasterOutput")
        itfType.addSignal(Signal("logic[2:0]","awsize"), "isMasterOutput")
        itfType.addSignal(Signal("logic[1:0]","awburst"), "isMasterOutput")
        itfType.addSignal(Signal("logic","awlock"), "isMasterOutput")
        itfType.addSignal(Signal("logic[3:0]","awcache"), "isMasterOutput")
        itfType.addSignal(Signal("logic[2:0]","awprot"), "isMasterOutput")
        itfType.addSignal(Signal("logic[3:0]","awqos"), "isMasterOutput")
        itfType.addSignal(Signal("logic[M_AXI_AWUSER_WIDTH-1:0]","awuser"), "isMasterOutput")
        itfType.addSignal(Signal("logic","awvalid"), "isMasterOutput")
        itfType.addSignal(Signal("logic","awready"), "isMasterInput")

        itfType.addSignal(Signal("logic[M_AXI_DATA_WIDTH-1:0]","wdata"), "isMasterOutput")
        itfType.addSignal(Signal("logic[M_AXI_DATA_WIDTH/8-1:0]","wstrb"), "isMasterOutput")
        itfType.addSignal(Signal("logic","wlast"), "isMasterOutput")
        itfType.addSignal(Signal("logic[M_AXI_WUSER_WIDTH-1:0]","wuser"), "isMasterOutput")
        itfType.addSignal(Signal("logic","wvalid"), "isMasterOutput")
        itfType.addSignal(Signal("logic","wready"), "isMasterInput")
        
        itfType.addSignal(Signal("logic[M_AXI_ID_WIDTH-1:0]","bid"), "isMasterInput")
        itfType.addSignal(Signal("logic[1:0]","bresp"), "isMasterInput")
        itfType.addSignal(Signal("logic[M_AXI_BUSER_WIDTH-1:0]","buser"), "isMasterInput")
        itfType.addSignal(Signal("logic","bvalid"), "isMasterInput")
        itfType.addSignal(Signal("logic","bready"), "isMasterOutput")

        itfType.addSignal(Signal("logic[M_AXI_ID_WIDTH-1:0]","arid"), "isMasterOutput")
        itfType.addSignal(Signal("logic[M_AXI_ADDR_WIDTH-1:0]","araddr"), "isMasterOutput")
        itfType.addSignal(Signal("logic[7:0]","arlen"), "isMasterOutput")
        itfType.addSignal(Signal("logic[2:0]","arsize"), "isMasterOutput")
        itfType.addSignal(Signal("logic[1:0]","arburst"), "isMasterOutput")
        itfType.addSignal(Signal("logic","arlock"), "isMasterOutput")
        itfType.addSignal(Signal("logic[3:0]","arcache"), "isMasterOutput")
        itfType.addSignal(Signal("logic[2:0]","arprot"), "isMasterOutput")
        itfType.addSignal(Signal("logic[3:0]","arqos"), "isMasterOutput")
        itfType.addSignal(Signal("logic[M_AXI_ARUSER_WIDTH-1:0]","aruser"), "isMasterOutput")
        itfType.addSignal(Signal("logic","arvalid"), "isMasterOutput")
        itfType.addSignal(Signal("logic","arready"), "isMasterInput")

        itfType.addSignal(Signal("logic[M_AXI_ID_WIDTH-1:0]","rid"), "isMasterInput")
        itfType.addSignal(Signal("logic[M_AXI_DATA_WIDTH-1:0]","rdata"), "isMasterInput")
        itfType.addSignal(Signal("logic[1:0]","rresp"), "isMasterInput")
        itfType.addSignal(Signal("logic","rlast"), "isMasterInput")
        itfType.addSignal(Signal("logic[M_AXI_RUSER_WIDTH-1:0]","ruser"), "isMasterInput")
        itfType.addSignal(Signal("logic","rvalid"), "isMasterInput")
        itfType.addSignal(Signal("logic","rready"), "isMasterOutput")

        return itfType 

    @staticmethod
    def createAXILite():
        itfType = InterfaceType("axi_lite_itf")

        itfType.addParameter(Parameter("int","S_AXI_ADDR_WIDTH","32"))
        itfType.addParameter(Parameter("int","S_AXI_DATA_WIDTH","32"))

        itfType.addSignal(Signal("logic[S_AXI_ADDR_WIDTH-1:0]","awaddr"), "isMasterOutput")
        itfType.addSignal(Signal("logic","awvalid"), "isMasterOutput")
        itfType.addSignal(Signal("logic","awready"), "isMasterInput")

        itfType.addSignal(Signal("logic[S_AXI_DATA_WIDTH-1:0]","wdata"), "isMasterOutput")
        itfType.addSignal(Signal("logic","wvalid"), "isMasterOutput")
        itfType.addSignal(Signal("logic","wready"), "isMasterInput")
        itfType.addSignal(Signal("logic[S_AXI_DATA_WIDTH/8-1:0]","wstrb"), "isMasterOutput")

        itfType.addSignal(Signal("logic[1:0]","bresp"), "isMasterInput")
        itfType.addSignal(Signal("logic","bvalid"), "isMasterInput")
        itfType.addSignal(Signal("logic","bready"), "isMasterOutput")

        itfType.addSignal(Signal("logic[S_AXI_ADDR_WIDTH-1:0]","araddr"), "isMasterOutput")
        itfType.addSignal(Signal("logic","arvalid"), "isMasterOutput")
        itfType.addSignal(Signal("logic","arready"), "isMasterInput")

        itfType.addSignal(Signal("logic[S_AXI_DATA_WIDTH-1:0]","rdata"), "isMasterInput")
        itfType.addSignal(Signal("logic[1:0]","rresp"), "isMasterInput")
        itfType.addSignal(Signal("logic","rvalid"), "isMasterInput")
        itfType.addSignal(Signal("logic","rready"), "isMasterOutput")

        return itfType 



    def createObj(self, name):
        return InterfaceObj(self, name)

    def addSignal(self, sig, isInputForMaster):
        self.signals.append(sig)
        if(isInputForMaster == "isMasterOutput"):
            self.signalMasterOutput.append(sig)
            self.signalSlaveInput.append(sig)
        elif(isInputForMaster == "isMasterInput"):
            self.signalMasterInput.append(sig)
            self.signalSlaveOutput.append(sig)
        else:
            self.signalMasterInput.append(sig)
            self.signalSlaveInput.append(sig)
    
    def addParameter(self, param):
        self.params.append(param)

    def addRelatedTransaction(self, trType):
        self.trType = trType

    def createFile(self, packageName):
        r = "import "+packageName+"::*;\n\n"
        if(self.params != []):
            r += "interface "+self.typeName+"#(\n"
            for i in range (0, len(self.params)):
                r += "parameter "+self.params[i].type + " "
                if(i == len(self.params)-1):
                    if(self.params[i].value != None):
                        r += self.params[i].name+" = "+self.params[i].value
                    else:
                        r += self.params[i].name
                else:
                    if(self.params[i].value != None):
                        r += self.params[i].name+" = "+self.params[i].value+", \n"
                    else:
                        r += self.params[i].name+",\n"
            r+=");\n"
        else:
            r += "interface "+self.typeName+";\n"

        for sig in self.signals:
            r+="\t"+sig.declare()

        r += "modport master(\n"
        if(self.signalMasterInput != []):
            for i in range(0, len(self.signalMasterInput)):
                r += "input " + self.signalMasterInput[i].name
                if((i == len(self.signalMasterInput)-1) and len(self.signalMasterOutput) == 0):
                    r += ");\n"
                else:
                    r += ",\n"
        if(self.signalMasterOutput != []):
            for i in range(0, len(self.signalMasterOutput)):
                r += "output " + self.signalMasterOutput[i].name
                if(i == len(self.signalMasterOutput)-1):
                    r += ");\n"
                else:
                    r += ",\n"
        r += "modport slave(\n"
        if(self.signalSlaveInput != []):
            for i in range(0, len(self.signalSlaveInput)):
                r += "input " + self.signalSlaveInput[i].name
                if((i == len(self.signalSlaveInput)-1) and len(self.signalSlaveOutput) == 0):
                    r += ");\n"
                else:
                    r += ",\n"
        if(self.signalSlaveOutput != []):
            for i in range(0, len(self.signalSlaveOutput)):
                r += "output " + self.signalSlaveOutput[i].name
                if(i == len(self.signalSlaveOutput)-1):
                    r += ");\n"
                else:
                    r += ",\n"

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


