from flask import Flask, request, jsonify, send_from_directory
from bluemix_service_discovery.service_publisher import ServicePublisher
import os, json
execfile('routes/orders.py')

vcap_application = json.loads(os.getenv('VCAP_APPLICATION'))
port = vcap_application['port']
my_url = vcap_application['application_uris'][0]
#port = int(os.getenv('VCAP_APP_PORT', 8080))
#my_url = os.getenv('VCAP_APPLICATION')['application_uris'][0]

# Setup Service Registry
sd_publisher = ServicePublisher('Orders', 300, 'UP',
                             'https://' + my_url, 'http',
                             tags=['test'])
sd_publisher.register_service(True)


app = Flask(__name__, static_url_path='')
@app.route('/')
@app.route('/<path:path>')
def index(path=None):
  if not path:
    path='index.html'
  app._static_folder = os.path.abspath("www/")
  return app.send_static_file(path)

@app.route('/rest/')
@app.route('/rest/orders', methods=['POST'])
def orders():
  j = request.get_json(silent=True)
  if not j:
    resp = jsonify({"msg": "Could not find json input in %s " % request.data})
    resp.status_code = 400
    return resp
    
  if not all (k in j for k in ("customerid","itemid","count")):
    resp = jsonify({"msg": "Missing some fields"})
    resp.status_code = 400
    return resp
    
  customerid = j['customerid']
  itemid = j['itemid']
  count = int(j['count'])
  return place_order(customerid=customerid, itemid=itemid, count=count)

@app.route('/rest/orders', methods=['GET'])
def get_all_orders():
  return list_orders()

@app.route('/rest/orders/<orderid>', methods=['GET'])
def search_order(orderid=None):
  return get_order(orderid)
  

app.run(host='0.0.0.0', port=port) 
