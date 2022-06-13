import codecs
import sys
import socket
import binascii

if len(sys.argv) != 3:
    print('Usage: mydns domain_name root_dns_ip')
    sys.exit()
domain_name = sys.argv[1]
root_dns_ip = sys.argv[2]
bufferSize = 512


# Returns a list of integers. These integers are the 'labels' of the name section of the query section of the message.
def return_numbers(domain_Name):
    list_num = []
    count = 0
    for x in range(len(domain_Name)):
        if domain_Name[x] == '.':
            list_num.append(count)
            count = 0
        elif x == len(domain_Name)-1:
            list_num.append(count + 1)
            count = 0
        else:
            count += 1
    return list_num

# Automates the creation of a dns message.
def create_Message(domain_Name):
    first_part = "BE EE 01 00 00 01 00 00 00 00 00 00 "
    last_part = "00 00 01 00 01"
    counter = 0
    numbers = return_numbers(domain_Name)
    if len(hex(numbers[counter])) < 4:
        first_part += '0' + f'{hex(numbers[counter])} '.strip('0x')
    else:
        first_part += f'{hex(numbers[counter])} '.strip('0x')
    for x in domain_Name:
        if x != '.':
            if len(hex(ord(x))) < 4:
                first_part += '0' + f'{hex(ord(x))} '.strip('0x')
            else:
                first_part += f'{hex(ord(x))} '.strip('0x')
        else:
            counter += 1
            if len(hex(numbers[counter])) < 4:
                first_part += '0' + f'{hex(numbers[counter])} '.strip('0x')
            else:
                first_part += f'{hex(numbers[counter])} '.strip('0x')

    message = first_part + last_part
    message = message.replace(' ', '').replace('\n', '')
    return message

# Returns the first two numbers from received data.
def get_byte(data):
    return data[0:2]

# Function for personal use (testing).
def display_bytes(data):
    counter = 0
    question = 0
    hold_num = -1
    print('\n\n\n')
    while counter <= len(data):
        #prints new line for the whole header
        if counter == 24:
            print()
        #prints new line for the question section
        if counter >= 24 and question == 0:
            if get_byte(data[counter:counter+3]) == '00':
                print('00', end=' ')
                question = 1
                for x in range(4):
                    print(get_byte(data[counter+2:counter+5]), end=' ')
                    counter += 2
                hold_num = counter + 26
                counter += 2
                print()
        if counter == hold_num:
            print()

        #responsible for printing most characters
        print(get_byte(data[counter:counter+3]), end=' ')
        counter += 2
    print('\n\n\n')

# Called to create a socket and send a message to the specified ip address.
def send_message(message, ip_address):
    primary_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = create_Message(domain_name)
    server_address = (ip_address, 53)
    primary_socket.sendto(binascii.unhexlify(message), server_address)
    data, _ = primary_socket.recvfrom(4096 * 4)
    primary_socket.close()
    data = give_Ouput(data)
    return data

# Converts array of bytes to array of hex values.
def give_Ouput(data):
    data = binascii.hexlify(data).decode('utf-8')
    return data


# Returns the intermediate server's ip address for later use
def obtain_ip(data):
    ip = ''
    skip = (len(domain_name)+1) * 2 + 34
    header = data[skip:skip+4]
    counter = (len(domain_name)+1) * 2 + 34
    iterations = int(data[16:20], 16)
    for x in range(iterations):
        counter += 20
        counter += int(data[counter:counter+4], 16) * 2 + 4
    counter += 24

    temp = int(data[counter - 4:counter], 16)
    while temp != 4:
        counter += temp * 2
        counter += 24
        temp = int(data[counter - 4:counter], 16)

    ip += f'{int(data[counter:counter + 2], 16)}.'
    ip += f'{int(data[counter + 2:counter + 4], 16)}.'
    ip += f'{int(data[counter + 4:counter + 6], 16)}.'
    ip += f'{int(data[counter + 6:counter + 8], 16)}.'
    return ip[:len(ip)-1]

# Obtains the final IP address once the while loop has ceased.
def obtain_answer_ip(data):
    ip = ''
    counter = (len(domain_name) + 1) * 2 + 58
    ip += f'{int(data[counter:counter + 2], 16)}.'
    ip += f'{int(data[counter + 2:counter + 4], 16)}.'
    ip += f'{int(data[counter + 4:counter + 6], 16)}.'
    ip += f'{int(data[counter + 6:counter + 8], 16)}.'
    return ip[:len(ip) - 1]


# Returns positive integer value if there is an answer to the query. Used to control iterations.
def answer_obtained(data):
    greater_than_zero = 0
    greater_than_zero = data[14:16]
    greater_than_zero = int(greater_than_zero)
    if greater_than_zero > 0:
        return 1
    else:
        return 0


# Where the main code begins:
message = create_Message(domain_name)
data = send_message(message, sys.argv[2])
#display_bytes(data)

ip = obtain_ip(data)
print('\n\nIntermediate IP addresses: \n\n')
print(ip, end= '\n\n')

# If there is no answer in the received data, then a different server is chosen to query.
while answer_obtained(data) == 0:
    message = create_Message(domain_name)
    data = send_message(message, ip)
    ip = obtain_ip(data)
    #display_bytes(data) # Toggle this comment to see the data visualized for testing.
    print(ip, end= '\n\n')

print(f'\n\n Answer IP: {obtain_answer_ip(data)} \n\n')


