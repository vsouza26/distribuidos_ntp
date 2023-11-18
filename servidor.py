import sys
import argparse
import socket
import time
import struct

class Servidor():
    def __init__(self, local_addr, local_port, addrNtp):
        self.local_addr = local_addr
        self.local_port = local_port
        self.addrNtp = addrNtp
        self.server = socket.create_server((local_addr,local_port), family=socket.AF_INET)

    def start_server(self):
        self.server.listen()
        while True:
            print("Esperando Clientes!")
            clientSocket, addr = self.server.accept()
            data = clientSocket.recv(1)
            print(data)
            if (data == bytes([120])):
                clientSocket.send(bytes([63]))
                start = time.time()
                resp = clientSocket.recv(8)
                elapsed = time.time() - start
                clientTime = struct.unpack('!d', resp)[0]
                ntp = NTP(self.addrNtp)
                timeNtp = ntp()
                deltaTime = (timeNtp + elapsed) - clientTime
                byteDeltaTime = struct.pack('!d',deltaTime)
                clientSocket.send(byteDeltaTime)
                clientSocket.close()

class NTP():
    def __init__(self, addr):
        self.addr = addr

    def __call__(self):
        REF_TIME_1970 = 2208988800  # Reference time
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = b'\x1b' + 47 * b'\0'
        client.sendto(data, (self.addr, 123))
        data, address = client.recvfrom(1024)
        if data:
            t1 = struct.unpack('!12I', data)
            #CONVERTE OS BITS RECEBIDOS EM SEGUNDO E MICROSEGUNDO ([10] É SEGUNDO E [11] É MICROSEGUNDO)
            time = (t1[10] + (float(t1[11]) / 2**32)) - REF_TIME_1970
        client.close()
        return time

if __name__ == '__main__':
    argparse = argparse.ArgumentParser()
    argparse.add_argument('--ip')
    argparse.add_argument('--porta')
    arguments = argparse.parse_args()
    if not arguments.ip or not arguments.porta:
        print('Erro!', file=sys.stderr)
        exit(1)
    server = Servidor(arguments.ip, int(arguments.porta),'0.de.pool.ntp.org')
    server.start_server()


