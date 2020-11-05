# oxAuth is available under the MIT License (2008). See http://opensource.org/licenses/MIT for full text.
# Copyright (c) 2016, Gluu
#
# Author: Yuriy Movchan
#

from org.gluu.model.custom.script.type.client import ClientRegistrationType
from org.gluu.service.cdi.util import CdiUtil
from org.gluu.oxauth.service import ScopeService
from org.gluu.util import StringHelper, ArrayHelper
from java.util import Arrays, ArrayList, HashSet

import java

class ClientRegistration(ClientRegistrationType):
    def __init__(self, currentTimeMillis):
        self.currentTimeMillis = currentTimeMillis

    def init(self, configurationAttributes):
        print "Client registration. Initialization"
        
        self.clientRedirectUrisSet = self.prepareClientRedirectUris(configurationAttributes)

        print "Client registration. Initialized successfully"
        return True   

    def destroy(self, configurationAttributes):
        print "Client registration. Destroy"
        print "Client registration. Destroyed successfully"
        return True   

    # Update client entry before persistent it
    #   registerRequest is org.gluu.oxauth.client.RegisterRequest
    #   client is org.gluu.oxauth.model.registration.Client
    #   configurationAttributes is java.util.Map<String, SimpleCustomProperty>
    def createClient(self, registerRequest, client, configurationAttributes):
        print "Client registration. CreateClient method"

        #Temporary workaround for acceptance scripts
        #Forcefully adds the "automated" scope on dynamically registered clients        
        print "Client registration. Adding 'automated' scope"
        automated_inum = "inum=03de78be-34e8-4a77-8af6-384dd90d9fa3,ou=scopes,o=gluu"

        currentScopes = client.getScopes()
        print "Client registration. Current scopes: %s" % currentScopes
        
        if not currentScopes:
            newScopes = [automated_inum]
        else:
            newScopes = ArrayHelper.addItemToStringArray(currentScopes, automated_inum)

        print "Client registration. Result scopes: %s" % newScopes
        client.setScopes(newScopes)

        client.setIncludeClaimsInIdToken(True)

        return True

    # Update client entry before persistent it
    #   registerRequest is org.gluu.oxauth.client.RegisterRequest
    #   client is org.gluu.oxauth.model.registration.Client
    #   configurationAttributes is java.util.Map<String, SimpleCustomProperty>
    def updateClient(self, registerRequest, client, configurationAttributes):
        print "Client registration. UpdateClient method"
        return True

    def getApiVersion(self):
        return 2

    def prepareClientRedirectUris(self, configurationAttributes):
        clientRedirectUrisSet = HashSet()
        if not configurationAttributes.containsKey("client_redirect_uris"):
            return clientRedirectUrisSet

        clientRedirectUrisList = configurationAttributes.get("client_redirect_uris").getValue2()
        if StringHelper.isEmpty(clientRedirectUrisList):
            print "Client registration. The property client_redirect_uris is empty"
            return clientRedirectUrisSet    

        clientRedirectUrisArray = StringHelper.split(clientRedirectUrisList, ",")
        if ArrayHelper.isEmpty(clientRedirectUrisArray):
            print "Client registration. No clients specified in client_redirect_uris property"
            return clientRedirectUrisSet
        
        # Convert to HashSet to quick search
        i = 0
        count = len(clientRedirectUrisArray)
        while i < count:
            uris = clientRedirectUrisArray[i]
            clientRedirectUrisSet.add(uris)
            i = i + 1

        return clientRedirectUrisSet