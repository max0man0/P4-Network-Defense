from scapy.all import sendp, get_if_hwaddr, conf
from scapy.layers.inet6 import Ether, IPv6, TCP
import psutil
import socket

# Parameters
PACKET_COUNT = 10
INTERFACE = "eth0"
SRC_MAC_ADDRESS = get_if_hwaddr(INTERFACE)
DST_MAC_ADDRESS = "02:01:01:01:00:01"
DST_IP = "2001:db8:1::1"
DST_PORT = 80

conf.iface = INTERFACE

def get_ipv6_address(interface_name):
    """
    Get the IPv6 address of a specified network interface that starts with '2001:'.

    Parameters:
        interface_name (str): Name of the network interface.

    Returns:
        str: IPv6 address of the interface starting with '2001:', or None if not found.
    """
    try:
        # Get all network interfaces and their addresses
        addresses = psutil.net_if_addrs()

        if interface_name not in addresses:
            raise ValueError(f"Interface '{interface_name}' not found.")

        # Iterate over the addresses of the given interface
        for address in addresses[interface_name]:
            if address.family == socket.AF_INET6:  # Check for IPv6 family
                ipv6_address = address.address.split('%')[0]  # Remove zone index if present
                if ipv6_address.startswith("2001:"):
                    return ipv6_address

        # If no matching IPv6 address is found
        return None

    except Exception as e:
        print(f"Error: {e}")
        return None

def send_tcp_packet():
    # Define Ethernet layer
    eth = Ether(src=SRC_MAC_ADDRESS, dst=DST_MAC_ADDRESS)

    # Define IPv6 layer
    src_ip = get_ipv6_address(INTERFACE)
    ipv6 = IPv6(src=src_ip, dst=DST_IP)

    # Define TCP layer
    tcp = TCP(dport=DST_PORT, flags="S")

    # Stack layers and send packet
    packet = eth / ipv6 / tcp
    sendp(packet)

if __name__ == "__main__":
    packets_sent = 0
    for i in range(PACKET_COUNT):
        send_tcp_packet()
        print(f"Sent TCP packet {i+1} to {DST_IP}.")
        packets_sent += 1
    print(f"Total packets sent: {packets_sent}.")