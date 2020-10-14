# oxAuth is available under the MIT License (2008). See http://opensource.org/licenses/MIT for full text.
# Copyright (c) 2017, Gluu
#
# Author: Jose Gonzalez
# Adapted from previous 3.0.1 script of Yuriy Movchan
#
# oxConfigurationProperty required:
#   allowed_clients - comma separated list of dns of allowed clients
#   (i.e. the SCIM RP client)

from org.gluu.oxauth.model.uma import UmaConstants
from org.gluu.model.uma import ClaimDefinitionBuilder
from org.gluu.model.custom.script.type.uma import UmaRptPolicyType
from org.gluu.service.cdi.util import CdiUtil
from org.gluu.util import StringHelper, ArrayHelper
from java.util import Arrays, ArrayList, HashSet
from java.lang import String
from org.gluu.oxauth.service import ClientService

class UmaRptPolicy(UmaRptPolicyType):

    def __init__(self, currentTimeMillis):
        self.currentTimeMillis = currentTimeMillis

    def init(self, configurationAttributes):
        print "RPT Policy. Initializing ..."
        self.clientsSet = self.prepareClientsSet(configurationAttributes)
        print "RPT Policy. Initialized successfully"
        return True

    def destroy(self, configurationAttributes):
        print "RPT Policy. Destroyed successfully"
        return True

    def getApiVersion(self):
        return 1

    def getRequiredClaims(self, context):
        json = """[
        ]"""
        return ClaimDefinitionBuilder.build(json)

    def authorize(self, context): # context is reference of org.gluu.oxauth.uma.authorization.UmaAuthorizationContext
        print "RPT Policy. Authorizing ..."

        client_id=context.getClient().getClientId()
        print "UmaRptPolicy. client_id = %s" % client_id
        
        # Temporary Workaround to allow for Automated EOEPCA Acceptance tests
        # [workaround]
        clientService = CdiUtil.bean(ClientService)
        automated_inum = "inum=03de78be-34e8-4a77-8af6-384dd90d9fa3,ou=scopes,o=gluu"
        try:
            #get scopes associated with client
            client_scopes = clientService.getClient(client_id).getScopes()
            print "Client scopes are: " + str(client_scopes)
            #check for presence of "automated" scope
            #this is a temporary, special operator that simply indicates this client is part of
            # automated testing
            if client_scopes and not ArrayHelper.isEmpty(client_scopes):
                for scope in client_scopes:
                    if automated_inum in scope:
                        print "UmaRptPolicy. Client is automated!"
                        return True
            
        except:
            print "UmaRptPolicy. Error reading scopes!"
            return False
        # [/workaround]

        if (StringHelper.isEmpty(client_id)):
            return False
     
        if (self.clientsSet.contains(client_id)):
            print "UmaRptPolicy. Authorizing client"
            return True
        else:
            print "UmaRptPolicy. Client isn't authorized"
            return False

    def getClaimsGatheringScriptName(self, context):
        return UmaConstants.NO_SCRIPT

    def prepareClientsSet(self, configurationAttributes):
        clientsSet = HashSet()
        if (not configurationAttributes.containsKey("allowed_clients")):
            return clientsSet

        allowedClientsList = configurationAttributes.get("allowed_clients").getValue2()
        if (StringHelper.isEmpty(allowedClientsList)):
            print "UmaRptPolicy. The property allowed_clients is empty"
            return clientsSet    

        allowedClientsListArray = StringHelper.split(allowedClientsList, ",")
        if (ArrayHelper.isEmpty(allowedClientsListArray)):
            print "UmaRptPolicy. No clients specified in allowed_clients property"
            return clientsSet
        
        # Convert to HashSet to quick search
        i = 0
        count = len(allowedClientsListArray)
        while (i < count):
            client = allowedClientsListArray[i]
            clientsSet.add(client)
            i = i + 1

        return clientsSet
