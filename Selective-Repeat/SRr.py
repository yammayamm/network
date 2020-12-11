from socket import *
import time
import random
from threading import Lock

class Pkt:
    def __init__(self, seqNum, acked):
        self._seqNum = seqNum
        self._acked = acked

    def getSeqNum(self):
        return self._seqNum

    def getAcked(self):
        return self._acked

    def setAcked(self, acked):
        self._acked = acked

rcvIP = "localhost"
rcvPort = 12000

packet_loss_prob = 0.001
windowSize = 50

rcvSocket = socket(AF_INET, SOCK_DGRAM)
rcvSocket.bind((rcvIP, rcvPort))

print("The server is ready to receive", end="\n\n")

windowLock = Lock()
window = []
for i in range(windowSize):
    pkt = Pkt(i, False)
    window.append(pkt)
flag = 0

while True:
    message, clientAddress = rcvSocket.recvfrom(2048)
    message = message.decode()

    if flag == 0:
        flag = 1
        baseTime = time.time()

    print("\t{0:0.4f} pkt: {1:s} Receiver < Sender".format(time.time() - baseTime, message))

    if random.random() < packet_loss_prob:
        print("\t{0:0.4f} ptk: {1:s} | Dropped".format(time.time() - baseTime, message))
        continue
    else:
        for tmp in window:
            if tmp.getSeqNum() == int(message):
                tmp.setAcked(True)
                break

    # 맨 앞 ack가 True이면 remove와 append
    for tmp in window:
        if tmp.getAcked():
            window.remove(tmp)
            pkt = Pkt(window[-1].getSeqNum()+1, False)
            window.append(pkt)
        else:
            break

    time.sleep(0.01)
    print("\t{0:0.4f} ACK: {1} Receiver > Sender".format(time.time() - baseTime, message))
    rcvSocket.sendto(message.encode(), clientAddress)