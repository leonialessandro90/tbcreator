from .Misc import ClassType, ClassObj
from .Driver import DriverType, DriverObj
from .Monitor import MonitorType, MonitorObj
from .Mailbox import MailboxType
from .Scoreboard import ScoreboardType

class EnvironmentType(ClassType):

    def __init__(self):
        ClassType.__init__(self, "Environment")
        self.drvs = []
        self.mons = []
        self.scb = None
        self.mbsSend = []
        self.mbsExp = []
        self.mbsAct = []
        self.itfs = []

    def setInterfaces(self, itfs):
        self.itfs = itfs

    def setup(self):
        scbType = ScoreboardType()
        for itf in self.itfs:
            itfType = itf.classType
            trType = itfType.trType
            mbType = MailboxType(trType.typeName)
            if(itf.classType.isWrite == True):
                drv = DriverType("Drv_"+itf.name, trType, mbType, itfType).createObj("drv_"+itf.name)
                mbSend = mbType.createObj("mbSend_"+itf.name)
                mbExp = mbType.createObj("mbExp_"+itf.name)
                drv.connectToInterface(itf)
                itf.connectToDriver(drv)
                drv.connectToMailbox(mbSend)
                self.drvs.append(drv)
                self.mbsSend.append(mbSend)
                self.mbsExp.append(mbExp)
                scbType.addExpectedMailbox(mbExp)

            if(itf.classType.isRead == True):
                mon = MonitorType("Mon_"+itf.name, trType, mbType, itfType).createObj("mon_"+itf.name)
                mbAct = mbType.createObj("mbAct_"+itf.name)
                mon.connectToInterface(itf)
                itf.connectToMonitor(mon)
                mon.connectToMailbox(mbAct)
                self.mons.append(mon)
                self.mbsAct.append(mbAct)
                scbType.addActualMailbox(mbAct)
        self.scb = scbType.createObj("scb")



    def createFile(self):
        r = "class "+self.typeName+";\n\n"
        for drv in self.drvs:
            r += drv.declare()
        for mon in self.mons:
            r += mon.declare()
        for mb in self.mbsSend:
            r += mb.declare()
        for mb in self.mbsExp:
            r += mb.declare()
        for mb in self.mbsAct:
            r += mb.declare()
        
        r += self.scb.declare()
        
        r += "\nfunction new(\n"

        for i in range (0, len(self.itfs)):
            r += "\t"+"\t"+"virtual "+self.itfs[i].classType.typeName + " "+self.itfs[i].name
            if(i == len(self.itfs) - 1):
                r += ");\n"
            else:
                r += ",\n"
        r += "\t"+self.scb.initialize()
        for drv in self.drvs:
            r += "\t"+drv.initialize()
        for mon in self.mons:
            r += "\t"+ mon.initialize()
        
        for mb in self.mbsSend:
            r += "\t"+mb.initialize()
        for mb in self.mbsExp:
            r += "\t"+mb.initialize()
        for mb in self.mbsAct:
            r += "\t"+mb.initialize()

        r += "\n"

        for drv in self.drvs:
            r += "\t"+drv.name+".setInterface("+drv.itf.name+");\n"
            r += "\t"+drv.name+".setMailbox("+drv.mb.name+");\n"
        for mon in self.mons:
            r += "\t"+ mon.name+".setInterface("+mon.itf.name+");\n"
            r += "\t"+mon.name+".setMailbox("+mon.mb.name+");\n"
        for mb in self.mbsExp:
            r += "\t"+self.scb.name + ".setMailboxExpected_"+mb.name+"("+mb.name+");\n"
        for mb in self.mbsAct:
            r += "\t"+self.scb.name + ".setMailboxActual_"+mb.name+"("+mb.name+");\n"

        r += "endfunction\n\n"

        r += "task run();\n"
        r += "\t"+"fork\n"
        for drv in self.drvs:
            r += "\t"+"\t"+drv.name+".run();\n"
        for mon in self.mons:
            r += "\t"+"\t"+mon.name+".run();\n"
        r += "\t"+"\t"+self.scb.name + ".run();\n"
        r += "\t"+"join_none\n"
        r += "endtask\n\n"
        r += "endclass\n"

        super(EnvironmentType, self).createFile(r)

