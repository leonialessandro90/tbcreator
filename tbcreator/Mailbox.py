from .Misc import ClassType, ClassObj

class MailboxType(ClassType):

    def __init__(self, typeName):
        ClassType.__init__(self, "mailbox#("+typeName+")")
        self.transactionTypeName = typeName

