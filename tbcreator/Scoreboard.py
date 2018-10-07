from .Misc import ClassType, ClassObj
from .Transaction import TransactionType

class ScoreboardType(ClassType):

    def __init__(self):
        ClassType.__init__(self, "Scoreboard")
        self.mbExps = []
        self.mbActs = []
        self.trExps = []
        self.trActs = []

    def addExpectedMailbox(self, mbObj):
        self.mbExps.append(mbObj)
        self.trExps.append(TransactionType(mbObj.classType.transactionTypeName).createObj(mbObj.name.replace("mbExp", "trExp")+"_queue"))

    def addActualMailbox(self, mbObj):
        self.mbActs.append(mbObj)
        self.trActs.append(TransactionType(mbObj.classType.transactionTypeName).createObj(mbObj.name.replace("mbAct", "trAct")+"_queue"))
    
    def createFile(self):
        r = "class "+self.typeName+";\n\n"

        for mb in self.mbExps:
            r+=mb.declare()
        for mb in self.mbActs:
            r+=mb.declare()
        
        for tr in self.trExps:
            r += tr.classType.typeName + " " + tr.name + "[$];\n"
        for tr in self.trActs:
            r += tr.classType.typeName + " " + tr.name + "[$];\n"
        
        
        r += "\nfunction new();\n"
        r += "endfunction\n\n"
        
        for mb in self.mbExps:
            r += "function void setMailboxExpected_"+mb.name+"("+mb.classType.typeName+" mb);\n"
            r += "\t"+mb.name + " = mb;\n"
            r += "endfunction\n\n"

        for mb in self.mbActs:
            r += "function void setMailboxActual_"+mb.name+"("+mb.classType.typeName+" mb);\n"
            r += "\t"+mb.name + " = mb;\n"
            r += "endfunction\n\n"

        r += "task run();\n"
        r += "\t"+"fork\n"

        for i in range(0, len(self.mbExps)):
            r += "\t"+"\t"+"forever begin\n"
            r += "\t"+"\t"+"\t"+self.trExps[i].classType.typeName + " tr;\n"
            r += "\t"+"\t"+"\t"+self.mbExps[i].name + ".get(tr);\n"
            r += "\t"+"\t"+"\t"+self.trExps[i].name + ".push_back(tr);\n"
            r += "\t"+"\t"+"\t"+"//USER: YOU WANNA DO SOMETHING MORE?\n"
            r += "\t"+"\t"+"end\n"
        
        for i in range(0, len(self.mbActs)):
            r += "\t"+"\t"+"forever begin\n"
            r += "\t"+"\t"+"\t"+self.trActs[i].classType.typeName + " tr;\n"
            r += "\t"+"\t"+"\t"+self.mbActs[i].name + ".get(tr);\n"
            r += "\t"+"\t"+"\t"+"//USER: "+self.trActs[i].name + ".push_back(tr);\n"
            r += "\t"+"\t"+"\t"+"//USER: PROBABLY YOU WANT TO COMPARE ETC..\n"
            r += "\t"+"\t"+"end\n"

        r += "\t"+"join_none\n"
        r += "endtask\n\n"

        r += "virtual function void finish();\n"
        r += "\t"+"//USER: CHECK WHETHER EVERYTHING IS OK (EMPTY QUEUES,...)\n"
        r += "endfunction\n\n"

        r += "endclass"
        super(ScoreboardType, self).createFile(r)
