import socket               # Import socket module
import string
import time                # Import time module
import platform             # Import platform module to get our OS
import os
from _thread import *
import pickle
import datetime
import urllib
import json


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((socket.gethostname(), 65423))
buf_size=25
s.listen(5)                  # Now wait for client connection.
Flag = False
count = 0
ck = 1000

x =1
i = 0



peer_list_dict={
    'IP_Addr':[],
    'port_list':[],
    'Host_Name':[],
    'listening_port' : [],
    'peers_cookie':[],
    'peer_flag':[],
    'peer_ttl':[],
    'last_status':[],
    'register_count':[],
}


def peer_cookie(c):
    i = 0
    if (c):
        i = i+100
    return i


def client_thread(conn, hstnm, addr,listening_port, Flag, pck, ttl, ls, rc):
    print(peer_list_dict['Host_Name'])
    for i in range(len(peer_list_dict['Host_Name'])):
        print(peer_list_dict['Host_Name'][i])
        print(peer_list_dict['IP_Addr'][i])

    ttl = ttl_thread(ttl)
    print(ttl)
    if ttl == 0:
        Flag = False

    cur_time = datetime.datetime.now()
    print(peer_list_dict)

    msg = json.dumps(peer_list_dict)
    print("sending this msg test")
    print(msg)
    conn.sendall(msg.encode())
    conn.close()

def cookie_finder(hstnm):
    pck=0
    for i in peer_list_dict['Host_Name']:
        if addr[0] == peer_list_dict['IP_Addr']:
            pck = peer_list_dict['peers_cookie'][i]
        else:
            pck=pck+1
            break
    return pck

def reg_count(hstnm, rc):
    rc=0
    for i in peer_list_dict['Host_Name']:
        if addr[0] == peer_list_dict['IP_Addr']:
            rc= peer_list_dict['register_count'][i]
            rc = rc+1
        else:
            rc = rc+1

    return rc

def ttl_thread(ttl=10):
    ttl = time.sleep(1)
    return ttl


pck = 100
ls = time.time()
rc = 0
while True:
    c, addr = s.accept()  # Establish connection with client.
    hstnm = c.getpeername()[0]
    print(addr[0])
    print(addr[1])
    cur_time = datetime.datetime.now()
    msg = c.recv(1024)
    listening_port = (msg.decode('utf-8'))

    print(listening_port)
    print(hstnm)
    Flag = True
    i=0
    ttl = 10
    if peer_list_dict['IP_Addr'] == []:
        peer_list_dict['IP_Addr'].append(addr[0])
        peer_list_dict['port_list'].append(addr[1])
        peer_list_dict['Host_Name'].append(hstnm)
        peer_list_dict['listening_port'].append(listening_port)
        peer_list_dict['peers_cookie'].append(pck)
        peer_list_dict['peer_flag'].append(Flag)
        peer_list_dict['peer_ttl'].append(ttl)
        peer_list_dict['last_status'].append(ls)
        peer_list_dict['register_count'].append(rc)
        rc = rc+1
        print('added 1st peer')
        client_thread(c, hstnm, addr[0],listening_port, Flag, pck, ttl, ls, rc)

    elif addr[0] not in peer_list_dict['IP_Addr']:
            peer_list_dict['IP_Addr'].append(addr[0])
            peer_list_dict['port_list'].append(addr[1])
            peer_list_dict['Host_Name'].append(hstnm)
            peer_list_dict['listening_port'].append(listening_port)
            peer_list_dict['peers_cookie'].append(pck)
            peer_list_dict['peer_flag'].append(Flag)
            peer_list_dict['peer_ttl'].append(ttl)
            peer_list_dict['last_status'].append(ls)
            peer_list_dict['register_count'].append(rc)
            print('traverse and added')
            rc = rc+1
            client_thread(c, hstnm, addr[0],listening_port, Flag, pck, ttl, ls, rc)

    else:
        print('runnig existing thread')
        pck = cookie_finder(hstnm)
        rc = reg_count(hstnm,rc)
        client_thread(c, hstnm, addr[0],listening_port, Flag, pck, ttl, ls, rc)


    c.close()
