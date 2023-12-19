import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host = socket.gethostname()
print ("got host name:", host)

port = 8888
print("connecting on port:", port)



# example sends "ACK" once
msg1 = "ACK"
time.sleep(1)
s.sendto(msg1.encode(), (host, port))