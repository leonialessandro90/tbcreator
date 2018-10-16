from .Misc import ClassType
import os

class TestCaseType(ClassType):

    def __init__(self, testType):
        ClassType.__init__(self, "Test01")
        self.testType = testType

    def createFile(self):
        r = ""
        r += "class Test01 extends Test;\n\n"
        r += "\nfunction new(\n"
        for i in range(0, len(self.testType.itfs)):
            if i == len(self.testType.itfs) - 1:
                if(self.testType.itfsIsMasterFromDUTPerspective[i]):
                    r += "\t"+"\t"+"virtual " + self.testType.itfs[i].classType.typeName + ".slave " +self.testType.itfs[i].name + ");\n"
                else:
                    r += "\t"+"\t"+"virtual " + self.testType.itfs[i].classType.typeName + ".master " +self.testType.itfs[i].name + ");\n"

            else:
                if(self.testType.itfsIsMasterFromDUTPerspective[i]):
                    r += "\t"+"\t"+"virtual " + self.testType.itfs[i].classType.typeName + ".slave " +self.testType.itfs[i].name + ",\n"
                else:
                    r += "\t"+"\t"+"virtual " + self.testType.itfs[i].classType.typeName + ".master " +self.testType.itfs[i].name + ",\n"
        r += "\t"+"super.new(\n"
        for i in range(0, len(self.testType.itfs)):
            if i == len(self.testType.itfs) - 1:
                r += "\t"+"\t"+self.testType.itfs[i].name + ");\n"
            else:
                r += "\t"+"\t"+self.testType.itfs[i].name + ",\n"

        r += "endfunction\n\n"

        r += "virtual task run();\n"
        r += "\t"+"//USER: Fill this task with your test.\n"
        r += "\t"+"//USER: What follows is an example.\n\n"
        i = 0
        for j in range (0, len(self.testType.itfs)):
            itf = self.testType.itfs[j]
            dutIsMaster = self.testType.itfsIsMasterFromDUTPerspective[j]
            if(dutIsMaster == False):
                trType = itf.classType.trType
                r += "\t"+trType.typeName + " tr_"+str(i)+" = new();\n"
                r += "\t"+"//USER: Fill the transaction fields.\n"
                for attr in trType.attributes:
                    r += "\t"+"//USER: tr_"+str(i)+"."+attr.name + " (" + attr.type+")\n"
                i = i+1
                r += "\n"

        i = 0
        for j in range(0, len(self.testType.itfs)):
            itf = self.testType.itfs[j]
            if(self.testType.itfsIsMasterFromDUTPerspective[j] == False):
                trType = itf.classType.trType
                r += "\t"+"SendTo"+itf.name+"(tr_"+str(i)+");\n"
                i = i + 1
        r += "endtask\n\n"

        r += "endclass"

        super(TestCaseType, self).createFile(r,"tests")
