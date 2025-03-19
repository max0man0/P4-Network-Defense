import random
import time
from datetime import datetime, timedelta
from scapy.all import *
from scapy.layers.inet6 import IPv6, ICMPv6ND_RA, ICMPv6NDOptPrefixInfo, ICMPv6NDOptMTU, ICMPv6NDOptSrcLLAddr

# Parameters
MTU = 1500
MAC_ADDRESS = get_if_hwaddr("eth0")  # Replace 'conf.iface' if needed with specific interface
PREFIX = "2001:db8::"

# set scapy interface
conf.iface = "eth0"

def create_ra_packet(prefix) -> Packet:
    # Construct the Router Advertisement packet with required options
    ra_packet = IPv6(dst="ff02::1") / ICMPv6ND_RA()
    ra_packet /= ICMPv6NDOptMTU(mtu=MTU)
    ra_packet /= ICMPv6NDOptSrcLLAddr(lladdr=MAC_ADDRESS)
    ra_packet /= ICMPv6NDOptPrefixInfo(prefix=prefix, prefixlen=64, L=1, A=1, validlifetime=0xffffffff, preferredlifetime=0xffffffff)
    return ra_packet

# Calculate current prefix based on the increment
ra_packet = create_ra_packet(PREFIX)

# Send the packet to the all-nodes multicast address
ra_packet.show()
send(ra_packet)
print(f"Sent Normal RA with prefix: {PREFIX}")
