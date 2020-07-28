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
from jinja2 import Template
import base64
import json
import time
import requests

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
        
        template = Template("{\"Request\": { \
                        \"AccessSubject\": { \
                            \"Attribute\": [ \
                                { \
                                    \"AttributeId\": \"user_id\", \
                                    \"Value\": \"{{ USERNAME }}\", \
                                    \"DataType\": \"string\", \
                                    \"IncludeInResult\": True \
                                }, \
                                { \
                                    \"AttributeId\": \"claim_token\", \
                                    \"Value\": \"{{ CLAIMTOKEN }}\", \
                                    \"DataType\": \"string\", \
                                    \"IncludeInResult\": True \
                                } \
                            ] \
                        }, \
                        \"Action\": [{ \
                            \"Attribute\": [{ \
                                \"AttributeId\": \"action-id\", \
                                \"Value\": \"{{ ACTION }}\" \
                            }] \
                        }], \
                        \"Resource\": [ \
                        {% for resource in RESOURCES %} \
                            {\"Attribute\": [ \
                                { \
                                    \"AttributeId\": \"resource-id\", \
                                    \"Value\": \"{{ resource }}\", \
                                    \"DataType\": \"string\", \
                                    \"IncludeInResult\": True \
                                } \
                            ]} \
                        {% if not loop.last %},{% endif %} \
                        {% endfor %} \
                        ] \
                    } \
                }")
        
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
            userInum = json.loads(decoded)["sub"]
            username = userService.getUserByInum(userInum)
            resourceIDList = context.getResourceIds()
        except:
            print "Protected Access Policy. No claim token passed!"
            return False

        #fill template
        #TODO get action from incoming request?
        jsonForm = eval(template.render(USERNAME = username, CLAIMTOKEN = claimToken, ACTION = "view", RESOURCES = resourceIDList))

        headers={'content-type': "application/json"}
        resp = requests.get(self.pdp_hostname+self.pdp_endpoint, headers=headers, json=jsonForm)
        try:
            pdpReply = resp.json()
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

    def getClaimsGatheringScriptName(self, context):
        return UmaConstants.NO_SCRIPT
