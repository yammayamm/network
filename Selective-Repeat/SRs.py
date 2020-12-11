from socket import *
import time
import threading
from threading import Lock
import random

# class Pkt holds a packet's info
class Pkt:
    def __init__(self, seqNum, time, acked):
        self._seqNum = seqNum
        self._time = time
        self._acked = acked

    def getSeqNum(self):
        return self._seqNum

    def getTime(self):
        return self._time

    def setTime(self, time):
        self._time = time

    def getAcked(self):
        return self._acked

    def setAcked(self, acked):
        self._acked = acked

windowSize = 50
timeOut = 0.1
packet_loss_prob = 0.001

windowLock = Lock()

window = []  # packets that have been sent are stored in the window
pktSndNum = 0
ACK = -1  # ACK number sender is expecting to receive
init_time = time.time()

def listener():
    global sndSocket
    global ACK
    global init_time
    global window

    while True:
        ack, rcvAddress = sndSocket.recvfrom(2048)
        ack = int(ack.decode())
        print("\t{0:0.4f} ACK: {1:d} Sender < Receiver".format(time.time() - init_time, ack))

        for tmp in window:
            if tmp.getSeqNum() == ack:
                tmp.setAcked(True)
                break

        with windowLock:

            ACK = ack
            for tmp in window:
                if tmp.getAcked():
                    window.remove(tmp)
                break


rcvIP = "localhost"
rcvPort = 12000

sndSocket = socket(AF_INET, SOCK_DGRAM)
sndSocket.bind(("localhost", 0))

t = threading.Thread(target=listener, args=())
t.start()

while True:
    # timeout
    with windowLock:
        if len(window) > 0 and time.time() - window[0].getTime() >= timeOut:
            print("\n\t{0:0.4f} pkt: {1:d} | Timeout since\t{2:0.4f}".format(time.time() - init_time, \
                                              window[0].getSeqNum(), window[0].getTime() - init_time), end="\n\n")
            sndSocket.sendto(str(window[0].getSeqNum()).encode(), (rcvIP, rcvPort))
            window[0].setTime(time.time())
            print("\t{0:0.4f} pkt: {1:d} Sender > Receiver <retransmitted>".format(time.time() - init_time,
                                                                                           window[0].getSeqNum()))
            continue

        # if window is full
        if len(window) == windowSize:
            continue

    # initialize packet transmission starting time
    if pktSndNum == 0:
        init_time = time.time()

    pkt = Pkt(pktSndNum, time.time(), False)

    with windowLock:
        window.append(pkt)

    # loss 발생
    if random.random() < packet_loss_prob:
        continue

    sndSocket.sendto(str(pkt.getSeqNum()).encode(), (rcvIP, rcvPort))
    print("\t{0:0.4f} pkt: {1:d} Sender > Receiver".format(time.time() - init_time, pkt.getSeqNum()))
    pktSndNum = pktSndNum + 1


sndSocket.close()