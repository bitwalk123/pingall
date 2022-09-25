from ipaddress import IPv4Network, ip_address

for addr in IPv4Network('192.168.150.0/24'):
    print(addr)
    print(ip_address(addr))