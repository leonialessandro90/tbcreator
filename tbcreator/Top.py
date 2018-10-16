from .Test import TestType
from .TestCase import TestCaseType
from .Misc import ClassType, ClassObj
import os

class Top(ClassType):

    def __init__(self, package, dut, outputDir):
        ClassType.__init__(self, "Top")
        self.testType = None
        self.testCaseType = None
        self.itfs = dut.itfs
        self.itfIsMasterFromDUTPerspective = dut.itfIsMaster
        self.dut = dut
        self.pkg = package

        self.testType = TestType()
        self.testType.setInterfaces(self.itfs, self.itfIsMasterFromDUTPerspective)
        self.testType.setup()
        self.testCaseType = TestCaseType(self.testType)

        
        ClassType.outputDir = os.path.join(outputDir, "db","tb")
        if(not os.path.exists(ClassType.outputDir)):
            os.makedirs(ClassType.outputDir)
        if(not os.path.exists(os.path.join(ClassType.outputDir,"tests"))):
            os.makedirs(os.path.join(ClassType.outputDir,"tests"))
    
    def addInterface(self, itfObj):
        self.itfs.append(itfObj)

    def createFile(self):
        r = "import "+self.pkg.typeName+"::*;\n\n"
        r += "module Top;\n\n"
        r += "bit clk;\n"
        r += "bit rst;\n\n"

        for itf in self.itfs:
            r += itf.instantiate()
        
        for itf in self.itfs:
            r += "assign "+itf.name+".clk = clk;\n"
            r += "assign "+itf.name+".rst = rst;\n"
        r += "\n\n"

        r += self.dut.instantiate()

        r += "initial begin \n"
        r += "\t"+"clk = 1'b0;\n"
        r += "\t"+"rst = 1'b1;\n"
        r += "\t"+"#(CLOCK_PERIOD) rst = 1'b0;\n"
        r += "end\n\n"

        r += "always #(CLOCK_PERIOD/2) clk = ~clk;\n\n\n"

        r += "initial begin\n"
        r += "\t"+"Test test;\n"
        r += "\t"+"string test_name;\n"
        r += "\t"+"void'($value$plusargs(\"testname=%s\",test_name));\n"
        r += "\t"+"case(test_name)\n"
        r += "\t"+"\t"+"\"Test01\" : begin\n"
        r += "\t"+"\t"+"\t"+"automatic Test01 t = new("

        for i in range(0, len(self.itfs)):
            if i != len(self.itfs)-1:
                if(self.itfIsMasterFromDUTPerspective[i]):
                    r += self.itfs[i].name+".slave,"
                else:
                    r += self.itfs[i].name+".master,"                
            else:
                if(self.itfIsMasterFromDUTPerspective[i]):
                    r += self.itfs[i].name+".slave);\n"
                else:
                    r += self.itfs[i].name+".master);\n"


        r += "\t"+"\t"+"\t"+"test = t;\n"
        r += "\t"+"\t"+"end\n"
        r += "\t"+"endcase\n"
        r += "\t"+"test.run_test();\n"
        r += "end\n\n"
        
        r += "endmodule"

        super(Top, self).createFile(r)


    def createFiles(self):

        for itf in self.itfs:
            itf.classType.createFile(self.pkg.typeName)
            itf.classType.trType.createFile()
            self.pkg.addIncludeFile(itf.classType.trType.typeName+".sv")
            self.pkg.addInterface(itf.classType.typeName)

        for drv in self.testType.envType.drvs:
            drv.classType.createFile()
            self.pkg.addIncludeFile(drv.classType.typeName+".sv")
        for mon in self.testType.envType.mons:
            mon.classType.createFile()
            self.pkg.addIncludeFile(mon.classType.typeName+".sv")
        
        self.testType.envType.scb.classType.createFile()
        self.pkg.addIncludeFile(self.testType.envType.scb.classType.typeName + ".sv")

        self.testType.envType.createFile()
        self.pkg.addIncludeFile(self.testType.envType.typeName+".sv")

        self.testType.createFile()
        self.pkg.addIncludeFile(self.testType.typeName+".sv")

        self.testCaseType.createFile()
        self.pkg.addIncludeFile("tests/"+self.testCaseType.typeName + ".sv")

        self.createFile()
        self.pkg.createFile()

        