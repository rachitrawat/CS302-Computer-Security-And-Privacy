import socket, ssl, pprint

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# require a certificate from the server
ssl_sock = ssl.wrap_socket(s,
                           ca_certs="CA.cert",
                           cert_reqs=ssl.CERT_REQUIRED)

ssl_sock.connect((socket.gethostname(), 10023))

print(repr(ssl_sock.getpeername()))
# pprint.pprint(ssl_sock.getpeercert())
print(pprint.pformat(ssl_sock.getpeercert()))

# send numbers to add
ssl_sock.send(("15 20").encode('ascii'))

# get sum
print("Received sum:", ssl_sock.recv(1024).decode('ascii'))

# close socket
print("Closing socket!")
ssl_sock.close()
