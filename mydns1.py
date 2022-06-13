# File for Assignment 2

import binascii
import codecs
import sys
from socket import *

# Prepare message to send to root DNS Server
# Size limit of messages = 512 octets
# Type A = 1 a host address
# Type NS = 2 an authoritative name server

# HEADER
# ID = 16 (would be '0010' in hexadecimal),
# QR = 0, OPCODE = 0, AA = 0, TC = 0, RD = 0 (No Recursion b/c iterative queries are required)
# RA = 0, Z = 0, RCODE = 0, QDCOUNT = 1, ANCOUNT = 0, NSCOUNT = 0, ARCOUNT = 0

# QUESTION SECTION
# QNAME = Need to split the domain name by the periods.
# QTYPE = 1
# QTYPE = 1

"""

class ResourceRecord:
    def __init__(self, data):
        if "c0" in name:
            name = name.replace('c0', '')
        i = int(name) - (length)
        self.name = ""
        while i < len(rdata):
            hexchr = chr(int(rdata[i:i+2], 16))
            if hexchr == '-':
                break
            self.name += hexchr
            i += 2

        # self.name = name
        self.type = type
        self.rrclass = rrclass
        self.ttl = ttl
        self.rdlength = rdlength
        self.rdata = rdata

"""

def header():
    id = '0010'
    secondRow = '0000'
    qdcount = '0001'
    ancount = '0000'
    nscount = '0000'
    arcount = '0000'

    message = id + secondRow + qdcount + ancount + nscount + arcount

    message = message.replace("\n", "")

    return message


def labelDomainName(domainName):

    qname = ""
    count = 0
    position = 0
    j = 0

    for i in domainName:
        if i == '.':
            qname += str(hex(count))
            while j < count:
                qname += str(codecs.encode(binascii.a2b_qp(domainName[position + j]), "hex"))
                j += 1
            position += j + 1
            j = 0
            count = 0
        else:
            count += 1

    qname += str(hex(count))
    while j < count:
        qname += str(codecs.encode(binascii.a2b_qp(domainName[position + j]), "hex"))
        j += 1

    qname += '00'

    return qname.replace("b", "").replace("'", "").replace("0x", "0")


def questionSection(dName):
    qname = labelDomainName(dName)
    qtype = '0001'
    qclass = '0001'

    return qname + qtype + qclass


def decodeResponse(message):

    # print(message)

    if message[0:4] != '0010':
        print("Wrong response.")
        exit(1)
    if message[4:8] != '8000':
        print("There was an error in the response.")
        exit(1)

    questions = int(message[8:12], 16)
    answers = int(message[12:16], 16)
    inter = int(message[16:20], 16)
    addInfoRecords = int(message[20:24], 16)

    """

    rrposition = message.find("00010001", 25, len(message))
    
    interHexArray = []
    interArray = []
    addHexArray = []

    i = rrposition + 8

    while i < (len(message) - (24 * addInfoRecords)):
        # print(i)
        if not interHexArray:
            interHexArray.append(message[i:i+62])
            i += 62
        else:
            interHexArray.append(message[i:i+32])
            i += 32

    for x in interHexArray:

    """
    
    print("DNS server to query: " + rootDNSIP)
    print("Reply received. Content overview:\n\t" +
        str(answers) + " Answers.\n\t" +
        str(inter) + " Intermediate Name Servers.\n\t" +
        str(addInfoRecords) + " Additional Information Records.")

    print("Answers Section:")
    print("Authotitative Section:")
    print("Additional Information Section:")
    # print("\tName: " + str(rrArray[0].name) + " Data Length: " + rrArray[0].rdlength + " Name Server: " + rrArray[0].rdata)

    return int(answers)

if len(sys.argv) < 3:
    print("Two arguments are required: Domain Name and Root DNS IP Address")
    exit(1)

domainName = sys.argv[1]
rootDNSIP = sys.argv[2]

answer = 0

# print("The domain name to resolve " + domainName + " and the given root IP address is " + rootDNSIP)

rootDNSServers = {'198.41.0.4': 'a.root-servers.net',
                  '199.9.14.201': 'b.root-servers.net'
                  }

rootDNSName = "m.root-servers.net"
rootDNSPort = 53

clientSocket = socket(AF_INET, SOCK_DGRAM)


message = header() + questionSection(domainName)

clientSocket.sendto(binascii.unhexlify(message), (rootDNSIP, rootDNSPort))

modifiedMessage, serverAddress = clientSocket.recvfrom(4096)

answer = decodeResponse(binascii.hexlify(modifiedMessage).decode("utf-8"))

# print(binascii.unhexlify(header()))
# print(binascii.unhexlify(labelDomainName(domainName)))
# print(binascii.unhexlify(questionSection(domainName)))

clientSocket.close()