import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)
res = s.connect_ex(('127.0.0.1', 8787))
print("Port 8787 open:", res == 0)
s.close()
