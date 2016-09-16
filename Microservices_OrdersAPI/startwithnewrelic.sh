#!/bin/sh
#################################################################
##################################################################
#
# startwithnewrelic.sh by Hans Kristian Moen
# 
# To auto-instrument python apps running in CloudFoundry / Bluemix
# in manifest.yaml file for python application add the line
# command: ./startwithnewrelic.sh <application.py>
#
# License: MIT
##################################################################
#################################################################


# Pull license key from VCAP if New Relic is bound to application
VCAP_KEY=$(python -c 'import json,os; vcap=json.loads(os.environ.get("VCAP_SERVICES")); print str(vcap["newrelic"][0]["credentials"]["licenseKey"])')

# Pull app name from VCAP
VCAP_APP_NAME=$(python -c 'import json,os; vcap=json.loads(os.environ.get("VCAP_APPLICATION")); print str(vcap["application_name"])')

# Prefer CF ENV variables over VCAP variables
key=${NEW_RELIC_LICENSE_KEY:-$VCAP_KEY}
app_name=${NEW_RELIC_APP_NAME:-$VCAP_APP_NAME}

# Generate standard config file
newrelic-admin generate-config ${key} newrelic.ini


export NEW_RELIC_CONFIG_FILE=newrelic.ini 
echo "Set newrelic app name to ${app_name}"
echo "Set newrelic license key to ${key}"
echo "Set newrelic config file to ${NEW_RELIC_CONFIG_FILE}"
newrelic-admin run-python $@


