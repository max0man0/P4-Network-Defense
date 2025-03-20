#!/bin/bash

# Check if PID is provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 host"
    exit 1
fi

# Base PID from the argument
base_pid=$(ps aux | grep "mininet:$1" | grep -v grep | awk '{print $2}' | head -n 1)

# Check if base_pid is valid
if [ -z "$base_pid" ]; then
    echo "Error: Could not find the process for mininet:$1"
    exit 1
fi

# List of host PIDs based on the formula: h101_PID, h101_PID+2, h101_PID+4, ..., h101_PID+10
host_pids=($(seq $base_pid 2 $((base_pid + 10))))

# Set the PID of h0
h0_pid=$(ps aux | grep "mininet:h0" | grep -v grep | awk '{print $2}' | head -n 1)

# Add the PID of h0 to the list
host_pids+=($h0_pid)

# Define the path to the python script and the python interpreter
script_path="send_dad.py"
python_interpreter="/home/mez/p4dev-python-venv/bin/python"


# Execute the script on each host using mnexec
for host_pid in "${host_pids[@]}"; do
    # Extract the IPv6 Global Unique Address
    ipv6_addr=$(mnexec -a "$host_pid" ip -6 addr show eth0 | awk '/inet6 2001:/ {print $2; exit}')

    # Check if an IPv6 address was found
    if [ -z "$ipv6_addr" ]; then
        echo "Error: No valid IPv6 address starting with 2001 found for host with PID $host_pid."
        exit 1
    fi

    echo "Using IPv6 address $ipv6_addr for host with PID $host_pid..."

    # Execute the script on the host
    mnexec -a "$host_pid" nohup "$python_interpreter" "$script_path" > /dev/null 2>&1 &

    echo "Script started on host PID $host_pid"
done

echo "Script executed on all specified hosts."
