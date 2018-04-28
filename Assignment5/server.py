import socket
import ssl

bindsocket = socket.socket()
bindsocket.bind((socket.gethostname(), 10023))
bindsocket.listen(5)
print("Server is running!")

while True:
    newsocket, fromaddr = bindsocket.accept()
    print("Got a connection from! %s" % str(fromaddr))
    connstream = ssl.wrap_socket(newsocket,
                                 server_side=True,
                                 certfile="server.cert",
                                 keyfile="server.pkey",
                                 ssl_version=ssl.PROTOCOL_TLSv1)
    numbers = connstream.recv(1024).decode('ascii').split()
    print("Received numbers: ", numbers)
    numbers = [int(x) for x in numbers]
    sum = numbers[0] + numbers[1]
    print("Sending sum %s" % sum)
    connstream.send(str(sum).encode('ascii'))
    # finished with client
    connstream.close()
