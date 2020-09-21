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
    'RFC_Title': ['RFC123', ],
    'Host_Name': [selfIP, ],
    'TTL': [7200, ],
}

def register(opt):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)          # Create a socket object
    host = "192.168.0.144"  # Get local machine name
    port = 65423                  # Reserve a port for your service.
    s.connect((host, port))
    clienthostname=s.getpeername()
    print(clienthostname)
    listening_port = 65425
    s.send(bytes("65425", 'utf-8'))
    host1 =''

    print("My IP is --", selfIP)
    if opt != "3":
        reg_msg = input("Enter 2 to exit\n Enter 3 for query\n")
        if reg_msg== "3":
            # query=input("enter query")
            data1, Peer_IP, Peer_lstn_port = PQuery(s, "get PEER list")
            print("peerip is")
            print(Peer_IP)

            peer_msg = input("enter 1 for query \n")

            if peer_msg == "1":
                print("requesting rfc")
                query = input("enter query")
                print("query here")
                cnt = 0
                print(Peer_IP)
                peerIp_list = []
                if type(Peer_IP) is not list:
                    peerIp_list = [Peer_IP]
                else:
                    peerIp_list = Peer_IP
                for i in peerIp_list:
                    print(i)
                    print(Peer_lstn_port[0])
                    p1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    p1.connect((peerIp_list[cnt], int(Peer_lstn_port[cnt])))
                    p1.send(query.encode())
                    msgrecv = p1.recv(1024)
                    if msgrecv.decode() == "Yes":
                        print("recieved yes")
                        p1.sendall(("get_%s" % query).encode())
                        with open('%s' % query, 'wb') as f:
                            while True:
                                data = p1.recv(1024)
                                if not data:
                                    print("breaking")
                                    break
                                print("got this")
                                print(data.decode())
                                f.write(data)
                            f.close()
                            print('connection closed')
                            break
                    elif msgrecv.decode() == "No":
                        print("not found")
                    cnt = cnt + 1
                # requestrfc()
            else:
                print("choose correct option")
        while(reg_msg!="2"):
            reg_msg = input("Enter 2 to exit\n")
        exit()
    return s






RFC_Numbers = [8800, 8801, 8802]
RFC_Tittle = ['RFC_1', 'RC_2','RFC_3']





# def Peer_List_Download(data1):
#     while True:
#         data1=s.recv(1024)
#         data = data1
#         if data:
#             print(data.decode())
#             print('i am sending')
#
#         return data
#     s.close()





#RFC_Client Function

def PQuery(s,query):
    Peer_IP=""
    Peer_lstn_port=""
    s.sendall(query.encode())
    while True:
        data1 = s.recv(1024)
        data = data1
        i = 0
        if data:
            print(data.decode())
            print('i am sending')
            output=json.loads(data)
            RFC_Index['Host_Name'].append(output['IP_Addr'])
            #RFC_Index['listening_port'].append(output['listening_port'])
            #ports=output['port_list']
            lsn_port = output['listening_port']
            print(lsn_port)
            print('while loop-----')
            for i in RFC_Index['Host_Name']:
                print('if loop')

                Peer_IP = output['Host_Name']
                list_peer_ip=[]
                list_peer_port=[]
                cnt=0
                for i in Peer_IP:
                    if i != selfIP:
                        list_peer_ip.append(i)
                        list_peer_port.append(output['listening_port'][cnt])
                    cnt=cnt+1
                Peer_lstn_port = output['listening_port']
                print("connecting with peer---")
                print(Peer_IP)
                print("list is")
                print(list_peer_ip)
                cnt=0
                    # for i in Peer_IP:
                    #     print(Peer_IP[0])
                    #     print(Peer_lstn_port[0])
                    #     threading.Thread(peer_connection(Peer_IP[cnt], Peer_lstn_port[cnt]))
                    #     cnt = +1

                   # p_thread = threading.Thread(target=peer_connection, args=(Peer_IP, Peer_lstn_port))
        else:
            s.close()
        print(RFC_Index['Host_Name'])
        print(RFC_Index)
        print("peer ip is")
        print(Peer_IP)
        return data1,list_peer_ip,list_peer_port





        # for ip,port in zip(ips,ports):
        #    print("%s:%s" %(ip,port))
#def send_rfc_doc(self, conn, addr):
#    try:
#        while True:


#RFC_Index['RFC_Number'].append(1000)
#print(RFC_Index['RFC_Number'])


#data = pickle.dumps(peer_infomation())
#print (data)
#s.send(data)
#data = s.recv(1024)
#print(data.decode('utf-8'))


reg_msg= input('Enter 1 for registering \n enter 2 for leaving if already entered \n enter 3 for query to get peer list from RS server \n')
#leave_msg  = input('Do you want to Leave : ')
#query_msg = input(' Query Type: ')
#keepalive_msg = 7200
if reg_msg == "2":
    print("already exited")
    exit()
s = register(reg_msg)
if reg_msg == "1":
    print("registered")
    #s = register()



elif reg_msg == "3":
    #query=input("enter query")
    data1,Peer_IP,Peer_lstn_port = PQuery(s, "get PEER list")
    print("peerip is")
    print(Peer_IP)


    peer_msg=input("enter 1 for query \n")


    if peer_msg == "1":
        print("requesting rfc")
        query = input("enter query")
        print("query here")
        cnt=0
        print(Peer_IP)
        peerIp_list=[]
        if type(Peer_IP) is not list:
            peerIp_list=[Peer_IP]
        else:
            peerIp_list=Peer_IP
        for i in peerIp_list:
            print(i)
            print(Peer_lstn_port[0])
            p1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            p1.connect((peerIp_list[cnt], int(Peer_lstn_port[cnt])))
            p1.send(query.encode())
            msgrecv=p1.recv(1024)
            if msgrecv.decode() == "Yes":
                print("recieved yes")
                p1.sendall(("get_%s" %query).encode())
                with open('%s' %query,'wb') as f:
                    while True:
                        data=p1.recv(1024)
                        if not data:
                            print("breaking")
                            break
                        print("got this")
                        print(data.decode())
                        f.write(data)
                    f.close()
                    print('connection closed')
                    break
            elif msgrecv.decode()=="No":
                print("not found")
            cnt = cnt+ 1
        #requestrfc()
    else:
        print("choose correct option")
#if peer_msg == "2":
#    print("get rfc")
    ##getrfc()
else:
    print("choose correct option")