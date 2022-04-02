import ipaddress
import sys
import socket
import time
import argparse

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

    # Define variables
    OUTPUT_FILE='scan.json'
    PORT_START=1
    PORT_END=140
    
    # Get params from CLI
    aparse = argparse.ArgumentParser(description='Options for creating a network scanner.')
    aparse.add_argument("-s", "--start", type=int, help="Start port, default value 1")
    aparse.add_argument("-e", "--end", type=int, help="End port, default value 1024")
    aparse.add_argument("-i", "--ip", help="IP Address to scan (e.g. 10.1.1.1)")
    aparse.add_argument("-n", "--network", help="Network to scan (IPv4 format)")    
    args = aparse.parse_args()
    
    if args.start is not None:
        PORT_START = args.start

    if args.end is not None:
        PORT_START = args.end
    
    if args.ip is not None:
        try:
            ipaddress.ip_address(args.ip)
        except:
            print("ERROR: IP address is not valid!")
            aparse.print_help()
            sys.exit()
        targetIps = [socket.gethostbyname(args.ip)]
        print(targetIps)
    
    if args.network is not None:
        targetIps = ipaddress.ip_network(args.network).hosts()

    # Parsing check
    # IP or network required
    if args.network is None and args.ip is None:
        print("ERROR: Specify IP address or Network to scan!")
        aparse.print_help()
        sys.exit()
        
    # Ports check        
    if PORT_START > PORT_END:
        print("ERROR: Starting port value has to be lower than ending port value!")
        aparse.print_help()
        sys.exit()
    
    if PORT_START not in range(1,65535) or PORT_END not in range (1,65536):
        print("Error: Defined ports are not valid!")
        aparse.print_help()
        sys.exit()  
    
       

    for ip in targetIps:
        # Add Intro information
        print("-" * 50)
        print("Scanning Target: " + str(ip))
        print("-" * 50) 
        scan_host(str(ip), PORT_START, PORT_END)
    
    print('Time taken:', time.time() - startTime)


if __name__ == "__main__":
    main()
