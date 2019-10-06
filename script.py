#!/usr/bin/env python

################################
from scapy.all import *        #  Imports
import sys                     #
################################






# - send_packets
# - - for each host, creates a packet and sends it
def send_packets(transport_proto, hosts, ports, toHTML):
    for x in hosts:
        s_p = create_packet(transport_proto, x, ports)
        send_packet(s_p, num_times, toHTML)


# - send_packet
# - - handles some outputting
# - - sends given packet a specified number of times
def send_packet(packet, num, toHTML):
    num = int(num)
    if toHTML:
        print("<br /><br /><br />")
    for i in range(num):
        #print("PRINTING PACKET")
        if toHTML:
            print("<li>")
        ans,unans = sr(packet,timeout=2)
        #an = sr1(packet, timeout=2)
        #an
        ans.nsummary()
        if toHTML:
            print("</li>")
        #unans.nsummary()
        #ans.summary()
        #packet.show()


# - create_packet
# - - given a protocol, host, and ports
# - - returns the scapy packet
def create_packet(transport_proto, host, ports):
    temp_IP = IP(dst=host)
    temp_TCP = TCP(dport=ports)
    temp_UDP = UDP(dport=ports)
    #sr1(IP(dst=host)/TCP(dport=ports))
    if transport_proto == 'TCP':
        temp_packet = temp_IP/temp_TCP
    else:
        temp_packet = temp_IP/temp_UDP
    return temp_packet




##############################################################################
#
#
#                  User-Input Section
#
#
##############################################################################


###############  GET HOSTS   #################################################
dest_hosts = []
print("")
print("Possible Formats:")
print("192.168.1.1")
print("192.168.1.1-255")
print("192.168.1.0/24")
host = raw_input("Destination Host: ")

try:
    host
except NameError:
    print("No Host set...exiting")
    exit()
else:
    if host == "":
        print("must include host. Exiting...")
        exit()
    else:
        split_host = host.split('.')
        #print((len(split_host)))
        if len(split_host) != 4:
            print("Incorrect IPv4 address format")
            exit()
        for octet in range(3):
            octet_val = split_host[octet]
            if not unicode(octet_val).isnumeric():
                print("bad octet, not numeric value")
                exit()
            elif int(octet_val) > 255:
                print("bad octet, numeric value too large")
                exit()
        last_octet = split_host[3].split('-')
        if len(last_octet) == 1:
            dest_hosts.append(host)
        else:
            low_num = int(last_octet[0])
            high_num = int(last_octet[1])
            num_nums = high_num - low_num + 1
            for i in range(num_nums):
                temp_str = split_host[0] + '.' + split_host[1] + '.' + split_host[2] + '.' + str(low_num + i)
                dest_hosts.append(temp_str)
            #for j in dest_hosts:
            #    print(j)



##################   GET Quick Ping Y/N   ####################################
is_ping = raw_input("Quick Ping? [y/N]: ")
if is_ping == "y":
    host_to_send_to = str(dest_hosts[0])
    #print(host_to_send_to)
    #temp_ip = IP(dest='192.168.1.1')
    #temp_icmp = ICMP()
    #print("hi")
    ans,unans = sr(IP(dst=dest_hosts)/ICMP(), timeout=2)
    ans.summary()
    exit()



####################   Get Ports to Array   #################################
ports = []
print("")
print("Comma separated ports (i.e. '22' or '20,21,80')")
port = raw_input("Destination Ports [80]: ")

try:
    port
except NameError:
    ports[0] = 80
    print("default port 80 set")
else:
    if port == "":
        ports.append(80)
        print("default port 80 used")
    elif unicode(port, 'utf-8').isnumeric():
        print("Port set to " + str(port))
        ports.append(int(port))
    else:
        temp_ports = port.split(',')
        for k in temp_ports:
            ports.append(int(k))
        #print("Invalid Port. Must be a number")
        #exit()


#####################   GET TRANSPORT PROTOCOL (TCP/UDP) #####################
transport_proto = raw_input("TCP or UDP [TCP]: ")

if transport_proto == "":
    transport_prot = 'TCP'


#####################   GET OUTPUT TYPE   ####################################
output_type = raw_input("Output to HTML? [Y/n]: ")

if output_type == "":
    toHTML = True
elif output_type == "Y":
    toHTML = True
else:
    toHTML = False



##############################   GET NUM TIMES TO SEND   #####################
num_times = raw_input("How many times would you like to send each packet?[1]: ")
if num_times == "":
    num_times = 1



# - For writing output to HTML file
if toHTML:
    sys.stdout = open('script_output.html', 'w')
    print("<html><head><title>Python Output</title></head><body>")

# - Take Inputs from Above and send packets
send_packets(transport_proto, dest_hosts, ports, toHTML)

# - Close HTML file
if toHTML:
    print("</body></html>")
    sys.stdout.close()

