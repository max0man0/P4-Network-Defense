encoded_values = {'2001:db8:1::2': 0, '2001:db8:1::3': 1, '2001:db8:1::4': 2, '2001:db8:1::5': 3, '2001:db8:1::6': 4, '2001:db8:1::7': 5, '2001:db8:2::1': 6, '2001:db8:2::10': 7, '2001:db8:2::11': 8, '2001:db8:2::12': 9, '2001:db8:2::13': 10, '2001:db8:2::14': 11, '2001:db8:2::2': 12, '2001:db8:2::3': 13, '2001:db8:2::4': 14, '2001:db8:2::5': 15, '2001:db8:2::6': 16, '2001:db8:2::7': 17, '2001:db8:2::8': 18, '2001:db8:2::9': 19, '2001:db8:2::a': 20, '2001:db8:2::b': 21, '2001:db8:2::c': 22, '2001:db8:2::d': 23, '2001:db8:2::e': 24, '2001:db8:2::f': 25, '2001:db9:1::1': 26, '2001:db9:1::10': 27, '2001:db9:1::11': 28, '2001:db9:1::12': 29, '2001:db9:1::13': 30, '2001:db9:1::14': 31, '2001:db9:1::2': 32, '2001:db9:1::3': 33, '2001:db9:1::4': 34, '2001:db9:1::5': 35, '2001:db9:1::6': 36, '2001:db9:1::7': 37, '2001:db9:1::8': 38, '2001:db9:1::9': 39, '2001:db9:1::a': 40, '2001:db9:1::b': 41, '2001:db9:1::c': 42, '2001:db9:1::d': 43, '2001:db9:1::e': 44, '2001:db9:1::f': 45, '2001:dba:0:100::1': 46, '2001:dba:0:100::10': 47, '2001:dba:0:100::11': 48, '2001:dba:0:100::12': 49, '2001:dba:0:100::13': 50, '2001:dba:0:100::14': 51, '2001:dba:0:100::2': 52, '2001:dba:0:100::3': 53, '2001:dba:0:100::4': 54, '2001:dba:0:100::5': 55, '2001:dba:0:100::6': 56, '2001:dba:0:100::7': 57, '2001:dba:0:100::8': 58, '2001:dba:0:100::9': 59, '2001:dba:0:100::a': 60, '2001:dba:0:100::b': 61, '2001:dba:0:100::c': 62, '2001:dba:0:100::d': 63, '2001:dba:0:100::e': 64, '2001:dba:0:100::f': 65, '2001:dbb:0:100::1': 66, '2001:dbb:0:100::10': 67, '2001:dbb:0:100::11': 68, '2001:dbb:0:100::12': 69, '2001:dbb:0:100::13': 70, '2001:dbb:0:100::14': 71, '2001:dbb:0:100::2': 72, '2001:dbb:0:100::3': 73, '2001:dbb:0:100::4': 74, '2001:dbb:0:100::5': 75, '2001:dbb:0:100::6': 76, '2001:dbb:0:100::7': 77, '2001:dbb:0:100::8': 78, '2001:dbb:0:100::9': 79, '2001:dbb:0:100::a': 80, '2001:dbb:0:100::b': 81, '2001:dbb:0:100::c': 82, '2001:dbb:0:100::d': 83, '2001:dbb:0:100::e': 84, '2001:dbb:0:100::f': 85, '2001:dbc:0:1::1': 86, '2001:dbc:0:1::10': 87, '2001:dbc:0:1::11': 88, '2001:dbc:0:1::12': 89, '2001:dbc:0:1::13': 90, '2001:dbc:0:1::14': 91, '2001:dbc:0:1::2': 92, '2001:dbc:0:1::3': 93, '2001:dbc:0:1::4': 94, '2001:dbc:0:1::5': 95, '2001:dbc:0:1::6': 96, '2001:dbc:0:1::7': 97, '2001:dbc:0:1::8': 98, '2001:dbc:0:1::9': 99, '2001:dbc:0:1::a': 100, '2001:dbc:0:1::b': 101, '2001:dbc:0:1::c': 102, '2001:dbc:0:1::d': 103, '2001:dbc:0:1::e': 104, '2001:dbc:0:1::f': 105}

SRC_NETWORKS = (
    "2001:db8:2::",
    "2001:db9:1::",
    "2001:dba:0:100::",
    "2001:dbb:0:100::",
    "2001:dbc:0:1::"
)
HOST_COUNT_PER_NETWORK = 20

def generate_network1_addresses():
    network_address = "2001:db8:1::"
    host_count = 7
    addresses = []
    # starts from 2 because the first address is not encoded
    for i in range(2, host_count + 1):
        if i < 0x10:
            addresses.append(f"{network_address}{i:1x}")
        else:
            addresses.append(f"{network_address}{i:02x}")
    return addresses

def generate_src_ipv6_addresses(host_count_per_network: int, src_networks: tuple):
    addresses = generate_network1_addresses()
    for network in src_networks:
        for i in range(1, host_count_per_network + 1):
            if i < 0x10:
                addresses.append(f"{network}{i:1x}")
            else:
                addresses.append(f"{network}{i:02x}")
            
    return addresses

if __name__ == "__main__":
    # check if the all of the generated addresses are keys in the encoded_values dictionary
    # print all of the addresses that are not in the dictionary
    print("Addresses not in the dictionary:")
    addresses_not_in_dict = []
    for address in generate_src_ipv6_addresses(HOST_COUNT_PER_NETWORK, SRC_NETWORKS):
        if address not in encoded_values:
            addresses_not_in_dict.append(address)
    
    
    for address in addresses_not_in_dict:
        
        print(address)
    print(f"Total addresses not in the dictionary: {len(addresses_not_in_dict)}")