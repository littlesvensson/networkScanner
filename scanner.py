import ipaddress
import json
import sys
import socket
import time
import argparse

OUTPUT_FILE='scan.json'

def scan_port(host, port, results):  
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.1)
        result = s.connect_ex((host, port))
        if result == 0:
            results[host]["ports"].append(port)
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

def scan_host(host, startPort, endPort, results):
    if host not in results:
        results.update({host: {"ports": []}})
        previous_results = []
    else:        
        previous_results= list(results[host]["ports"])
        results[host]["ports"].clear()
    for port in range(startPort, endPort+1):
            scan_port(host, port, results)
    # Results comparison
    new_results = list(results[host]["ports"])
    # print(new_scan)
    if previous_results != new_results or (previous_results is None and new_results is None):
        print("Differences for host {} found!".format(host))
        print("Current output:")
        for ports in results[host]["ports"]:
            print("Ports: {1}/tcp/open".format(host, ports))
        print("Previous output:")
        for ports in previous_results:
            print("Ports: {1}/tcp/open".format(host, ports))
    else:
        print("Host {}: No difference in open ports found in the current scan".format(host))
        print("Current output:")
        for ports in results[host]["ports"]:
            print("Ports: {1}/tcp/open".format(host, ports))   
    

def main():
    # Define variables    
    PORT_START=1
    PORT_END=1024
    results={}
    
    # Get params from CLI
    aparse = argparse.ArgumentParser(description='Options for creating a network scanner.')
    aparse.add_argument("-s", "--start", type=int, help="Start port, default value 1")
    aparse.add_argument("-e", "--end", type=int, help="End port, default value 1024")
    aparse.add_argument("-i", "--ip", help="IP Address(e.g. 10.1.1.1) or network (e.g. 192.168.1.0/24) to scan ") 
    args = aparse.parse_args()
    
    if args.start is not None:
        PORT_START = args.start

    if args.end is not None:
        PORT_START = args.end
    
    #if args.ip is not None:
    #    try:
    #        ipaddress.ip_address(args.ip)
    #    except:
    #        print("ERROR: IP address is not valid!")
    #        aparse.print_help()
    #        sys.exit()
    #    targetIps = [socket.gethostbyname(args.ip)]
    
    if args.ip is not None:
        targetIps = ipaddress.ip_network(args.ip).hosts()

    # Parsing check
    # IP or network required
    if args.ip is None:
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
    
    ## Open file with past data if exists
    try:
        with open(OUTPUT_FILE, "r") as file:
            results = json.load(file)
    except IOError:
        pass

    for ip in targetIps:
        print("-" * 50)
        print("Scanning Target: " + str(ip))

        scan_host(str(ip), PORT_START, PORT_END, results)
    
    # Save results
    with open(OUTPUT_FILE,"w") as file:
        json.dump(results,file)


if __name__ == "__main__":
    main()
