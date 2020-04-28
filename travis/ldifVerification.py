from ldif3 import LDIFParser
from os import sys
import traceback

def import_ldif():
    ldif_mappings = {
        "default": [
            "base.ldif",
            "attributes.ldif",
            "scopes.ldif",
            "scripts.ldif",
            "configuration.ldif",
            "scim.ldif",
            "oxidp.ldif",
            "oxtrust_api.ldif",
            "passport.ldif",
            "oxpassport-config.ldif",
            "gluu_radius_base.ldif",
            "gluu_radius_server.ldif",
            "clients.ldif",
            "oxtrust_api_clients.ldif",
            "scim_clients.ldif",
            "o_metric.ldif",
            "gluu_radius_clients.ldif",
            "passport_clients.ldif",
            "scripts_casa.ldif",
        ]
    }
    exitCode = 0
    for file_ in ldif_mappings["default"]:
        print("Checking {} file...".format(file_))
        src = "./templates/ldif/{}".format(file_)
        try:
            parser = LDIFParser(open(src))
            print("Successfully tested",file_)
        except:
            traceback.print_exc()
            print(file_," validation failed")
            exitCode = -1
        print("--------------------")
    return exitCode

returnCode = import_ldif()
sys.exit(returnCode)
