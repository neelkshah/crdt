import json
import requests
import uuid
from model.Registration import Registration
import random


class GCounter:

    def __init__(self, host):
        self.id = str(uuid.uuid4())
        node = Node(0, host)
        self.counter = dict()
        self.counter[self.id] = node
        self.allHosts = ""

    def increment(self):
        self.counter[self.id].count = self.counter[self.id].count + 1

    def merge(self, packet):
        randomnum = random.randint(1, 20)
        if randomnum == 1:
            return
        for key in packet:
            value = packet[key]
            otherCount = int(value.split(",")[0])
            otherHost = value.split(",")[1]
            if key in self.counter:
                self.counter[key].count = max(
                    self.counter[key].count, otherCount)
            else:
                self.counter[key] = Node(otherCount, otherHost)

    def value(self):
        result = 0
        for key in self.counter:
            result += self.counter[key].count
        return str(result)

    def view(self):
        resultStr = ""
        for key in self.counter:
            resultStr += key + ": " + str(self.counter[key].count) + "\n"
        return resultStr

    def ping(self):
        packet = dict()
        for key in self.counter:
            packet[key] = str(self.counter[key].count) + \
                "," + self.counter[key].host
        for host in self.allHosts.split(","):
            if host != self.counter[self.id].host:
                requests.post("http://" + host + "/merge",
                              json=json.dumps(packet))

    def register(self, host):
        self.counter[self.id].host = host
        jsonbody = json.dumps(Registration(self.id, host).__dict__)
        requests.post('http://localhost:5000/register', json=jsonbody)

    def populateAllHosts(self):
        self.allHosts = requests.get('http://localhost:5000/list').text


class Node:
    def __init__(self, count, host):
        self.count = count
        self.host = host

    def __dict__(self):
        return {
            'count': str(self.count),
            'host': str(self.host)
        }
