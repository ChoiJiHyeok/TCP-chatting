
# a=[(<socket.socket fd=444, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('10.10.21.104', 9050), raddr=('10.10.21.104', 53880)>, ('10.10.21.104', 53880))]
a=[(0),(1,2)]
b= a.index((1,2))
print(b)