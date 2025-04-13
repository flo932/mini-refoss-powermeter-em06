import asyncio
import json
import logging
import socket

# for refoss Powermeter EM06
import os
from hashlib import md5
import time
import requests
import json
import string
import random


def request(ip,dd_id,mode="info"):
    md5_hash = md5()

    t = bytes(str(time.time()),"ascii")
    md5_hash = md5(t)

    # mode's
    SYSTEM_ALL = "Appliance.System.All"
    SYSTEM_ABILITY = "Appliance.System.Ability"

    CONTROL_TOGGLEX = "Appliance.Control.ToggleX"
    CONTROL_ELECTRICITYX = "Appliance.Control.ElectricityX"


    messageId = md5_hash.hexdigest().lower()
    timestamp = int(round(time.time()))
    method = "GET" # GET , SET=TOGGLE

    namespace_val = SYSTEM_ALL 
    destination_device_uuid = dd_id

    payload = {}
    userkey = ""

    randomstring = "".join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(16)
    )

    strtohash = f"{messageId}{userkey}{timestamp}"
    md5_hash.update(strtohash.encode("utf8"))
    signature = md5_hash.hexdigest().lower()

    if 1: # sonsor data
        #namespace_val = "Appliance.Control.ElectricityX"
        payload = {"electricity": {"channel": 65535}}

    data = {
            "header": {
                "from": f"/app/{randomstring}/subscribe",
                "messageId": messageId,
                "method": method,
                "namespace": namespace_val,
                "payloadVersion": 1,
                "sign": signature,
                "timestamp": timestamp,
                "triggerSrc": "HA",
                "uuid": destination_device_uuid,
            },
            "payload": payload,
        }


    #print(data)
    a=1

    path = f"http://{ip}/public"

    url = path
    #print(ip,url)
    x=requests.post(url, json=data)
    print("="*20)
    print(x.text)
    node = None
    if 1:#try:
        jdata=json.loads(x.text)
        node = {"ip":ip,"uuid":"","name":"floor1"}
        if jdata["header"]["uuid"]:
            node["uuid"] = jdata["header"]["uuid"]
        print("node:",node)
    #except Exception as e:
    #    print("err",e)
    print("="*20)
    print()
    return node


def socket_init() -> socket.socket:
    """socket_init."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    #sock.bind(("", 9989))
    return sock

nodes = []

def server():
    PORT = 9988
    PORT = 9989
    IP = "" #"0.0.0.0"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    sock.bind((IP, PORT))
    print(f"start listening to {IP}:{PORT}")
    while True:
        print(1)
        #data, addr = sock.recv(10) #from(10)
        data, addr = sock.recvfrom(1024)
        print(f"received message: {data}")
        try:
            jdata = json.loads(data)
            ip  = addr[0]
            dd_id = jdata["uuid"]
            node = request(ip,dd_id,mode="info")
            if node:
                nodes.append(node)
        except Exception as e:
            print("err",e)


import _thread as thread

thread.start_new_thread(server,())
import time
time.sleep(2)

class X():
    def __init__(self):
        self.sock = socket_init()
    def send(self,ip="192.168.20.1"):
        address = (ip, 9988)
        msg = json.dumps(
            {"id": "48cbd88f969eb3c486085cfe7b5eb1e4", "devName": "*"}
        ).encode("utf-8")
        self.sock.sendto(msg, address)
        print("OK",ip,msg)


x = X()
import config 
x.send(ip=config.braodcast_ip) # broadcast
time.sleep(2)
print("sleep...")
time.sleep(1)
print("end")
print()

print("# append in your config.py ")
for i,node in enumerate(nodes):
    j = i+1
    node["name"] = f"floor{j}"
    print("_node =",node)
    print("nodes.append(_node)")
    print()
