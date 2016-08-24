from flask import Flask, request, jsonify, send_from_directory
import os
execfile('routes/orders.py')
app = Flask(__name__, static_url_path='')

port = int(os.getenv('VCAP_APP_PORT', 8080))
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
