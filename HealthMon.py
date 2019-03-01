# Name: Luke Heary
# Date: 2/22/19

import socket
import optparse
from threading import Thread
import json

def main():

    parser = optparse.OptionParser()
    options, args = parser.parse_args()

    ips = []
    sockets = []
    firstSock = []
    switch = True

    infoPath = args[1]
    for x in args[2:]:
        ips.append(x)
        stuff = x.split(":")
        address = stuff[0]
        port = stuff[1]

        if switch:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((address, int(port)))
            firstSock.append(sock)
            switch = False

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockets.append(sock)
        sock.connect((address, int(port)))

    readData(infoPath, firstSock)
    readSamples(sockets)
    # get Sample records from Stdin and pass them to each of the correct sockets

def readData(infoPath, sockets):
    file = open(infoPath, "r")

    records = []
    counter = 0
    record = []
    for line in file:
        line = line.strip("\n")
        if(line != ''):
            if counter < 3:
                record.append(line)
                counter += 1
            else:
                record.append(line)
                data = json.dumps(record)
                recordStr = ':'.join(str(e) for e in record) + "]["
                sockets[0].send(recordStr)
                record = []
                counter = 0

    return records

def readSamples(sockets):
    file = open("samples.dat", "r")
    for line in file:
        line = line.strip("\n")
        lineArray = line.split(", ")
        destIndex = int(lineArray[0]) - 1 # gets the first index and subtracts the value by 1 for interacting
        destSocket = sockets[destIndex]
        data = json.dumps(line)
        destSocket.send(data.encode())


main()