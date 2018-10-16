from tbcreator import *

##################################################################################
########################### PHASE 1: PACKAGE CREATION ############################
##################################################################################
## Define the name of the package and its parameters.                           ##
##################################################################################
pkg = Package("MyPackage")
pkg.addParameter(Parameter("int","DWIDTH","8","Width of the data bus"))


##################################################################################
######################### PHASE 2: TRANSACTIONS CREATION #########################
##################################################################################
## Create Transaction types and add Attributes to each one.                     ##
## Queues or unpacked arrays can be implemented using the "postName" argument.  ##
## For other types the "postName" argument must be the empty string.            ##
##################################################################################
trWrType = TransactionType("TrPacketWrite")
trWrType.addAttribute(Attribute("logic[DWIDTH-1:0]","pkt","[$]","{}"))

trRdType = TransactionType("TrPacketRead")
trRdType.addAttribute(Attribute("logic[DWIDTH-1:0]","pkt","[$]","{}"))
trRdType.addAttribute(Attribute("logic","error","","1'b0"))

trAXIType = TransactionType("TrAXI")
trAXIType.addAttribute(Attribute("logic[31:0]", "pkt", "[$]", "{}"))
##################################################################################
####################### PHASE 3: INTERFACE TYPES CREATION ########################
##################################################################################
## Create the interface types.                                                  ##
## The isRead field, if True, means that a Monitor will be attached to it, so   ##
##     the TB will read transactions from that interface;                       ##
## The isWrite field, if True, means that a Driver will be attached to it, so   ##
##     the TB will write transaction to that interface;                         ##
## An interface type cannot have at the same time isRead and isWrite to True    ##
## An interface type is automatically created with two signals: "clk" and "rst" ##
## The user can add custom signals to it specifying type, name and direction    ##
## The direction can be "in" (a Driver or Monitor reads the signal) or          ##
##     "out" (a Driver or Monitor reads the signal)                             ##
## Because the parameterizable interfaces are not supported (they are a hell    ##
##      to implement with virtual interfaces), the parameters are taken from    ##
##      the package file that is automatically included.                        ##
## AXIFull and AXILite interfaces are available by default                      ##
##################################################################################
itfWrType = InterfaceType("InterfaceWriteType")
itfWrType.addSignal(Signal("logic[DWIDTH-1:0]","wwdata","in"), "isMasterOutput")
itfWrType.addSignal(Signal("logic[DWIDTH-1:0]","wwe","in"), "isMasterOutput")
itfWrType.addSignal(Signal("logic[DWIDTH/2-1:0]","wrdata","in"), "isMasterInput")
itfWrType.addSignal(Signal("logic[DWIDTH/2-1:0]","wre","in"), "isMasterInput")
itfWrType.addRelatedTransaction(trWrType)

itfRdType = InterfaceType("InterfaceReadType")
itfRdType.addSignal(Signal("logic[DWIDTH-1:0]","rdata","out"), "isMasterOutput")
itfRdType.addSignal(Signal("logic","error","out"), "isMasterOutput")
itfRdType.addRelatedTransaction(trRdType)

itfAXIFullType = InterfaceType.createAXIFull()
itfAXIFullType.addRelatedTransaction(trAXIType)

itfAXILiteType = InterfaceType.createAXILite()
itfAXILiteType.addRelatedTransaction(trAXIType)

##################################################################################
########################## PHASE 4: INTERFACES CREATION ##########################
##################################################################################
## For each interface type more than one interface can be created               ##
##################################################################################
itfWr0 = itfWrType.createObj("itfWr0")
itfWr1 = itfWrType.createObj("itfWr1")

itfRd0 = itfRdType.createObj("itfRd0")
itfRd1 = itfRdType.createObj("itfRd1")

itfAXIFullLeft = itfAXIFullType.createObj("itfAXIFullLeft")
itfAXIFullRight = itfAXIFullType.createObj("itfAXIFullRight")

itfAXILiteSlave = itfAXILiteType.createObj("itfAXILiteSlave")

##################################################################################
############################# PHASE 5: DUT CREATION ##############################
##################################################################################
## Create DUT, specifying the name of the type (the name of its instante will   ##
##     be set automatically to "dut")                                           ##
## If the DUT has paramenters, set them specifying the value at which they are  ##
##     initialized. If they are initialized with a paramter coming from the     ##
##     package, set the name of the parameter as its value.                     ##
## The DUT must then be connected to the interfaces. If the DUT has spare       ##
##     signals not grouped in interfaces, the Top.sv file must be manually      ##
##     changed.                                                                 ##
## The "clk" and "rst" signals are automatically added to the DUT in addition   ##
##     to the interfaces.                                                       ##
##################################################################################
dut = DUT("MY_DUT_TYPE")
dut.addParameter(Parameter("int","DWIDTH"), "DWIDTH")
dut.addParameter(Parameter("bit","RESET_POLARITY"), "1'b1")
dut.connectInterface("dutItfWr0", itfWr0, "Slave")
dut.connectInterface("dutItfWr1", itfWr1, "Master")
dut.connectInterface("dutItfRd0", itfRd0, "Master")
dut.connectInterface("dutItfRd1", itfRd1, "Slave")
dut.connectInterface("dutAXIFullLeft", itfAXIFullLeft, "Slave")
dut.connectInterface("dutAXIFullRight", itfAXIFullRight, "Master")
dut.connectInterface("dutAXILiteSlave", itfAXILiteSlave, "Slave")


##################################################################################
########################### PHASE 6: TB TOP CREATION #############################
##################################################################################
## Create the Top file of the testbench.                                        ##
## The top requires the previously created package, DUT and the name of the     ##
##     folder where to put the files to be generated.                           ##
##################################################################################
top = Top(pkg, dut, "out")


##################################################################################
################### PHASE 7: TB AND SOURCE FILES GENERATION ######################
##################################################################################
## The tb and source files to be generated are:                                 ##
## 1. testbench files, mandatory and to be called as first;                     ##
## 2. a DUT dummy source file, used just to be able to compile and simulate.    ##
##      If not needed, this step can be skipped;                                ##
##################################################################################
top.createFiles()
dut.createDummyFile()

##################################################################################
##################### PHASE 8: QUESTASIM FILES GENERATION ########################
##################################################################################
## It is possible to generate some python scripts to compile and simulate the   ##
##     verification environment with Questasim/Modelsim.                        ##
## In order to do so, a Questasim object has to be created, initialized with    ##
##     the package previously created. The name of each source file must be     ##
##     added to it, if the dummy DUT is used it is just the dummy source file.  ##
## The scripts generated, in the "questasim" folder, are:                       ##
## 1. compile.py: to be run without arguments, it compiles all tb and source    ##
##     files;                                                                   ##
## 2. simulate.py: needs the name of the test case as argument (without ".sv"). ##
##     top.createFiles() automatically creates Test01 in db/tb/tests/           ## 
##################################################################################
sim = Questasim(pkg)
sim.addSourceFile("MY_DUT_TYPE.sv")
sim.createFiles()