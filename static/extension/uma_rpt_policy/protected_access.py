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
import requests

class UmaRptPolicy(UmaRptPolicyType):

    def __init__(self, currentTimeMillis):
        self.currentTimeMillis = currentTimeMillis

    def init(self, configurationAttributes):
        print "Protected Access Policy. Initializing ..."
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
        
        template = {"Request": { \
                        "User": { \
                            "Attribute": [ \
                                { \
                                    "AttributeId": "%HOSTNAME%/identity/user/user_name", \
                                    "Value": "%USERNAME%", \
                                    "DataType": "string", \
                                    "IncludeInResult": True \
                                }, \
                                { \
                                    "AttributeId": "claim_token", \
                                    "Value": "%CLAIMTOKEN%", \
                                    "DataType": "string", \
                                    "IncludeInResult": True \
                                } \
                            ] \
                        }, \
                        "Resource": { \
                            "Attribute": [ \
                                { \
                                    "AttributeId": "resource-id", \
                                    "Value": "%RESOURCEID%", \
                                    "DataType": "string", \
                                    "IncludeInResult": True \
                                } \
                            ] \
                        } \
                    } \
                }
                
        hostname=""
        username=""
        claimToken=""
        resourceID=""
        
        authenticationService = CdiUtil.bean(AuthenticationService)
        userService = CdiUtil.bean(UserService)
        
        try:
            claimToken = context.getClaimToken()
            payload = str(claimToken).split(".")[1]
            paddedPayload = payload + '=' * (4 - len(payload) % 4)
            decoded = base64.b64decode(paddedPayload)
            userInum = json.loads(decoded)["sub"]
            username = userService.getUserByInum(userInum)
            resourceID = context.getResourceIds()[0]
            #TODO Get hostname
        except:
            print "Protected Access Policy. No claim token passed!"
            return False

        templateString=str(template)
        filledTemplate=templateString.replace("%HOSTNAME%",hostname)
        filledTemplate=filledTemplate.replace("%USERNAME%",username)
        filledTemplate=filledTemplate.replace("%CLAIMTOKEN%",claimToken)
        filledTemplate=filledTemplate.replace("%RESOURCEID%",resourceID) #This assumes only 1 resource. Probably needs an a specific template engine to implement multiple resources
        
        jsonForm=eval(filledTemplate)

        #TODO Elaborate request to PDP and get True or False as reply
        headers=""
        payload="{'jsonForm': "+ jsonForm +"}"
        resp = True
        
        if not resp:
            print "Protected Access Policy. Access denied!"
            return False
        else:
            print "Protected Access Policy. Access granted!"
            return True

    def getClaimsGatheringScriptName(self, context):
        return UmaConstants.NO_SCRIPT
