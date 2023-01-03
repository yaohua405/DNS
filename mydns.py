# clean code with comments DNS query, with methodology and technicalities

import sys
import os
import struct
import binascii
import codecs
from socket import socket, AF_INET, SOCK_DGRAM

# get server name and ip address from command line
if len(sys.argv) != 3:
	print('Usage: mydns domain-name root-dns-ip')    
	sys.exit()
domainName = sys.argv[1]
rootDNSip = sys.argv[2]

# create socket
udpsocket = socket(AF_INET, SOCK_DGRAM)
udpsocket.settimeout(5)

def convertDomainName(domainName):
    qname = ""                # The temporary string that will contain the encoded characters for the labels in the domainName.
    finalqname = ""           # The string to be returned for use in the next method questionection.
    length_of_label = 0       # Temporary variable used as placeholder to keep track of the length of the current label of domainName.
    currentPosition = 0       # Keeps track of the current position when traversing domain name.
    second_index = 0          # Keeps track of the characters up to the dot.
    for i in domainName:
        if i != '.':         
            currentPosition += 1 # If we did not encounter a dot then go to the next character's index.
        elif i == '.':
            qname +=str(hex(currentPosition))   
            # If a dot was found then we need the total length of characters up to the dot so encode that number in hexadecimal notation.
            while second_index < currentPosition:    
                # Traverse as long as the number of characters before the currentPosition number has not been reached yet.
                qname += str(codecs.encode(binascii.a2b_qp(domainName[length_of_label + second_index]), "hex")) 
                # Encode characters up to the dot first from hex to binary, then encode it to binary data.
                second_index += 1 # Increment to the next character's position in domain name to encode.
            length_of_label += second_index + 1 
            # Update the length of the label so that it starts at the first character after a dot was found which is second_index + 1.
            currentPosition = 0   # Reset since characters up to the dot found have been encoded.
            second_index = 0       # Reset so that when next dot is found we can do the proper traversal.
            
    qname += str(hex(currentPosition))  
    # Convert the number currentPosition currently has to hexadecimal since this part entails converting the part of the domainName after
    # the last dot was found to hexadecimal. Basically converting the total length of the last label found in domainName.
    
    for x in range(second_index, currentPosition): # Traversing the last label of the domainName.
        qname += str(codecs.encode(binascii.a2b_qp(domainName[length_of_label + x]), "hex"))   # Encode each character of that last label.
        x += 1   # Increment the traversal index by 1.
        
    qname += '00'  # q name always ends with 00.
    
    finalqname += qname.replace("b", "").replace("'", "").replace("0x", "0")       
    # Replacing the 0x and the b from the hex and binary conversions with 0.
    
    return finalqname  # Return the string.

def dnsQuery(domainName):
	id = '0010'
	secondRow = '0000'
	qdcount = '0001'
	ancount = '0000'
	nscount = '0000'
	arcount = '0000'

	header = id + secondRow + qdcount + ancount + nscount + arcount

	qname = convertDomainName(domainName)
	qtype = '0001'
	qclass = '0001'

	question = qname + qtype + qclass

	return header + question

def decodeResponse(message):

	if message[0:4] != '0010':
		print("Wrong response.")
		exit(1)
	if message[4:8] != '8000':
		print("There was an error in the response.")
		exit(1)

	question = int(message[8:12], 16)
	answers = int(message[12:16], 16)
	authority = int(message[16:20], 16)
	additionalInfo = int(message[20:24], 16)

	rrposition = message.find("00010001", 25, len(message))
	rrArray = [0]
	authorHexArray = []
	authorArray = []
	addHexArray = []

	i = rrposition + 8

	while i < (len(message) - (24 * additionalInfo)):
		
		if not authorHexArray:
			authorHexArray.append(message[i:i+62])
			i += 62
		else:
			authorHexArray.append(message[i:i+32])
			i += 32


	for x in authorHexArray:
		
		print("DNS server to query: " + rootDNSip)
		print("Reply received. Content overview:\n\t" +
				str(answers) + " Answers.\n\t" +
				str(authority) + " Intermediate Name Servers.\n\t" +
				str(additionalInfo) + " Additional Information Records.")
		j = answers
		k = authority
		e = additionalInfo
		print("Answers Section:")
		# make a loop to print each answer section
		while j > 0:
			print("Name: " + "\tIP: ")
			j = j - 1
		print("Authority Section:")
		# loop
		while k > 0:
			print("Name: " + "\tName Server: ")
			k = k - 1
		print("Additional Information Section:")
		# loop
		while e > 0:
			print("Name: "  + "\tIP: " )
			e = e - 1
		

	return int(answers)


dns_message = dnsQuery(domainName)

udpsocket.sendto(binascii.unhexlify(dns_message), (rootDNSip, 53))

dnsMsg_data, serverAddress = udpsocket.recvfrom(1024)

response = decodeResponse(binascii.hexlify(dnsMsg_data).decode("utf-8"))

	
udpsocket.close()
