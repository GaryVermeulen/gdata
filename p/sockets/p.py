import random
import socket
import time
import ipaddress
import struct

from threading import Thread

def checksum(source_string):
    sum = 0
    count_to = (len(source_string) / 2) * 2
    count = 0
    while count < count_to:
        this_val = source_string[count + 1] * 256 + source_string[count]
        sum = sum + this_val
        sum = sum & 0xffffffff
        count = count + 2
    if count_to < len(source_string):
        sum = sum + source_string[len(source_string) - 1]
        sum = sum & 0xffffffff
    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def create_packet(id):
    header = struct.pack('bbHHh', 8, 0, 0, id, 1)
    data = 192 * b'Q'
    my_checksum = checksum(header + data)
    header = struct.pack('bbHHh', 8, 0, socket.htons(my_checksum), id, 1)
    return header + data


def ping(addr, timeout=1):
    print("ping: " + str(addr))
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    except Exception as e:
        print ("Exception caught (e): " + e)
    packet_id = int((id(timeout) * random.random()) % 65535)
    packet = create_packet(packet_id)
    try:
        my_socket.connect((addr, 80))
    except Exception as e1:
        print("Exception caught (e1): " + str(e1))
    my_socket.sendall(packet)
    my_socket.close()


def rotate(addr, file_name, wait, responses):
    print ("Sending Packets", time.strftime("%X %x %Z"))
    for ip in addr:
##        print("rotate: " + str(ip))
        try:
            ping(str(ip))
        except Exception as pe:
            print("Exception caught in rotate calling ping: " + str(pe))
        time.sleep(wait)
    print ("All packets sent", time.strftime("%X %x %Z"))

    print ("Waiting for all responses")
    time.sleep(2)

    # Stoping listen
    global SIGNAL
    SIGNAL = False
    ping('127.0.0.1')  # Final ping to trigger the false signal in listen

    print("responses type: " + str(type(responses)))
    print (len(responses), "hosts found!")
    print ("Writing File")
    hosts = set()
    print(hosts)
    r = 0
    for response in sorted(responses):
        ip = struct.unpack('BBBB', response)
        ip = str(ip[0]) + "." + str(ip[1]) + "." + str(ip[2]) + "." + str(ip[3])
        hosts.add(ip)
        r += 1
##        print(str(response))
        print("r: " + str(r) + " >" + str(ip) + "<")
   
    for ips in hosts:
        print(ips)
    
    print("b4 open file")    
    with open(file_name, 'w') as file:
##        file.write('\n'.join(sorted(hosts, key=lambda item: socket.inet_aton(item))))
        for ips in hosts:
            file.write(ips + "\n")

    print ("Done", time.strftime("%X %x %Z"))


def listen(responses):
    global SIGNAL
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    s.bind(('', 1))
    print ("Listening")
    while SIGNAL:
        packet = s.recv(1024)[:20][-8:-4]
        responses.append(packet)
    print ("Stop Listening")
    s.close()

SIGNAL = True

responses = []

##ips = '192.168.1.0/28' # Internet network
ips = '10.0.0.0/28' # Internet network
wait = 0.002  # Adjust this based in your bandwidth (Faster link is Lower wait)
file_name = 'log1.txt'

ip_network = ipaddress.ip_network(ips, strict=False)

t_server = Thread(target=listen, args=[responses])
t_server.start()

t_ping = Thread(target=rotate, args=[ip_network, file_name, wait, responses])
t_ping.start()
