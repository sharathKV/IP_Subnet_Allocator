# Get_remote_Interface_Details
Extract IP, MAC, Interface types of available interfaces on a remote machine  

Example Usage:  

`python interface_details.py svkumar2, 1.2.3.4, password123`  

Available interfaces on the machine:  

0) lo  
1) eth0  
2) eth1  
Enter the interface name to get the corresponding details / type 'all' for all interfaces: all  
```json output
{
    "lo": {
        "ip-address": "127.0.0.1",
        "mac-address": "00:00:00:00:00:00",
        "interface-type": "link/loopback"
    },
    "eth0": {
        "ip-address": "10.25.11.111",
        "mac-address": "00:50:56:06:5e:14",
        "interface-type": "link/ether"
    },
    "eth1": {
        "ip-address": "152.7.176.80",
        "mac-address": "00:50:56:06:5e:15",
        "interface-type": "link/ether"
    }
}  
```
