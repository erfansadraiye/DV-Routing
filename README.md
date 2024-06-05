# Practical Homework of Computer Networks Course
We implemented a simple router with Distance Vector Routing Algorithm. We used Python for the implementation

We assumed that subnets doesn't overlap and the router has a unique IP address for each link.

The program reads the commands from the standard input line by line and executes the commands. The router should print the output of the commands to the standard output.

## How to Run - Commands

1. add a link to the router.  
```
add link <id> <neighbor-ip-address>/<subnet-mask-bits-number> <distance-estimate>
```
Example:  
```
add link 2 1.2.3.4/24 12
```

2. delete a link from the router.  
```
delete link <id>
```
Example:  
```
delete link 2
```

3. update the distance estimate of a link when a new distance estimate is received.  
```
update <link-id> <distance-vector-length>
```
and then in the next `distance-vector-length` lines, the distance vector is given this format:  
```
<ip-address>/<subnet-mask-bits-number> <distance-estimate>
```

Example:  
```
update 2 3
1.2.4.1/24 30
1.2.5.1/24 32
1.3.8.1/16 45
```

4. print the routing table of the router.  
```
print
```
The router should print all their distance vectors in the following format with order of the ip addresses:

```
<ip-address>/<subnet-mask-bits-number> <distance-estimate> 
```

Example:  
```
1.1.1.1/24 3
1.1.2.1/24 7
1.1.11.3/24 5
1.1.20.4/28 28
1.2.0.0/16 18
```

5. route a packet to a destination IP address.  
```
route <destination-ip-address>
```

and the router should print the link id of the next hop to the destination.
```
<link-id>
```

6. exit the router.  
```
exit
```


## Test Cases

### Test Case 1

Input:
```
add link 1 192.168.1.0/24 5
add link 2 192.168.2.0/24 10
print
route 192.168.1.15
route 192.168.2.20
remove link 1
print
route 192.168.1.15
exit
```

Output:
```
192.168.1.0/24 5
192.168.2.0/24 10
1
2
192.168.2.0/24 10
No route found
```

### Test Case 2
Input:
```
add link 1 192.168.1.0/24 5
add link 2 192.168.3.0/24 15
update 2 2
192.168.4.0/24 7
192.168.5.0/24 10
print
route 192.168.4.25
route 192.168.5.30
exit
```

Output:
```
192.168.1.0/24 5
192.168.3.0/24 15
192.168.4.0/24 22
192.168.5.0/24 25
2
2
```

### Test Case 3

Input:
```
add link 1 192.168.1.0/24 50
add link 2 192.168.3.0/24 15
update 2 2
192.168.1.0/24 7
192.168.5.0/24 10
print
route 192.168.1.25
route 192.168.5.30
remove link 2
print
route 192.168.1.25
exit
```

Output:
```
192.168.1.0/24 22
192.168.3.0/24 15
192.168.5.0/24 25
2
2
192.168.1.0/24 50
1
```