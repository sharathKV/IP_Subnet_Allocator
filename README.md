# IP_Subnet_Allocator
Problem 4

#IP_Subnet_Allocator
Assigns first available IP subnet based on customer demand. The script uses pandas external library
to maintain the assigned addresses in the backend in an excel spreasheet.
The script asks the user for 3 inputs
- customer name
- desired network range from available options: E.g. 1
- required number of hosts

Example Usage:  

`python ip_subnet_allocator.py`  
```python output
******************************IP Subnet Allocator*******************************  
List of available class B network addresses:  

id         network  avl_address  avl_percent  

1   168.212.0.0/16        65024     99.21875  

2   132.147.0.0/16        65536    100.00000  

3   129.142.0.0/16        65536    100.00000  

Enter customer name: skyworks  

Choose your desired network address range, input 1 or 2 or ..: 1  

Enter the required number of hosts: 12  

Your assigned sub-network: 168.212.0.0/28  
```
