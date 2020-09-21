import socket
import time
import os
from threading import Timer
import sys
import pickle
import platform
import json
#from receiver import calculate_checksum
import struct
import random


ipaddr = ''
ip = '127.0.0.1'
port = 7739
print("Enter <PORT NUMBER> <file name in txt format>  <Probability>")
#port = input()
port = int(port)
#filename = input()
filename = 'new5.txt'
#probability =input()
#probability = float(probability)
probability = 0.05

buf = 0
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((ip, port))
header_len = 8
all_zero = b'0000000000000000'


identifier = b'0101010101010101'
#size, addr = s.recvfrom(1024)
#print("filesize = ", size.decode('utf-8'))


def checksum_cal(self,data, checksum):
    new_chksum= '%4X' % (-(sum(ord(c) for c in data) % 65536) & 0xFFFF)
    #new_chksum = bytes(new_chksum)- bytes()
    print(type(new_chksum))
    print("new chcksm ",new_chksum )
    if checksum == new_chksum:
        return True
    else:
        return False


print("connection done")




#while True:
expect_seq = 0
while True:
        # sz, addre = s.recvfrom(2048)
        # print(int(sz))
        #while buf <= int(sz):
        data, addres = s.recvfrom(2048)
        f = open(filename, 'a+')
        # expect_seq = '{0:032b}'.format(expect_seq)
        print("f is ", f)
        data1 = data.decode()
        print("data is ", '\n', data1)
        print("data written, will prepare ack now")
        seq_num = int(data1[1:32])
        print("seq number = ", seq_num)
        chksm = str(data1[32:36])
        print("checksum is = ", chksm)
        rcvd_data = str(data1[52:])
        print("rcvd data=", rcvd_data.encode('utf-8'))
        print("writing data")

        verify_chksm = checksum_cal(s, rcvd_data, chksm)
        print(verify_chksm)
        data_identifier = str(data1[39:52].encode())
        print("data identifier is ", data_identifier)
            #verify_chksm = True
        if expect_seq == seq_num:
              r = random.random()
              #r = 0
              print("random is ", r)
              if float(r) >= probability:
                  print("r is greater than prob")
                  if verify_chksm == True:
                       f.write(rcvd_data)
                       print("verify checksum is true")
                       seq_num = '{0:032b}'.format(seq_num)
                       print(seq_num)
                       ack = str(seq_num) + all_zero.decode() + identifier.decode()
                       print("ack is ", str(ack))
                       act=str(ack).encode()
                       print("act is = ", act)
                       s.sendto(act, (ip, 7740))
                       print('ack sent')
                  if expect_seq == 0:
                    print("increasing seq")
                    expect_seq=1
                  else:
                    expect_seq=0
              else:
                  time.sleep(0.05)
                  resend = str('yes').encode()
                  print('resend message', resend)
                  s.sendto(resend, (ip, 7740))
                  continue
        else:
              print("Packet loss, sequence number = ",seq_num )
              print("Sender has to retransmit packet")
               #time.sleep(2)
     #data, addr = s.recvfrom(2048)
          #totalrcv = len(data)
         #f.write(str(data))
f.close()
s.close()               # while totalrcv < int(sz):
               #      data = s.recvfrom(2048)
               #      totalrcv+= len(data)
               #      f.write(data)
               #      data, address = s.recvfrom(2048)
               #      f.close()

          #f.open("new file", 'a')

          #



#     #data, address = s.recv(2048).decode('utf-8')
#     print("data is ", data)
#     #print(data.decode('utf-8'))
#     #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     #s.bind((ip, port))
#     msg = "ACK"
#     print("test")
#     s.sendto(bytes(msg, 'utf-8'), (ip, port))
#     print("test2")
#     #s.sendto(b'ACK', (ip, port))
#     #s.close()

