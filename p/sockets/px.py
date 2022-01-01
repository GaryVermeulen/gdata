import ipaddress

ip10 = ipaddress.ip_address('10.0.0.10')
ip10type = type(ip10)


print("type: " + str(ip10type))
print("ip10: " + str(ip10))
print("ipv : " + str(ip10.version))

for i in range(6):
    print("ip: " + str(i) + " : " + str(ipaddress.ip_address(i)))
    
    
ipnet = ipaddress.ip_network('10.0.0.0/28') # Don't use host bits!

print(ipnet)
print("range: " + str(ipnet.num_addresses))

for x in ipnet.hosts():
    print("usable: " + str(x))

for ips in ipnet:
    print(ips)
    
        
ipi = ipaddress.ip_interface('10.0.0.1/24')

print("ipi: " + str(ipi))
print("host: " + str(ipi.network))



