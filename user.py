import sys
import socket
import random
from aes import *

port = 23445

#intialize a variable to keep track of whether all the file's information is sent yet
# SENT = False

def server_setup():
    # create a socket
    s = socket.socket()
    print ("Socket created")

    # bind to the port
    s.bind(('', port))
    print ("binded to port %s" %(port))

    # set socket to listening mode
    s.listen(5) 
    print ("socket is listening")

    return s

def client_setup(IP):
    #create a socket
    s = socket.socket()
    print ("Socket created")

    s.connect((IP, port))
    print ("connected to %s" %(IP))

    return s

if __name__ == "__main__":
    #user input will be in one the following forms:
        #python3 user.py -SEND FILENAME IP
        #python3 user.py -RECIEVE
        #the port for the user will be in the program

    if (sys.argv[1] == "-SEND"):
        file_path = sys.argv[2]
        server_ip = sys.argv[3]

        client_socket = client_setup(server_ip)
        
        #now the client has to recieve information
        #send some information here
        
        AES_KEY = random.getrandbits(128) #ideally it would not be random

        encoded_text = encode(file_path, AES_KEY)
        # plaintext = "asdjhcakjsncksan" #ideally take information from a file by reading bytes / bits and put it into a string
        client_socket.send(len(encoded_text).to_bytes(4, byteorder = "little"))
        client_socket.send(encoded_text)
        # for i in range(len(encoded_text) // 16):
        #     client_socket.send(encoded_text[16*i: 16 * (i + 1)])

        # client_socket.send(b'0' * 16)

        server_response = client_socket.recv(128)
        # encoded_arr = encode(plaintext, AES_KEY)

        # print(AES_KEY)

        # close the connection after all the information is sent
        # SENT = True
        if(server_response == b'END_RECIEVE'):
            client_socket.close()
        else:
            print("error in server response:", server_response)
            client_socket.close()
        
    elif (sys.argv[1] == "-RECIEVE"):
        server_socket = server_setup()
        # recieved = b'a' * 16
        # zeroes = b'0' * 16
        # final = b''

        client, address = server_socket.accept()
        print ('established connection from', address )

        leninbytes = b''
        while len(leninbytes) < 4:
            received = client.recv(4 - len(leninbytes))
            if not received:
                raise RuntimeError("broken sockets")
            leninbytes += received

        length = int.from_bytes(leninbytes, byteorder="little")
        print("Length:", length)

        # Receive the encoded text
        received_data = b''
        while len(received_data) < length:
            data = client.recv(length - len(received_data))
            if not data:
                raise RuntimeError("Socket connection broken")
            received_data += data
        
        print("RECIEVED DATA: ", received_data)
        # while (recieved != (zeroes)):
        #     recieved = server_socket.recv(16)
        #     # establish connection when client connects
        #     final += recieved
        #     if recieved == zeroes:
        #         break

        # Close the connection when all the required information is sent through the socket
        client.send(b'END_RECIEVE')
        client.close()
        server_socket.close()

    else:
        print("ERROR, IMPROPER ARGUMENTS!")
