from org.gluu.model.custom.script.type.uma import UmaRptPolicyType

class UmaRptPolicy(UmaRptPolicyType):
    def __init__(self, currentTimeMillis):
        self.currentTimeMillis = currentTimeMillis

    def init(self, configurationAttributes):
        print "Open Policy. Initializing ..."
        print "Open Policy. Initialized successfully"
        return True

    def destroy(self, configurationAttributes):
        print "Open Policy. Destroying ..."
        print "Open Policy. Destroyed successfully"
        return True

    def getApiVersion(self):
        return 1

    def authorize(self, context):
        print "Authorized successfully!"
        return True