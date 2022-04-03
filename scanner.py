#!/usr/bin/python
import ipaddress
import json
import sys
import socket
import argparse
from queue import Queue
from threading import Thread

OUTPUT_FILE = 'scan.json'

class MyThread (Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.daemon = True
        self.pool = tasks
        self.start()

    def run(self):
        while self.pool.not_empty:
            func, args, kwargs = self.pool.get()
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(e)
            finally:
                self.pool.task_done()

class Pool:
    """Pool for Tasks """

    def __init__(self, threads):
        self.tasks = Queue(threads)
        for _ in range(threads):
            MyThread(self.tasks)

    def add_task(self, func, *args, **kwargs):
        """ """
        self.tasks.put((func, args, kwargs))

    def wait(self):
        """ """
        self.tasks.join()

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

def compare_scans(previous_results, host, ports, results):
    new_results = list(results[host]["ports"])

    if previous_results != new_results or (previous_results is None and new_results is None):
        print("-" * 50)
        print("Differences for host {} found!".format(host))
        print("Current output:")
        for ports in results[host]["ports"]:
            print("Ports: {1}/tcp/open".format(host, ports))
        print("Previous output:")
        for ports in previous_results:
            print("Ports: {1}/tcp/open".format(host, ports))
    else:
        print("-" * 50)
        print("Host {}: No difference in open ports found in the current scan".format(host))
        print("Current output:")
        for ports in results[host]["ports"]:
            print("Ports: {1}/tcp/open".format(host, ports))

    # Save results
    with open(OUTPUT_FILE, "w") as file:
        json.dump(results, file)

def scan_host(host, startPort, endPort, results):
    previous_results = list(results[host]["ports"])
    if host not in results:
        results.update({host: {"ports": []}})        
    else:
        results[host]["ports"].clear()

    # Scan ports simultaneously    
    tasks = Pool(1024)
    for port in range(startPort, endPort+1):
        tasks.add_task (scan_port, host, port, results)
    tasks.wait()
    compare_scans(previous_results, host, port, results)     

def main():
    # Define variables
    port_start = 1
    port_end = 150
    results = {}

    # Get params from CLI
    aparse = argparse.ArgumentParser(
        description='Options for creating a network scanner.')
    aparse.add_argument("-s", "--start", type=int,
                        help="Start port, default value 1")
    aparse.add_argument("-e", "--end", type=int,
                        help="End port, default value 1024")
    aparse.add_argument(
        "-i", "--ip", help="IP Address(e.g. 10.1.1.1) or network (e.g. 192.168.1.0/24) to scan ")
    args = aparse.parse_args()

    if args.start is not None:
        port_start = args.start

    if args.end is not None:
        port_end = args.end

    if args.ip is not None:
        try:
            targetIps = ipaddress.ip_network(args.ip).hosts()
        except:
            print("ERROR: Specify a valid IP address or Network to scan!")
            aparse.print_help()
            sys.exit()    

    # Parsing check
    # IP or network required
    if args.ip is None:
        print("ERROR: Specify IP address or Network to scan!")
        aparse.print_help()
        sys.exit()

    # Ports check
    if port_start > port_end:
        print("ERROR: Starting port value has to be lower than ending port value!")
        aparse.print_help()
        sys.exit()

    if port_start not in range(1, 65535) or port_end not in range(1, 65536):
        print("Error: Defined ports are not valid!")
        aparse.print_help()
        sys.exit()

    # Open file with past data if exists
    try:
        with open(OUTPUT_FILE, "r") as file:
            results = json.load(file)
    except IOError:
        pass    

    for ip in targetIps:       
        scan_host(str(ip), port_start, port_end, results)   

if __name__ == "__main__":
    main()
