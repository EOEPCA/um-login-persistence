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
        
        #TODO get hostname + endpoint from global variables in persistence
        PDPhostname=""
        PDPendpoint=""
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
        resp = requests.get(PDPhostname+PDPendpoint, headers=headers, json=jsonForm)
        #resp = True
        
        if resp:
            print "Protected Access Policy. Access granted!"
        else:
            print "Protected Access Policy. Access denied!"
        return resp

    def getClaimsGatheringScriptName(self, context):
        return UmaConstants.NO_SCRIPT

## BELOW IS SOLELY FOR DEBUGGING PURPOSES - TO BE DELETED
# template = Template("{\"Request\": { \
#                         \"AccessSubject\": { \
#                             \"Attribute\": [ \
#                                 { \
#                                     \"AttributeId\": \"user_id\", \
#                                     \"Value\": \"{{ USERNAME }}\", \
#                                     \"DataType\": \"string\", \
#                                     \"IncludeInResult\": True \
#                                 }, \
#                                 { \
#                                     \"AttributeId\": \"claim_token\", \
#                                     \"Value\": \"{{ CLAIMTOKEN }}\", \
#                                     \"DataType\": \"string\", \
#                                     \"IncludeInResult\": True \
#                                 } \
#                             ] \
#                         }, \
#                         \"Action\": [{ \
#                             \"Attribute\": [{ \
#                                 \"AttributeId\": \"action-id\", \
#                                 \"Value\": \"{{ ACTION }}\" \
#                             }] \
#                         }], \
#                         \"Resource\": [ \
#                         {% for resource in RESOURCES %} \
#                             {\"Attribute\": [ \
#                                 { \
#                                     \"AttributeId\": \"resource-id\", \
#                                     \"Value\": \"{{ resource }}\", \
#                                     \"DataType\": \"string\", \
#                                     \"IncludeInResult\": True \
#                                 } \
#                             ]} \
#                         {% if not loop.last %},{% endif %} \
#                         {% endfor %} \
#                         ] \
#                     } \
#                 }")
# print(template.render(USERNAME = "Tiago", CLAIMTOKEN = "ABCD1234", ACTION = "view", RESOURCES = [1,2]))
# print(eval(template.render(USERNAME = "Tiago", CLAIMTOKEN = "ABCD1234", ACTION = "view", RESOURCES = [1,2])))