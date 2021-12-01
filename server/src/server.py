# Pyramid Imports
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response
from pyramid.response import Response
from datetime import datetime
import time
import json

# Import MySQL Connector Driver
import mysql.connector as mysql

# Load the DB credentials
import os
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

# Valid commands from web UI controller
valid_commands = ['takeoff','land','up','down','left','right','back','forward','cw','ccw']


""" Helper Functions """

# A Function to Queue Commands to the MySQL Database
def send_command(command):
  time = str(datetime.now())
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  sql = """INSERT INTO Commands(
    message, created_at)
    VALUES (%s, %s)"""
  val = (command, time)
  cursor.execute(sql, val)
  db.commit()
  
""" Routes """

# TEST ROUTE TEST ROUTE TEST ROUTE TEST ROUTE TEST ROUTE
def test(req):
  send_command("test")
  return Response("Command sent to db (server): 'test'")

# VIEW: Web Controller Route
def web_ui_route(req):
  return render_to_response('templates/web_ui.html', [], request=req)

# REST: Drone Command Route
def drone_command_route(req):
  command = req.matchdict.get('command')
  arg = req.matchdict.get('arg')

  if command not in valid_commands:
    return {'Response (server):':'Invalid command received'}

  # Combine argument with command
  command = command if not arg else command + " " + arg[0]

  print('Sending command: ', command)
  send_command(command)
  return {'Response (server):':'Command sent!'}

#############################################################
### Define and build your NEW route functionalities here: ###
#############################################################
def flight_plan(req):
    cmd = req.json_body
    # print(cmd)
    cmdlist = str(cmd['ida']).replace('\n', ' ').lower().split()
    c = 0
    for cmd in cmdlist:
          cmdlist[c] = cmd.replace('_', ' ')
          c += 1
    #check command if valid
    validcmd = []
    for cmd in cmdlist:
          if str(cmd.split()[0]) in valid_commands:
                validcmd.append(cmd)
    for cmd in validcmd:
          send_command(cmd)
          time.sleep(3)

def get_telemetry(req):
      db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
      cursor = db.cursor()
      cursor.execute("SELECT * FROM Telemetry ORDER BY id DESC LIMIT 1")
      data = cursor.fetchone()
      db.commit()
      ld = []
      if type(data) != type(None):
        for d in data:
              ld.append(d)
        ld.pop()
        ld.pop(0)
      keys = ["pitch", "roll", "yaw", "vgx", "vgy", "vgz", "templ",
            "temph", "tof", "h", "bat", "baro", "time", "agx", "agy", "agz"]
      # print(ld)
      jsondata = dict(zip(keys, ld))
      # jsondata = {"pitch":ld[1],"roll":ld[2],"yaw":ld[3],"vgx":ld[4],"vgy":ld[5],"vgz":ld[6],"templ":ld[7],"temph":ld[8],"tof":ld[9],"h":ld[10],"bat":ld[11],"baro":ld[12],"time":ld[13],"agx":ld[14],"agy":ld[15],"agz":ld[16]}
      response = Response(body=json.dumps(jsondata))
      response.headers.update({'Access-Control-Allow-Origin': '*',})
      return response
      
""" Main Entrypoint """

if __name__ == '__main__':
  with Configurator() as config:
    config.include('pyramid_jinja2')
    config.add_jinja2_renderer('.html')

    # TEST ROUTE TEST ROUTE TEST ROUTE TEST ROUTE TEST ROUTE
    config.add_route('test', '/test')
    config.add_view(test, route_name='test')

    config.add_route('web_ui', '/')
    config.add_view(web_ui_route, route_name='web_ui')

    config.add_route('drone_command', '/drone_command/{command}*arg')
    config.add_view(drone_command_route, route_name='drone_command', renderer='json')

    config.add_route('flight_plan', '/flight_plan')
    config.add_view(flight_plan, route_name='flight_plan', renderer='json')
    
    config.add_route('get_telemetry', '/get_telemetry')
    config.add_view(get_telemetry, route_name='get_telemetry', renderer='json')

    config.add_static_view(name='/', path='./public', cache_max_age=3600)

    app = config.make_wsgi_app()

  server = make_server('0.0.0.0', 1234, app)
  print('Web server started on: http://0.0.0.0:8000 OR http://localhost:8000')
  server.serve_forever()
