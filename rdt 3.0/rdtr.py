from socket import *
import time
import random

rcvIP = "localhost"
rcvPort = 10000

packet_loss_prob = 0.001

rcvSocket = socket(AF_INET, SOCK_DGRAM)
rcvSocket.bind((rcvIP, rcvPort))

print("The server is ready to receive", end="\n\n")

while True:
    message, clientAddress = rcvSocket.recvfrom(2048)
    rcvpkt = message.decode()

    print("\tpkt: {0:s} Receiver < Sender".format(rcvpkt))

    if random.random() < packet_loss_prob:
        print("\tptk: {0:s} | Dropped".format(rcvpkt))
        continue

    print("\tACK: {0:s} Receiver > Sender".format(rcvpkt))
    rcvSocket.sendto(str(rcvpkt).encode(), clientAddress)
