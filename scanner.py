import sys
import socket
import time
import argparse

# Define variables
OUTPUT_FILE='scan.json'
DEFAULT_PORT_START=1
DEFAULT_PORT_END=140

def scan_port(host, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(0.1)

            # returns an error indicator
            result = s.connect_ex((host, port))
            if result == 0:
                print("Port{}/tcp open".format(port))
            s.close()
        except KeyboardInterrupt:
            print("\n Exiting program by user")
            sys.exit()
        except socket.gaierror:
            print("\n Hostname Could Not Be Resolved")
            sys.exit()
        except socket.error:
            print("\ Error: Server not responding.")
            sys.exit()

def scan_host(host, startPort, endPort):
    for port in range(startPort, endPort):
            scan_port(host, port)

def main():

    startTime = time.time()
    # Defining a target
    if len(sys.argv) == 2:
        # translate hostname to IPv4
        target = socket.gethostbyname(sys.argv[1])
    else:
        print("Invalid amount of Argument")

    # Add Intro information
    print("-" * 50)
    print("Scanning Target: " + target)
    print("-" * 50)    

    scan_host(target, startPort=DEFAULT_PORT_START, endPort=DEFAULT_PORT_END)
    
    

    print('Time taken:', time.time() - startTime)


if __name__ == "__main__":
    main()
