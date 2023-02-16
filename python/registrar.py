from flask import Flask, request, Response
from model.Registration import Registration
import json

app = Flask(__name__)

hostregister = dict()

@app.route('/register', methods=['POST'])
def register():
    othercounter = Registration(**json.loads(str(request.json)))
    hostregister[othercounter.id] = othercounter.host
    return Response("{'"+othercounter.id+"':'"+othercounter.host+"'}", status=201, mimetype='application/json')

@app.route('/list', methods=['GET'])
def list():
    hostsStr = ",".join(hostregister.values())
    return hostsStr