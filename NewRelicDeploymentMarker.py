#!/usr/bin/python
import requests, json, os, argparse

# Get API key if it is in shell environment
APIKEY = os.getenv('NR_APIKEY')

# Create the argument parser
parser = argparse.ArgumentParser(description='Insert a Deployment Marker in New Relic. Uses sample text and auto-increments revision ID')
parser.add_argument("-k", "--key", action='store', dest='key', help="New Relic API Key. Overrides the environment variable NR_APIKEY if it exists")
args = parser.parse_args()

if args.key:
  APIKEY=args.key
  
if not APIKEY:
    parser.print_help()
    print ""
    print "Error: No New Relic API Key found. "
    print "Please set key in environment variable NR_APIKEY or as application argument"
    print ""
    exit()

print "New Relic API Key set to " + APIKEY


# Get a list of the applications reporting to New Relic
r = requests.get('https://api.newrelic.com/v2/applications.json', headers={"X-Api-Key": APIKEY})
if r.status_code != 200:
  exit("Error communicating with NewRelic API: " + r.text)

# Get the application ID for the MicroservicesCatalogAPI
for application in r.json()['applications']:
  if application['name'] == 'MicroservicesCatalogAPI':
    application_id=application['id']

if not 'application_id' in globals():
  exit("Could not find NewRelic Application ID for MicroservicesCatalogAPI. Make sure application is started and reporting status")

# Get the last deployment revision
maxrev = 0
r = requests.get('https://api.newrelic.com/v2/applications/' + str(application_id) + '/deployments.json', headers={"X-Api-Key": APIKEY})
for d in r.json()['deployments']:
  if int(d['revision']) > int(maxrev):
    maxrev = int(d['revision'])

# Build the deployment info to post
revision = maxrev + 1
payload = {
  "deployment": {
    "revision": revision,
    "changelog": "http://some.url/changelogs/rev" + str(revision),
    "description": "Update XYZ https://github.com/hassenius/MicroservicesShop/commit/dda0891ea7e2b29fbace8ccc6a8e44aef65e2f1e",
    "user": "Ada Lovelace"
  }
}

# Post the deployment info
r = requests.post('https://api.newrelic.com/v2/applications/' + str(application_id) + '/deployments.json', headers={"X-Api-Key": APIKEY, 'Content-Type': 'application/json'}, data=json.dumps(payload))

if r.status_code == 201:
  print "Successfully inserted deployment marker with revision " + str(revision)
else:
  print "Failed to update deployment"
  print r.text
