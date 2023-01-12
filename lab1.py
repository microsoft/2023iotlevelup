import os, socket, sys, json
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
conn_str = os.getenv("conn_str")
osname = ""

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

# reference: https://github.com/Azure/azure-iot-sdk-python/blob/main/samples/sync-samples/receive_direct_method.py
def method_request_handler(method_request):
    # Determine how to respond to the method request based on the method name
    if method_request.name == "method1":
        payload = {"result": True, "data": "some data"}  # set response payload
        status = 200  # set return status code
        print("executed method1")
    else:
        payload = {"result": False, "data": "unknown method"}  # set response payload
        status = 400  # set return status code
        print("executed unknown method: " + method_request.name)

    # Send the response
    method_response = MethodResponse.create_from_method_request(method_request, status, payload)
    device_client.send_method_response(method_response)

# reference: https://github.com/Azure/azure-iot-sdk-python/blob/main/samples/sync-samples/receive_message.py
def message_handler(message):
    print("the data in the message received was ")
    print(message.data)
    print("custom properties are")
    print(message.custom_properties)

# reference: https://github.com/Azure/azure-iot-sdk-python/blob/main/samples/sync-samples/receive_twin_desired_properties_patch.py
def twin_patch_handler(patch):
    print("the data in the desired properties patch was: {}".format(patch))

device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)
device_client.connect()
device_client.on_message_received = message_handler
device_client.on_method_request_received = method_request_handler
device_client.on_twin_desired_properties_patch_received = twin_patch_handler

# get the initial twin, reference: https://github.com/Azure/azure-iot-sdk-python/blob/main/samples/sync-samples/get_twin.py
twin = device_client.get_twin()
print("Initial twin document received:")
print("    {}".format(twin))
print()

# setting a reported twin, reference: https://github.com/Azure/azure-iot-sdk-python/blob/main/samples/sync-samples/update_twin_reported_properties.py
reported_properties = {"OS": osname, "CurrentUser": str(os.environ["LOGNAME"]), "IP": str(socket.gethostbyname(socket.gethostname()))}

print("Sending reported twin properties:")
print("    {}".format(reported_properties))
print()
device_client.patch_twin_reported_properties(reported_properties)

#finally sending a message with properties and encoding
iotmessage = Message(json.dumps({"Message": "Hello World"}))
iotmessage.custom_properties["alert"] = False
iotmessage.content_encoding = "utf-8"
iotmessage.content_type = "application/json"
device_client.send_message(iotmessage)

input("Message " + str(iotmessage) + " and twin sent, waiting to reveive messages/command/twins, Press any key to quit\n")
