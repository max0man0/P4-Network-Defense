import sys
import os
import multiprocessing
from csv import writer

def print_percentage(queue: multiprocessing.Queue, total: int):
    print("print_percentage | Starting...")
    try:
        while True:
            iteration = queue.get()
            if iteration is None:  # Sentinel value to stop the process
                break
            percent = ("{0:.1f}").format(100 * (iteration / float(total)))
            sys.stdout.write(f'\r{percent}% Complete')
            sys.stdout.flush()
    except KeyboardInterrupt:
        print("\nprint_percentage | Interrupted.")
    finally:
        print("\nprint_percentage | Finished.")
        sys.stdout.flush()

def prepare_write_results():
    print("write_results | Emptying tests.csv file...")
    # empty tests.csv file
    open('tests.csv', 'w').close()

    print("write_results | writing header to tests.csv file...")
    with open('tests.csv', 'a', newline='') as csvfile:
        csvwriter = writer(csvfile)
        # Write the header only if the file is empty
        if csvfile.tell() == 0:
            csvwriter.writerow(["key", "hash1", "hash2", "hash3", "passed"])

def write_results(queue: multiprocessing.Queue):
    with open('tests.csv', 'a', newline='') as csvfile:
        csvwriter = writer(csvfile)        
        print(f"write_results {os.getpid()} | writing results to tests.csv file...")
        try:
            while True:
                key = queue.get()
                if key is None:  # Sentinel value to stop the process
                    break
                hashes = hash(key)
                passed = hashes[1] == hashes[2]
                row = [key, hashes[0], hashes[1], hashes[2], passed]
                csvwriter.writerow(row)
        except KeyboardInterrupt:
            print(f"\nwrite_results {os.getpid()} | Interrupted.")
        finally:
            print(f"write_results {os.getpid()} | Finished.")

def hash(key):
    h = 0
    h = h + key
    h = h + (h << 10)
    h = h ^ (h >> 6)
    hash1 = h % 1024

    h = h + (h << 3)
    h = h ^ (h >> 11)
    hash2 = h % 1024

    h = h + (h << 15)
    hash3 = h % 1024

    return hash1, hash2, hash3

# def jenkins_hash(key):
#     # Split the 32-bit key into four 8-bit chunks
#     # the bytes are 32 bits long to add them to the hash_result
#     # (both need to be the same size)
#     byte0 = key & 0xFF
#     byte1 = (key >> 8) & 0xFF
#     byte2 = (key >> 16) & 0xFF
#     byte3 = (key >> 24) & 0xFF

#     # Initialize hash to zero
#     hash_result = 0

#     # Process each byte, following the JOAT steps
#     hash_result = hash_result + byte0
#     hash_result = hash_result & 0xFFFFFFFF
#     hash_result = hash_result + (hash_result << 10)
#     hash_result = hash_result & 0xFFFFFFFF
#     hash_result = hash_result ^ (hash_result >> 6)

#     hash_result = hash_result + byte1
#     hash_result = hash_result & 0xFFFFFFFF
#     hash_result = hash_result + (hash_result << 10)
#     hash_result = hash_result & 0xFFFFFFFF
#     hash_result = hash_result ^ (hash_result >> 6)

#     hash_result = hash_result + byte2
#     hash_result = hash_result & 0xFFFFFFFF
#     hash_result = hash_result + (hash_result << 10)
#     hash_result = hash_result & 0xFFFFFFFF
#     hash_result = hash_result ^ (hash_result >> 6)

#     hash_result = hash_result + byte3
#     hash_result = hash_result & 0xFFFFFFFF
#     hash_result = hash_result + (hash_result << 10)
#     hash_result = hash_result & 0xFFFFFFFF
#     hash_result = hash_result ^ (hash_result >> 6)

#     # Final mixing steps
#     hash_result = hash_result + (hash_result << 3)
#     hash_result = hash_result & 0xFFFFFFFF
#     hash_result = hash_result ^ (hash_result >> 11)
#     hash_result = hash_result + (hash_result << 15)
#     hash_result = hash_result & 0xFFFFFFFF

#     return hash_result


# def get_hashes(src_addr, dst_addr):
#     # first 32 bits of src_addr
#     src_addr_p1 = src_addr & 0xFFFFFFFF
#     # the next 32 bits of src_addr
#     src_addr_p2 = (src_addr >> 32) & 0xFFFFFFFF
    
#     # first 32 bits of dst_addr
#     dst_addr_p1 = dst_addr & 0xFFFFFFFF
#     # the next 32 bits of dst_addr
#     dst_addr_p2 = (dst_addr >> 32) & 0xFFFFFFFF 

#     input1 = src_addr_p1 ^ dst_addr_p2
#     input2 = src_addr_p2 ^ dst_addr_p1
#     input3 = src_addr_p1 ^ dst_addr_p1

#     return jenkins_hash(input1), jenkins_hash(input2), jenkins_hash(input3)


def main():
    # 
    keys = range(0, 0xFFFFFFF + 1)
    print("Main process | Testing keys 0 to 0xFFFFFF...")
    passed = True

    # prepare the tests.csv file
    prepare_write_results()

    print("Main process | Starting the processes...")
    # Create a multiprocessing Queue to communicate with the print_percentage and write_results processes
    write_queue1 = multiprocessing.Queue()
    write_queue2 = multiprocessing.Queue()
    write_queue3 = multiprocessing.Queue()


    # Start the print_percentage and write_results processes
    writing_process1 = multiprocessing.Process(target=write_results, args=(write_queue1,))
    
    try:
        # progress_process.start()
        # writing_process1.start()
        pass_count = 0
        fail_count = 0
        for i, key in enumerate(keys):
            # print(f"Main process | {i}:##")
            hashes = hash(key)

            passed = hashes[1] == hashes[2]

            if passed:
                pass_count += 1
            else:
                fail_count += 1

            # Send the test results to the write_results process
            # print(f"Main process | ##### {i}")
            # write_queue1.put(key)

            # Send current iteration to the print_percentage process
            # progress_queue.put(i + 1)

            # if not passed:
            #     print(f"\nMain process | Failed for key {key}. Hashes: {hashes}")
            #     break
        print(f"\nMain process | {i}")
    except KeyboardInterrupt:
        print("\nMain process | Interrupted.")
    finally:
        print("\nMain process | Finishing...")
        # Signal the processes to stop
        write_queue1.put(None)
        write_queue2.put(None)
        write_queue3.put(None)

        print("Main process | Joining the processes...")
        # Wait for the processes to finish
        # writing_process1.join()
        
        

        print("Main process | Closing the queues...")
        # Close the queues
        write_queue1.close()
        write_queue2.close()
        write_queue3.close()

        print("Main process | Closing the processes...")
        # Terminate the processes
        # writing_process1.close()
        
        

        # Print the final result
        # print("Main process | Test results written to the file 'tests.csv'.")
        total_tests = pass_count + fail_count
        print(f"Main process | {pass_count} tests passed.")
        print(f"Main process | {fail_count} tests failed.")
        print(f"Main process | {total_tests} tests total.")

        return

if __name__ == "__main__":
    main()