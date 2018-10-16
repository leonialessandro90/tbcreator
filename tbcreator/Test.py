from .Misc import ClassType
from .Environment import EnvironmentType

class TestType(ClassType):

    def __init__(self):
        ClassType.__init__(self, "Test")
        self.envType = None
        self.itfs = []
        self.itfsIsMasterFromDUTPerspective = []

    def setInterfaces(self, itfs, isMasterFromDUTPerspective):
        self.itfs = itfs
        self.itfsIsMasterFromDUTPerspective = isMasterFromDUTPerspective

    def setup(self):
        self.envType = EnvironmentType()
        self.envType.setInterfaces(self.itfs, self.itfsIsMasterFromDUTPerspective)
        self.envType.setup()


    def createFile(self):
        r = "class Test;\n\n"

        r += self.envType.typeName + " env;\n\n"

        for i in range (0, len(self.itfs)):
            if(self.itfsIsMasterFromDUTPerspective[i]):
                r += "virtual " + self.itfs[i].classType.typeName + ".slave "+self.itfs[i].name+";\n"
            else:
                r += "virtual " + self.itfs[i].classType.typeName + ".master "+self.itfs[i].name+";\n"
        
        r += "\nfunction new(\n"
        for i in range(0, len(self.itfs)):
            if i == len(self.itfs) - 1:
                if self.itfsIsMasterFromDUTPerspective[i]:
                    r += "\t"+"\t"+"virtual " + self.itfs[i].classType.typeName + ".slave " +self.itfs[i].name + ");\n"
                else:
                    r += "\t"+"\t"+"virtual " + self.itfs[i].classType.typeName + ".master " +self.itfs[i].name + ");\n"
            else:
                if self.itfsIsMasterFromDUTPerspective[i]:  
                    r += "\t"+"\t"+"virtual " + self.itfs[i].classType.typeName + ".slave " +self.itfs[i].name + ",\n"
                else:
                    r += "\t"+"\t"+"virtual " + self.itfs[i].classType.typeName + ".master " +self.itfs[i].name + ",\n"
        for itf in self.itfs:
            r += "\t"+"this."+itf.name +" = "+itf.name + ";\n"
        r += "endfunction\n\n"

        r += "task run_test();\n"
        r += "\t"+"env = new(\n"
        
        for i in range(0, len(self.itfs)):
            if i == len(self.itfs) - 1:
                r += "\t"+"\t"+self.itfs[i].name + ");\n"
            else:
                r += "\t"+"\t"+self.itfs[i].name + ",\n"            

        r += "\t"+"env.run();\n"
        r += "\t"+"this.run();\n"
        r += "\t"+"env.scb.finish();\n"
        r += "\t"+"#1000;\n"
        r += "\t"+"$finish;\n"
        r += "endtask\n\n"

        
        for i in range (0, len(self.itfs)):
            itf = self.itfs[i]
            if(self.itfsIsMasterFromDUTPerspective[i] == False):
                r += "task SendTo"+itf.name+"("+itf.classType.trType.typeName+" tr);\n"
                r += "\t"+"this.env.mbSend_"+itf.name+".put(tr);\n"
                r += "\t"+"this.env.mbExp_"+itf.name+".put(tr);\n"
                r += "endtask\n\n"

        r += "virtual task run();\n"
        r += "endtask\n\n"
        r += "endclass"
        super(TestType, self).createFile(r)


