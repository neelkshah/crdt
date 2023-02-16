from flask import Flask, request
from model.GCounter import GCounter
import json
import threading
import time
import os
import datetime
import sys
import random

app = Flask(__name__)

gcounter = GCounter("")


def heartbeat():
    while True:
        randomnum = random.randint(1, 20)
        if randomnum == 1:
            return
        f = open("C:\\Users\\neelshah\\Desktop\\crdt.log", "a")
        f.write(str(os.getpid()) + " : " +
                str(datetime.datetime.now()) + " : Refreshing all hosts.\n")
        f.close()
        gcounter.populateAllHosts()
        gcounter.ping()
        time.sleep(30)


@app.route('/')
def hello_world():
    gcounter.register(request.host)
    gcounter.populateAllHosts()
    return gcounter.view()


@app.route('/me')
def gc():
    return gcounter.view()


@app.route('/me/value')
def value():
    return gcounter.value()


@app.route('/me/increment')
def incrementgcounter():
    gcounter.increment()
    gcounter.ping()
    return str(gcounter.view())


@app.route('/merge', methods=['POST'])
def merge():
    othercounter = json.loads(str(request.json))
    gcounter.merge(othercounter)
    return str(gcounter.view())


@app.route('/ping', methods=['POST'])
def ping():
    othercounter = str(json.loads(str(request.json)))
    gcounter.merge(othercounter)
    return str(gcounter.view())


if __name__ == '__main__':
    print("Starting heartbeats.")
    heartbeatthread = threading.Thread(target=heartbeat, name="crdthb")
    heartbeatthread.start()
    app.run(debug=False, port=int(sys.argv[1]))
