# Network Scanner

Network scanner takes care of repetitive network scans of defined IP address or network. Choice of port range is included. Program can compare scans with the previous one.

## How to use

Scanning ports on a single host/defined network:

```
$ python ./scanner.py -i <ipaddress/network>
```
Scanning defined ports:

```
$ python ./scanner.py -i <ipaddress/network> -s <starting port number> -e <ending port number>
```

The host/network parameter is required in order to run the scan.

### Applying manifest

Apply the manifest by running:
```
$ kubectl apply -f cj.yaml
```

Now the program will be run every 5 minutes. You can check it with the following command:
```
$ kubectl get cj
```

The IP address or network can be configured in the cj.yaml file.
