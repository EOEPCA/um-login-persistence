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

class UmaRptPolicy(UmaRptPolicyType):

    def __init__(self, currentTimeMillis):
        self.currentTimeMillis = currentTimeMillis

    def init(self, configurationAttributes):
        print "Authenticated RPT Policy. Initializing ..."
        print "Authenticated RPT Policy. Initialized successfully"
        return True

    def destroy(self, configurationAttributes):
        print "Authenticated RPT Policy. Destroyed successfully"
        return True

    def getApiVersion(self):
        return 1

    def getRequiredClaims(self, context):
        json = """[
        ]"""
        return ClaimDefinitionBuilder.build(json)

    def authorize(self, context): # context is reference of org.gluu.oxauth.uma.authorization.UmaAuthorizationContext
        print "Authenticated RPT Policy. Authorizing ..."
        authenticationService = CdiUtil.bean(AuthenticationService)
        userService = CdiUtil.bean(UserService)

        try:
            claim_token = context.getClaimToken()
            payload = str(claim_token).split(".")[1]
            paddedPayload = payload + '=' * (4 - len(payload) % 4)
            decoded = base64.b64decode(paddedPayload)
            userInum = json.loads(decoded)["sub"]
            tokenExp = int(json.loads(decoded)["exp"])
            user = userService.getUserByInum(userInum)
            logged_in = authenticationService.authenticate(user.getUserId())
        except:
            print "Authenticated RPT Policy. No claim token passed!"
            return False

        if tokenExp < int(time.time()):
             print "Authenticated RPT Policy. Claim token has expired!"
             return False

        print "Authenticated RPT Policy. Logged in: " + str(logged_in)

        if not logged_in:
            print "Authenticated RPT Policy. User is not authenticated!"
            #clientId = context.getConfigurationAttributes().get("client_id").getValue2()
            #redirectUri = context.getClaimsGatheringEndpoint() + "?authentication=true"
            #authorizationUrl = context.getAuthorizationEndpoint() + "?client_id=" + clientId + "&redirect_uri=" + redirectUri + "&scope=openid&response_type=code"
            #context.redirectToExternalUrl(authorizationUrl)
            return False
        else:
            print "Authenticated RPT Policy. User is authenticated."
            return True

    def getClaimsGatheringScriptName(self, context):
        return UmaConstants.NO_SCRIPT
