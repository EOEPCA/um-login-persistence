# oxAuth is available under the MIT License (2008). See http://opensource.org/licenses/MIT for full text.
# Copyright (c) 2017, Gluu
#
# Author: Tiago Fernandes
#

from org.gluu.oxauth.model.uma import UmaConstants
from org.gluu.model.uma import ClaimDefinitionBuilder
from org.gluu.model.custom.script.type.uma import UmaRptPolicyType
from org.gluu.service.cdi.util import CdiUtil
from org.gluu.util import StringHelper, ArrayHelper
from java.util import Arrays, ArrayList, HashSet
from java.lang import String
from org.gluu.oxauth.service import AuthenticationService
from org.gluu.oxauth.service import UserService
import base64
import json
import time
import httplib

class UmaRptPolicy(UmaRptPolicyType):

    def __init__(self, currentTimeMillis):
        self.currentTimeMillis = currentTimeMillis

    def init(self, configurationAttributes):
        print "Protected Access Policy. Initializing ..."
        if not configurationAttributes.containsKey("pdp_hostname"):
            print "Protected Access Policy init error, pdp hostname not specified!"
            return False
        self.pdp_hostname = str(configurationAttributes.get("pdp_hostname").getValue2())

        if not configurationAttributes.containsKey("pdp_endpoint"):
            print "Protected Access Policy init error, pdp endpoint not specified!"
            return False
        self.pdp_endpoint = str(configurationAttributes.get("pdp_endpoint").getValue2())
        print "Protected Access Policy. PDP endpoint set to: " + self.pdp_hostname + self.pdp_endpoint
        print "Protected Access Policy. Initialized successfully"
        return True

    def destroy(self, configurationAttributes):
        print "Protected Access Policy. Destroyed successfully"
        return True

    def getApiVersion(self):
        return 1

    def getRequiredClaims(self, context):
        json = """[
        ]"""
        return ClaimDefinitionBuilder.build(json)

    def authorize(self, context): # context is reference of org.gluu.oxauth.uma.authorization.UmaAuthorizationContext
        print "Protected Access Policy. Authorizing ..."
        
        username=""
        claimToken=""
        resourceIDList=""
        
        authenticationService = CdiUtil.bean(AuthenticationService)
        userService = CdiUtil.bean(UserService)
        
        try:
            claimToken = context.getClaimToken()
            payload = str(claimToken).split(".")[1]
            paddedPayload = payload + '=' * (4 - len(payload) % 4)
            decoded = base64.b64decode(paddedPayload)
            print str(decoded)
            userInum = json.loads(decoded)["sub"]
            tokenExp = int(json.loads(decoded)["exp"])
            print str(tokenExp)
            username = userService.getUserByInum(userInum).getUserId()
            resourceIDList = context.getResourceIds()
        except Exception as e:
            print "Protected Access Policy. No claim token passed!"
            print str(e)
            return False

        if tokenExp < int(time.time()):
            print "Protected Access Policy. Claim token has expired!"
            return False

        #fill request form
        request = {}
        #Add Access Subject with user_id and claim_token attributes
        attribute_user_id = { "AttributeId": "user_id", "Issuer": "", "Value": str(username), "DataType": "string", "IncludeInResult": True }
        attribute_claim_token = {"AttributeId": "claim_token", "Value": str(claimToken), "DataType": "string", "IncludeInResult": True}
        access_subject_attributes = [attribute_user_id, attribute_claim_token]
        accessSubject = {"Attribute": access_subject_attributes}
        access_subject_list = [accessSubject]
        request.update({"AccessSubject": access_subject_list})

        #Add Action, the default is "view" but can easily be extended in the future
        attribute_action_view = {"AttributeId": "action-id", "Value": "view"}
        action_attribute_list = [attribute_action_view]
        attribute_action = {"Attribute": action_attribute_list}
        action_list = [attribute_action]
        request.update({"Action": action_list})

        #Add Resources as a list
        #Each resource contains a list of attributes to characterize it
        #Right now, resources are just characterized by their resource-id. Can be expanded in the future
        resource_list = []
        for resource in resourceIDList:
            resource_attribute_id = {"AttributeId": "resource-id", "Value": str(resource), "DataType": "string", "IncludeInResult": True }
            resource_attribute = {"Attribute": [resource_attribute_id]}
            resource_list.append(resource_attribute)
        request.update({"Resource": resource_list})

        #Build request form in JSON format
        requestForm = {"Request": request}

        #Make request to PDP
        try:
            headers={'content-type': "application/json", "Accept": "text/plain"}
            conn = httplib.HTTPConnection(self.pdp_hostname)
            conn.request("GET", self.pdp_endpoint, body=json.dumps(requestForm), headers=headers)
            resp = conn.getresponse().read()

            try:
                pdpReply = eval(resp)
                decision = str(pdpReply["Response"][0]["Decision"])
                if decision == "Permit":
                    print "Protected Access Policy. Access granted!"
                    return True
                print "Protected Access Policy. Access denied!"
                return False
            except Exception as e:
                print "Protected Access Policy. Exception occured:"
                print str(e)
            return False
        except Exception as e:
            print "Protected Access Policy. Failure to connect to PDP."
            print str(e)
            return False

    def getClaimsGatheringScriptName(self, context):
        return UmaConstants.NO_SCRIPT
