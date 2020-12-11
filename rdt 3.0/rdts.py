from socket import *
import time
import threading
import random

def listener():
    global sndSocket
    global sendpkt
    global rcvack
    global init_time
    global flag

    while True:
        ack, rcvAddress = sndSocket.recvfrom(2048)
        rcvack = int(ack.decode())

        print("\t{0:0.4f} ACK: {1:d} Sender < Receiver".format(time.time() - init_time, rcvack))

        if sendpkt != rcvack:
            continue
        else: flag = 0

rcvIP = "localhost"
rcvPort = 10000

sndSocket = socket(AF_INET, SOCK_DGRAM)
sndSocket.bind(("localhost", 0))

t = threading.Thread(target=listener, args=())
t.start()

timeOut = 0.1
packet_loss_prob = 0.001

sendpkt = 0
rcvack = -1
init_time = time.time()
sndSocket.sendto(str(sendpkt).encode(), (rcvIP, rcvPort))
print("\t{0:0.4f} pkt: {1:d} Sender > Receiver".format(time.time() - init_time, sendpkt))
flag = -1

while True:
    # timeout
    timer = time.time()-init_time
    if timer >= timeOut:
        flag = -1
        print("\n\t{0:0.4f} pkt: {1:d} | Timeout".format(timer, sendpkt), end="\n\n")
        init_time = time.time()
        sndSocket.sendto(str(sendpkt).encode(), (rcvIP, rcvPort))
        print("\t{0:0.4f} pkt: {1:d} Sender > Receiver <retransmitted>".format(time.time() - init_time, sendpkt))
        continue


    # loss 발생
    if random.random() < packet_loss_prob:
        continue

    # 받은 것과 보낸 게 같으면 실행
    if flag == 0:
        if sendpkt == 0:
            sendpkt = 1
        else: sendpkt = 0
        init_time = time.time()
        sndSocket.sendto(str(sendpkt).encode(), (rcvIP, rcvPort))
        print("\t{0:0.4f} pkt: {1:d} Sender > Receiver".format(time.time() - init_time, sendpkt))
        flag = -1

sndSocket.close()