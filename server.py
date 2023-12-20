#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os
def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s соединено" % client_address)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    name = client.recv(BUFSIZ).decode("utf-8")
    clients[client] = name
    while True:
        try:
            msg = client.recv(BUFSIZ)
            dsmg = msg.decode('utf-8')
            id_kuda = dsmg.split("'__'")[0]
            if "otpravit" == dsmg.split("'__'")[-1]:
                s = socket(AF_INET, SOCK_STREAM)
                host = "0.0.0.0"
                port = int(dsmg.split("'__'")[3])
                s.bind((host, port))
                s.listen(1)
                print(port)
                print("waiting...")
                conn, addr = s.accept()
                print(addr, "connected")

                filename = dsmg.split("'__'")[-2]
                file = open(filename, "wb")
                while True:
                    file_data = conn.recv(4096)
                    file.write(file_data)
                    if not file_data:
                        break
                file.close()
                conn.close()
                broadcast(id_kuda,clients[client]+"'__'"+dsmg)
            if "prinat" == dsmg.split("'__'")[-1]:
                s = socket(AF_INET, SOCK_STREAM)
                host = "0.0.0.0"
                port = int(dsmg.split("'__'")[1])
                s.bind((host, port))
                s.listen(1)
                print("waiting...")
                conn, addr = s.accept()
                print(addr, "connected")
                filename = dsmg.split("'__'")[2]
                file = open(filename, "rb")
                while True:
                    file_data = file.read(4096)
                    conn.send(file_data)
                    if not file_data:
                        break
                file.close()
                os.remove(dsmg.split("'__'")[2])
                conn.close()
        except:
            client.close()
            del clients[client]
            break



def broadcast(id_kuda,msg):
    for sock in clients:
        if clients[sock] == id_kuda:
            sock.send(bytes(msg, "utf-8"))

        
clients = {}
addresses = {}

HOST = '0.0.0.0'
PORT = 1
BUFSIZ = 4096
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()