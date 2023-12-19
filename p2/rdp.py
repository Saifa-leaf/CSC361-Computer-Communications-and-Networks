import select
import socket
import string
import sys
import queue
import time
import re

def main():
    server_address = (sys.argv[1], int(sys.argv[2]))       
    # Create a TCP/IP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set the socket to non-blocking mode
    server.setblocking(0)
    # bind address, server_address is defined by the input
    server.bind(server_address)
    # Listen for incoming connections.str()
    server.listen(5)

    # Sockets to watch for readability
    inputs = [server]
    # Sockets to watch for writability
    outputs = []


#     Initialization:
        # ○ Import packages such as socket, sys
        # ○ Initialize a UDP socket: udp_sock
        # ○ Initialize a sending buffer: snd_buf
        # ○ Initialize a receiving buffer: rcv_buf
        # ○ Initialize two classes: rdp_sender, rdp_receive

class rdp_sender:
    __state = "closed" # closed -> syn-sent -> open -> "FIN" -> closed

    def __send(self): # Private
        if self.__state == "syn-sent":
            # Write SYN rdp packet into snd_buf
        if self.__state == "open":
            # Write the available window of DAT rdp packets into snd_buf
            if all data has been sent:
                # call self.close()
        if self.__state == "FIN":
            # Write FIN rdp packet into send_buf

    def open(self):
        # Write SYN rdp packet into snd_buf
        self.__state = "syn-sent"

    def rcv_ack(self):
        if self.__state == "syn-sent":
            if ack_num is correct:
                # self.__state = "open"
        if self.__state == "open":
            if three duplicate received:
                # Resend packets
            if ack_num is correct:
                # Move the sliding window, and call 
                # self.__send()
        if self.__state == "FIN":
            if ack_num is correct:
                self.__state = "close"

    def timeout(self):
        if self.__state != "close":
            # Rewrite the rdp into buffer

    def close(self):
        # Write FIN packet to snd_buf
        self.__state = "FIN"




    

if __name__ == "__main__":
    main()
