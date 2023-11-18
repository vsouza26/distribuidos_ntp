import socket
import struct
import time


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9999))
client.send(bytes([120]))
data = client.recv(1)
times = time.time()
data = struct.pack('!d', times)
client.send(data)
byteTimeDelta = client.recv(8)
floatTimeDelta = struct.unpack('!d', byteTimeDelta)[0]
print(floatTimeDelta)
client.close()

