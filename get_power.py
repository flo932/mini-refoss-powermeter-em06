#!/usr/bin/python3
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
#t = b"1"
    md5_hash = md5(t)

    SYSTEM_ALL = "Appliance.System.All"
    SYSTEM_ABILITY = "Appliance.System.Ability"

    CONTROL_TOGGLEX = "Appliance.Control.ToggleX"
    CONTROL_ELECTRICITYX = "Appliance.Control.ElectricityX"


    messageId = md5_hash.hexdigest().lower()
    timestamp = int(round(time.time()))
    method = "GET" # GET , SET=TOGGLE

    namespace_val = SYSTEM_ALL 
    #namespace_val = SYSTEM_ABILITY 
    if mode == "power":
        namespace_val = CONTROL_ELECTRICITYX

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

    #ip = "192.168.20.171"
    #ip = "192.168.20.129"
    #path = f"http://{ip}/config"
    path = f"http://{ip}/public"

    url = path
    #print()
    #print(ip,url)
    x=requests.post(url, json=data)

    #print(x.text)

    return json.loads(x.text)
    exit()
    def print_x(a,level=1):
        if type(a) is dict:
            for k,v in a.items():
                print(" "*level,level,k)
                print_x(v,level=level+1)
        else:
            print(" "," "*level,a)


    d = json.loads(x.text)
    for k,v in enumerate(d):
        print()
        print(k,v)
        print_x(d,level=1)

def print_power(out):
    for k,v in enumerate(out):
        print(k,v)

from datetime import datetime
import config

def log_power(out):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fname = config.log_path +datetime.now().strftime('%Y-%m-%d')+".log"
    print("log_path:",fname)
    f = open(fname,"a")
    for k,v in enumerate(out):
        f.write(json.dumps(v)+"\n")
    f.close()

def log_power_space():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fname = config.log_path+datetime.now().strftime('%Y-%m-%d')+".log"
    print("log_path:",fname)
    f = open(fname,"a")
    f.write("\n")
    f.close()

def parse_power(r,name=""):
    out = [] #{"name":""}
    data=r["payload"]["electricity"]
    map1 = {'name': 'OG','channel':"CH",'current':"A",'voltage':"V",'power':"W",'mConsume':"kWh",'factor':"fa"}
    map2 = {'current':1000,'voltage':1000,'power':1000,'mConsume':1000,'factor':1}
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for k,v in enumerate(data): #.items():
        #if name:
        #    data[k]["name"] = name
        d = {"stamp":now,"name":name}
        #d.update(data[k])
        for kk,vv in data[k].items():
            div = 1
            if kk in map2:
                div = map2[kk]
                try:
                    if div > 1:
                        vv /= div
                    vv = round(vv,2)
                except: pass

            if kk in map1:
                kk = map1[kk]

            d[kk] = vv
 
        out.append(d)
        #print(".",k,v)

    return out #r["payload"]["electricity"]

def get_power(ip,dd_id,name):
    try:
        r=request(ip,dd_id,mode="power")
        out=parse_power(r,name=name)
        print_power(out)
        log_power(out)
    except Exception as e:
        print("er",ip,e)

if __name__ == "__main__":
    log_power_space()
    # -------------

    import config 
    for v in config.nodes:
        print()
        print("node",v)
        get_power(v["ip"],v["uuid"],name=v["name"])
        time.sleep(0.3)
    
    

