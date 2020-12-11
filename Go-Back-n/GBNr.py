from socket import *
import time
import random

rcvIP = "localhost"
rcvPort = 10000

packet_loss_prob = 0.001

rcvSocket = socket(AF_INET, SOCK_DGRAM)
rcvSocket.bind((rcvIP, rcvPort))

print("The server is ready to receive", end="\n\n")

expectedSeq = -1    # keeps the seq number value the receiver is expecting to receive
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

    # packet was received in order
    if int(message) == expectedSeq + 1:
        expectedSeq = expectedSeq + 1

    time.sleep(0.01)
    print("\t{0:0.4f} ACK: {1:d} Receiver > Sender".format(time.time() - baseTime, expectedSeq))
    rcvSocket.sendto(str(expectedSeq).encode(), clientAddress)