import select
import socket
import string
import sys
import queue
import time
import re

def main():
    check = 0
    conAlive = {}
    listOfMessage = False
    Sendback = 0

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
    # Outgoing message queues (socket:Queue)
    response_messages = {}
    # request message
    request_message = {}

    while True:
            # Wait for at least one of the sockets to be ready for processing
            # timeout as 4th arg if it is block forever
            try:
                readable, writable, exceptional = select.select(inputs, outputs, inputs, 60)
                if len(readable) == 0 and len(writable) == 0 and len(exceptional) == 0:
                    if (client_socket is not server):
                        inputs = [server]
                        exceptional.append(client_socket)   
            except ValueError:
                break
            for s in readable:
                if s is server:
                # , accept new connection, and append new connection socket to
                # the list to watch for readability
                    client_socket, client_address = s.accept()
                    client_socket.setblocking(0)
                    inputs.append(client_socket)
                    response_messages[client_socket] = queue.Queue()
                    request_message[client_socket] = []
                else:
                    #Receive message from the receiving buffer
                    message = s.recv(1024).decode()
                    conAlive[s] = 0
                    if ("\n\n" in message and message != "\n\n"):
                        listOfMessage = True
                        Multimessage = message.split("\n")
                        for eachLine in Multimessage:
                            request_message[client_socket].append(eachLine)

                            if (len(request_message[client_socket][0].split(" ")) != 3 or "GET" not in request_message[client_socket][0] or "HTTP/1.0" not in request_message[client_socket][0]):
                                # print('bad request')
                                response_messages[s].put("HTTP/1.0 400 Bad Request\r\n")
                                response_messages[s].put("Connection: close\r\n\r\n")
                                outputs.append(s) 

                            print(request_message[client_socket])
                            if ("\r\n\r\n" in request_message[client_socket] or "\n\n" in request_message[client_socket] or "\n" in request_message[client_socket] \
                                or "" in request_message[client_socket]):
                                whole_message = request_message[client_socket]
                                #add connection socket s to the list for writable, as we will send back messages
                                outputs.append(s)
                                for line in whole_message:
                                    print(line)
                                    newLine = line.split()
                                    try:
                                        if (len(newLine) == 3 and "GET" == newLine[0] and "HTTP/1.0" == newLine[2]):
                                            f = open(newLine[1].replace("/", ""), "r")
                                            response_messages[s].put("HTTP/1.0 200 OK\r\n")
                                            check = 1
                                            print(check)
                                            # response_messages[s].put(f.read())
                                    except (FileNotFoundError):
                                        response_messages[s].put("HTTP/1.0 404 Not Found\r\n")
                                    else:
                                        if ("connection" in line.lower() and "keep-alive" in line.lower()):
                                            response_messages[s].put("Connection: keep-alive\r\n\r\n")
                                            conAlive[s] = 1
                                        else:
                                            conAlive[s] = 0

                                for readFile in whole_message:
                                    splitReadFile = readFile.split()
                                    if(check == 1 and len(splitReadFile) == 3 and "get" in readFile.lower()):
                                        try:
                                            print("should work")
                                            f = open(splitReadFile[1].replace("/", ""), "r")
                                            response_messages[s].put(f.read())
                                            f.close()
                                            check = 0
                                        except (FileNotFoundError):
                                            None



                    if message and not listOfMessage and (message != "\n" or not len(request_message[client_socket]) == 0):
                        #If message is not empty, we add the message to the queue for further process if format is correct
                        if(len(message) != 1):
                            request_message[client_socket].append(message.strip())
                        else:
                            request_message[client_socket].append(message)

                        if (len(request_message[client_socket][0].split(" ")) != 3 or "GET" not in request_message[client_socket][0] or "HTTP/1.0" not in request_message[client_socket][0]):
                            response_messages[s].put("HTTP/1.0 400 Bad Request\r\n")
                            response_messages[s].put("Connection: close\r\n\r\n")
                            outputs.append(s)

                        if ("\r\n\r\n" in request_message[client_socket] or "\n\n" in request_message[client_socket] or "\n" in request_message[client_socket]):
                            whole_message = request_message[client_socket]
                            #add connection socket s to the list for writable, as we will send back messages
                            outputs.append(s)
                            for line in whole_message:
                                newLine = line.split()
                                try:
                                    if (len(newLine) == 3 and "GET" == newLine[0] and "HTTP/1.0" == newLine[2]):
                                        f = open(newLine[1].replace("/", ""), "r")
                                        response_messages[s].put("HTTP/1.0 200 OK\r\n")
                                        check = 1
                                        # response_messages[s].put(f.read())
                                except (FileNotFoundError):
                                    response_messages[s].put("HTTP/1.0 404 Not Found\r\n")
                                else:
                                    if ("connection" in line.lower() and "keep-alive" in line.lower()):
                                        response_messages[s].put("Connection: keep-alive\r\n\r\n")
                                        conAlive[s] = 1

                                # if "GET" not in whole_message or "HTTP/1.0"  not in whole_message:
                                #     print('bad request')
                                #     print(line)
                                    # response_messages.append(“HTTP/1.0 400 Bad Request”)
                                #else:
                                    #Add response messages accordingly
                            for readFile in whole_message:
                                splitReadFile = readFile.split()
                                if(check == 1 and len(splitReadFile) == 3 and "get" in readFile.lower()):
                                    f = open(splitReadFile[1].replace("/", ""), "r")
                                    response_messages[s].put(f.read())
                                    f.close()
                                    check = 0

            
            for s in outputs :
                #get messages from response_message{s}
                if (Sendback != 1):
                    toSendBack = response_messages[s].queue[0]
                    Sendback = 1

                try:
                    next_msg = response_messages[s].get_nowait()
                except queue.Empty:
                    #check if timeout or connection is persistent or not, and close socket accordingly
                    time1 = time.strftime("%a %b %d %X PDT %Y: ", time.localtime())
                    print(time1 + sys.argv[1] + ":" + sys.argv[2] + " " + request_message[s][0] + "; " + str(toSendBack), end = '') 
                    Sendback = 0
                    if conAlive[s] != 1:
                        outputs.remove(s)
                        inputs.remove(s)
                        s.close()
                    else:
                        outputs.remove(s)
                        conAlive[s] = 0
                        response_messages[s] = queue.Queue()
                        request_message[s] = []
                else:
                    #send messages and print logs if finish responding to a request
                    s.send(next_msg.encode())

            for s in exceptional:
            # Stop listening for input on the connection inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                s.close()
                # Remove message queue
                # del response_messages[s]
                response_messages[s] = queue.Queue()
                request_message[s] = []




if __name__ == "__main__":
    main()
