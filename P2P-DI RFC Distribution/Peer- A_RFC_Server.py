import socket               # Import socket module
import time                # Import time module
import platform             # Import platform module to get our OS
import os
import pickle
import sys
import threading
from _thread import *
import json

self_name = socket.gethostname()
selfIP = socket.gethostbyname(self_name)

RFC_Index = {
    'RFC_Number': [7157, ],
    'RFC_Title': ['rfc123', ],
    'Host_Name': [self_name, ],
    'TTL': [7200, ],
}
addr=selfIP
listening_port = 65425

def send_rfc_doc(self, conn, addr):
    remotefilepath = "C:\\User\\ayush\\Desktop\\rfc"
    while True:
        try:
            s.connect(RFC_Index['Host_Name'], lsn_port)
            print("Client connected to download a file...")
            try:
                filename = conn.recv(1024)
                if os.path.exists(remotefilepath + '/' + filename):
                    filesize = os.path.getsize(remotefilepath + '/' + filename)
                    if filesize > 0:
                        conn.send(str(filesize))
                        with open(remotefilepath + '/' + filename, 'rb') as f:
                            bytes = f.read(1024)
                            conn.send(bytes)
                            while bytes != "":
                                bytes = f.read(1024)
                                conn.send(bytes)
                    else:
                        conn.send("Empty")
                else:
                    conn.send("False")
            finally:
                conn.close()
        finally:
            return False



print("conecting with peer in thread")
p1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
p1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
p1.bind((addr, int(listening_port)))
p1.listen(10)
while True:
    c, addr = p1.accept()  # Establish connection with client.
    print("connection success")
    msg = c.recv(1024)
    print("recieved this ::::::")
    print(msg)
    if "rfc" in msg.decode():
        print(msg.decode())
        print("expected is %s" %RFC_Index['RFC_Title'])
        if  msg.decode() in RFC_Index['RFC_Title']:
            #msg1 = json.dumps()
            print("sending yes")
            c.sendall(b'Yes')
        else:
            print("sending no")
            c.sendall(b'No')
    msg = c.recv(1024)
    print("recieved this ::::::")
    print(msg)
    if "get_" in msg.decode():
        file = msg.decode().lstrip("get_")
        file = file + ".txt"
        f = open(file, 'rb')
        l = f.readline()
        while b'\n' in l:
            c.sendall(l)
            print('sent', repr(l))
            l = f.readline()
        f.close()
        c.close()


