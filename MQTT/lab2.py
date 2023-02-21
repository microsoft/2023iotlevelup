import os, socket, sys, json
from base64 import b64encode, b64decode
from hashlib import sha256
from time import time
from urllib.parse import quote_plus, urlencode
from hmac import HMAC
import paho.mqtt.client as mqtt
conn_str = os.getenv("conn_str")
osname = ""
rid = 0

if sys.platform == "linux":
    osname = str(os.uname().release + " " + os.uname().version + " " + os.uname().machine)
else:
    osname = str("Windows build " + str(sys.getwindowsversion().build) + " " + os.environ["PROCESSOR_IDENTIFIER"])

if conn_str == None:
    print("Please set the enviornment variable conn_str to the value of a device connection string")
    print("    example: export conn_str=\"HostName=ksaye.azure-devices.net;DeviceId=python;SharedAccessKey=4sDfmCBS1MnfVsQxUv/rEksRlzOctcOU=\"")
    print("exiting now")
    quit()
conn_str = conn_str.replace("\"","")
print("Connection String: " + conn_str)
print()

def generate_sas_token(uri, key, expiry=3600):
    ttl = time() + expiry
    sign_key = "%s\n%d" % ((quote_plus(uri)), int(ttl))
    sign_key = sign_key.encode('utf-8')
    signature = b64encode(HMAC(b64decode(key), sign_key, sha256).digest())
    return 'SharedAccessSignature ' + urlencode({'sr' : uri,'sig': signature, 'se' : str(int(ttl))})

def message_handler(client, userdata, msg):
    global rid
    msgpayload = msg.payload.decode("utf-8")
    if "$iothub/methods/POST/" in msg.topic:
        # responding to a direct method
        print("Received Direct Method: " + str(msg.topic).split("/")[3] + " with payload: " + str(msgpayload))
        print()
        rid = int(msg.topic.split("=")[1])
        # acknowledging the direct method
        payload = {"result": True, "data": "some data"} 
        status = 200
        client.publish("$iothub/methods/res/" + str(status) + "/?$rid=" + str(rid), str(payload))
    elif "$iothub/twin/res/" in msg.topic:
        # received a twin
        print("Received twin status " + str(msg.topic).split("/")[3] +  " with payload: "+str(msgpayload))
        print()
        int(msg.topic.split("=")[1].split("&")[0])
    elif "devices/" + deviceID + "/messages/devicebound/" in msg.topic:
        # we have a cloud to device message
        print("Received C2D with payload: "+str(msgpayload))        

def on_connect(client, userdata, flags, rc):
    client.subscribe("devices/" + deviceID + "/messages/devicebound/#")     # C2D
    client.subscribe("$iothub/methods/POST/#")                              # direct methods
    client.subscribe("$iothub/twin/res/#")                                  # twins
    client.publish("$iothub/twin/GET/?$rid=" + str(rid), "")                # must send a message to get the initial twin

hostname = conn_str.split(";")[0].split("=")[1]
deviceID = conn_str.split(";")[1].split("=")[1]
deviceKey = conn_str.split(";")[2].replace("SharedAccessKey=", "")
password = generate_sas_token(hostname + "/devices/" + deviceID, deviceKey)

client = mqtt.Client(client_id=deviceID)
client.on_message = message_handler
client.on_connect = on_connect
client.username_pw_set(hostname + "/" + deviceID + "/api-version=2016-11-14", password)
client.tls_set_context(context=None)
client.connect(hostname, 8883)
while not client.is_connected():
    client.loop()       # waiting for connection

# updating a twin property
reported_properties = {"OS": osname, "CurrentUser": str(os.environ["LOGNAME"]), "IP": str(socket.gethostbyname(socket.gethostname()))}
client.publish("$iothub/twin/PATCH/properties/reported/?$rid=" + str(rid), json.dumps(reported_properties))
print("sent twin: " + str(reported_properties))

# send a message with properties and encoding
iotmessage = json.dumps({"Message": "Hello World"})
client.publish("devices/" + deviceID + "/messages/events/alert=False$.ct=application%2Fjson&$.ce=utf-8", iotmessage)

print("Message " + str(iotmessage) + " and twin sent, waiting to reveive messages/command/twins, Control+C to exit")
client.loop_forever()
