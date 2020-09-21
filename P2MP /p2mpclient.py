import socket
import time
import os
import threading
import math
from threading import Timer
import sys
import pickle
import platform
import json
#from receiver import calculate_checksum
import concurrent.futures

host = '127.0.0.1'
port = 7735
print(" Enter <Filename> <MSS> <PORT NUMBER>")
filename = input()
#filename= 'dummy.txt'
MSS = input()
MSS = int(MSS)
#port = input()
#port = int(port)
timeout_val = 0.5

port1 = 7740
buf = 0
data_identifier = "1010101010101010"
buff = bytes(buf)
i=1
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port1))

ip = '127.0.0.1'
seq_num = 0
ip_list = ['127.0.0.1']
port_list = [7735, 7736, 7737, 7738, 7739]
#port_list = [7735]
acks = []
threads = []
start = time.perf_counter()

def checksum_cal(data):
    return '%4X' % (-(sum(ord(c) for c in data) % 65536) & 0xFFFF)


def rdt_send(data, addr, port, seq_num):
    print("sending data via thread")
    print("addr", addr)
    print("port", port)
    while data:
        s.sendto(data, (addr, port))

        print("data sent and time threading started")
        # t = threading.Thread(target=timer_expiry, args=[0])
        # t.start()
        # t.join()
        # print(t)
        ack, address = s.recvfrom(2048)
        ack = ack.decode()
        print("ack rcvd ", ack, "\n")
        while ack == 'yes':
            time.sleep(0.05)
            print("timeout, sequence number = ", seq_num)
            print("resend port is ", address[1])
            port = address[1]
            print("ack is yes for resend")
            s.sendto(data, (addr, port))
            print("sent")
            ack, address = s.recvfrom(2048)
            ack = ack.decode()
        rcvd_seq = ack[0:32]
        print("seq_num", rcvd_seq)
        seq_num = int(seq_num)
        rcvd_seq = int(rcvd_seq)
        print(seq_num)
        print(rcvd_seq)
        print("seq 32 bits are =", rcvd_seq)
        while not ack:
        #if ack == '' or seq_num != rcvd_seq:
            #print("timer expiry set")
            print("timeout, sequence number = ", seq_num)
            print("Retransmitting as pkt not rcvd")
            s.sendto(data, (addr, port))
        #else:
        print("returning next", next)
        return next


def timer_expiry(seconds):
    #timer = Timer()
    #timer.is_alive()

    print("in timer expiry function")
    time.sleep(seconds)
    return False


def packet_buider(filename):
    size = os.path.getsize(filename)
    #s.sendto(str(size).encode(), (host, port))
    length = len(filename)
    print("length", length)
    seq = math.ceil(size / MSS)
    o = size/MSS
    print(" o output ", o)
    print("ciel output ", seq)
    time.sleep(2)
    f = open(filename[0:MSS], "r")
    file_data = f.read()
    seq_num = 0
    count = 1
    time_flstrt = time.time()
    global buf
    with open(filename) as f:
        while count <= seq:
            print("######### LETS START1111111")
            print("Segment Sequence Number ", count)
            get_chunk = file_data[buf:buf + MSS]
            checksum = checksum_cal(get_chunk)
            seq_num = '{0:032b}'.format(seq_num)
            print("seq_num ", seq_num)
            senddata = (seq_num + checksum + data_identifier + get_chunk).encode('utf-8')
            print('send data is = ', senddata)
            #for _ in ip_list:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                print("you are in concurrent loop")
                #print("ip list ", ip_list)
                result = [executor.submit(rdt_send, senddata,ip,prt, seq_num) for prt in port_list]
                print("result is ",result)
                print('recieved next')
                if int(seq_num) == 1:
                    seq_num = 0
                else:
                    seq_num = 1
            count = count+1
            buf = buf + MSS
            time_flend = time.time()
            end = time.perf_counter()
    print("counter value ", count)

    print(start)
    print(end)
    print(time_flstrt)
    print(time_flend)
    total_time = float(time_flend-time_flstrt)
    print("total time ", total_time)
    total_time = end - start
    print(total_time)
    print("chunk sent, check now")
    s.close()
    sys.exit(s)


while filename:
    packet_buider(filename)
    s.close()
