import os
import random
import time
from scapy.all import sendp, get_if_hwaddr, conf
from scapy.layers.inet6 import IPv6, ICMPv6ND_NS, Ether

# Parameters
ATTACK_DURATION = 5 * 60 # Duration of the attack in seconds (5 minutes)
SEND_INTERVAL = 5  # Duration between sending NSs in seconds
MTU = 1500
INTERFACE = "eth0"
SRC_MAC_ADDRESS = get_if_hwaddr(INTERFACE)  # Replace 'conf.iface' if needed with specific interface
DST_MAC_ADDRESS = "02:01:01:01:00:02"
TARGET_IP = "2001:db8:2::1"

conf.iface = INTERFACE

def send_neighbor_solicitations(interface: str, interval : int = SEND_INTERVAL, duration : int = ATTACK_DURATION, target_ip : str = TARGET_IP):
    """
    Sends Neighbor Solicitations at a fixed rate for a specified duration, 
    on a specified target IP address.

    :param str interface: Network interface to send the advertisements from.
    :param int rate: Number of advertisements to send per second.
    :param int duration: Total time to send advertisements, in seconds.
    """
    # Send packets
    try:
        start_time = time.time()
        end_time = start_time + duration
        i = 0
        while time.time() < end_time:
            # Construct the NS packet
            ns_packet = Ether(src=SRC_MAC_ADDRESS, dst=DST_MAC_ADDRESS) \
                / IPv6(dst=target_ip) / ICMPv6ND_NS(tgt=target_ip)

            # Show the packet
            ns_packet.show()

            # Send the packet
            sendp(ns_packet, iface=interface, verbose=False)

            # Introduce a random link latency (5-30 ms delay) to simulate network conditions
            link_latency = 0.005 + (0.025 - 0.005) * random.random()

            # Sleep to maintain the desired rate
            time.sleep(interval + link_latency)

            # print progress every 5 seconds
            if i % 5 == 0:
                elapsed = time.time() - start_time
                print(f"Sent {(i + 1)} NSs in {elapsed:.2f} seconds...")
            
            i += 1
    except KeyboardInterrupt:
        print("\nStopped sending Neighbor Solicitations.")
        
    print(f"Finished: Sent {i} NSs in {time.time() - start_time:.2f} seconds.")

if __name__ == "__main__":
    trigger_file = "start.trigger"
    # check if the trigger file exists
    while not os.path.exists(trigger_file):
        time.sleep(0.1)
    print("Start sending RAs...")
    
    send_neighbor_solicitations(interface=INTERFACE, interval=SEND_INTERVAL, duration=ATTACK_DURATION, target_ip=TARGET_IP)
