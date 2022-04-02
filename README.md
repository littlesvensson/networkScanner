# Network Scanner

Network scanner takes care of repetitive network scans of defined IP address or network. Choice of port range is included. Program can compare scans with the previous one.

## How to use

Scanning ports on a single host/defined network:

```
$ ./scanner.py -i <ipaddress/network>
```
Scanning defined ports:

```
$ ./scanner.py -i <ipaddress/network> -s <starting port number> -e <ending port number>
```

The host/network parameter is required in order to run the scan.