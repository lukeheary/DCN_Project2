#!/usr/bin/env python

# Name: Luke Heary
# Date: 2/22/19

import select
import time
import socket
import optparse

def main():

    # sets up that tag for command line inputs
    parser = optparse.OptionParser()
    parser.add_option('-p', action="append", dest="port")
    options, args = parser.parse_args()

    ports = options.port
    sockets = []

    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((str(socket.INADDR_ANY), int(port)))
        sockets.append(sock)
        sock.listen(5)

    # obtains all of the records from the first IP address
    data = ""
    conn, addr = sockets[0].accept()
    while True:
        readable, _, _ = select.select([sockets[0]], [], [])
        for x in readable:
            time.sleep(1)
            data = conn.recv(1024)
            break
        break

    data = data.strip("\"")
    records = data.split("][")
    inputs = []
    for x in sockets:
        inputs.append(x)

    while True:
        readable,_,_ = select.select(inputs, [], [])
        sampleSets = []

        for s in inputs:
            if s in readable:
                conn, addr = s.accept()
                sampleData = conn.recv(1024)
            else:
                sampleData = conn.recv(1024)
            sampleSets.append(sampleData)
        break

    printAll(records, sampleSets)

# Prints all of the data using all of the calculate functions below
def printAll(records, sampleSets):

    dataDict = {}
    for x in sampleSets:
        if x[0]:
            x = x.split("][")
            for y in x:
                if y:
                    y = y.split(":")
                    cur = y[1]
                    if cur in dataDict:
                        dataDict[cur].append(y)
                    else:
                        dataDict[cur] = [y]

    counter = 0
    dictCounter = 1
    for x in dataDict:
        d = dataDict.get(str(dictCounter))
        record = records[counter]
        record = record.split(":")

        print(record[0] + "\n" + record[1] + "\n" + record[2] + "\n" + record[3] + "\n")
        dates = calculateDates(d)
        print("From " + dates[0] + " to " + dates[1])
        calculateAveragePulse(d)
        print("Average Pulse: " + "%.1f" % float(calculateAveragePulse(d)))
        print("Average Blood Oxygen: " + "%.1f" % float(calculateAverageBlood(d)))
        print("Total Steps: " + calculateTotalSteps(d))
        print("")
        counter += 1
        dictCounter += 1

def calculateDates(samples):
    dates = []
    returnDates = []
    for sample in samples:
        dates.append(sample[2])

    returnDates.append(min(dates))
    returnDates.append(max(dates))
    return returnDates

def calculateAveragePulse(samples):
    allPulses = []
    for sample in samples:
        pulses = sample[3]
        allPulses.extend(pulses.split(" "))

    allPulses = [int(i) for i in allPulses]
    sum = 0
    for x in allPulses:
        sum += x

    return str(sum / len(allPulses))

def calculateAverageBlood(samples):
    allBlood = []
    for sample in samples:
        blood = sample[4]
        allBlood.extend(blood.split(" "))

        allBlood = [int(i) for i in allBlood]

    sum = 0
    for x in allBlood:
        sum += x

    return str(sum / len(allBlood))


def calculateTotalSteps(samples):
    allSteps = []
    for sample in samples:
        steps = sample[5]
        allSteps.extend(steps.split(" "))

        allSteps = [int(i) for i in allSteps]

    sum = 0
    for x in allSteps:
        sum += x

    return str(sum)

main()
