import socket

from ping3 import ping

host = socket.gethostname()
print(host)
ip = socket.gethostbyname(host)
print(ip)

print(ping('192.168.150.2', timeout=0.5))
