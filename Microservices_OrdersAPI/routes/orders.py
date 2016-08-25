import os, json, pymysql, pymysql.cursors


# Get mysql connectivity info from VCAP_SERVICES
if os.environ.get('VCAP_SERVICES'):
  vcap_services = json.loads(os.environ.get('VCAP_SERVICES'))
  if vcap_services.has_key('user-provided'):
    for service in vcap_services['user-provided']:
      if service['name'] == 'mysql-OrdersDBService':
        mysql = service['credentials']
else:
  # Probably not launched in a CF environment
  quit('Could not find VCAP_SERVICES environment')

if not mysql:
  quit('Error: Could not find mysql credentials. Make sure the user-provided services is bound to the application')
  
connection = pymysql.connect(host=str(mysql['host']), port=int(mysql['port']), user=str(mysql['user']), password=str(mysql['password']), db=str(mysql['db']), cursorclass=pymysql.cursors.DictCursor)

def connect():
  global mysql, connection
  connection = pymysql.connect(host=str(mysql['host']), port=int(mysql['port']), user=str(mysql['user']), password=str(mysql['password']), db=str(mysql['db']), cursorclass=pymysql.cursors.DictCursor)

def table_exist():
  global connection
  if not connection.open:
    connect()
  cursor = connection.cursor()
  cursor.execute("SHOW TABLES LIKE 'orders'")
  result = cursor.fetchone()
  cursor.close()
  return result

def create_table():
  global connection
  if not connection.open:
    connect()
  cursor = connection.cursor()
  sql = 'CREATE TABLE IF NOT EXISTS orders (id int(11) NOT NULL AUTO_INCREMENT, itemid varchar(32), customerid varchar(32), count int(11), PRIMARY KEY (id) )'
  cursor.execute(sql)
  connection.commit()
  cursor.close()
  return True
  

def place_order(itemid=None, customerid=None, count=None):
  global connection
  if not connection.open:
    connect()
  cursor = connection.cursor()
  try:
    sql = 'INSERT INTO orders (itemid, customerid, count) VALUES (%s, %s, %s)'
    af = cursor.execute(sql, (str(itemid), str(customerid), int(count),) )
    connection.commit()
    msg = {"msg": "Successfully created your order"}
    resp = jsonify(msg)
    resp.status_code = 201
  except (pymysql.ProgrammingError, pymysql.DataError, pymysql.OperationalError, pymysql.IntegrityError) as e:
    resp = jsonify({"error": json.dumps(e)})
    resp.status_code = 500
  finally:
    cursor.close()
    if connection.open:
      connection.close()
  return resp
  

def list_orders():
  global connection
  if not connection.open:
    connect()
  try:
    with connection.cursor() as cursor:
      sql = 'SELECT * FROM orders'
      cursor.execute(sql)
      result = cursor.fetchall()
      resp = jsonify({"orders": result})
      resp.status_code = 200
  finally:
    if connection.open:
      connection.close()
  return resp
  

def get_order(orderid=None):
  if not connection.open:
    connect()
  try:
    cursor = connection.cursor()
    sql = 'SELECT * FROM orders WHERE id = "%s"'
    cursor.execute(sql, (int(orderid),))
    result = cursor.fetchone()
    if result:
      resp = jsonify(result)
      resp.status_code = 200
    else:
      resp = jsonify({"msg": "Error: cloud not find item: %s" % str(orderid)})
      resp.status_code = 403
  finally:
    if connection.open:
      connection.close()
    
  return resp

if not table_exist():
  create_table()


#print table_exist()
#print create_table()
#print list_orders()
#print get_order(4)
