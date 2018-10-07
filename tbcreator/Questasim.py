import os
from .Misc import ClassType

class Questasim(ClassType):

    def __init__(self, package):
        ClassType.__init__(self, "Questasim")
        self.srcs = []
        self.packageName = package.typeName

    def addSourceFile(self, filenameInside_db_src):
        self.srcs.append(filenameInside_db_src)

    def createFiles(self):
        db = os.path.split(ClassType.outputDir)[0]
        root, db = os.path.split(db)
        questaDir = os.path.join(root,"questasim")
        if(not os.path.exists(questaDir)):
            os.makedirs(questaDir)
        
        # create compile.py
        r = ""
        r += "import os\n\n"
        r += "src = ''\n"

        for src in self.srcs:
            r += "src += '../db/src/" + src + "'\n"
        
        r += "\n"
        r += "tb = ''\n"
        r += "tb += '../db/tb/" + self.packageName + ".sv'\n\n"
        r += "top = '../db/tb/Top.sv'\n\n"

        r += "cmd = 'vlog -mixedsvvh ' + tb + ' -work work'\n"
        r += "os.system(cmd)\n"
        r += "cmd = 'vlog -mixedsvvh ' + src + ' -work work +incdir+../db/tb/'\n"
        r += "os.system(cmd)\n"
        r += "cmd = 'vlog -mixedsvvh ' + top + ' -work work'\n"
        r += "os.system(cmd)\n"

        F = open(os.path.join(questaDir,"compile.py"), "w")
        F.write(r)
        F.close()

        # Simulate.py
        r = "import os\n"
        r += "import sys\n\n"
        r += "cmd = 'vsim -novopt -c -do \"do batch.tcl ' + sys.argv[1]+ '\"'\n"
        r += "os.system(cmd)\n"


        F = open(os.path.join(questaDir,"simulate.py"), "w")
        F.write(r)
        F.close()

        # Batch.tcl
        r = "set TEST_NAME $1\n\n"
        r += "vsim -wlf vsim.wlf -t 1ps Top +testname=${TEST_NAME}\n"
        r += "log -r /*\n"
        r += "run -all\n"
        r += "exit"

        F = open(os.path.join(questaDir,"batch.tcl"), "w")
        F.write(r)
        F.close()
        #

