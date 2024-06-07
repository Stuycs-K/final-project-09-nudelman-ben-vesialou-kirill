import sys
import socket
import random
import aes

port = 23451

#intialize a variable to keep track of whether all the file's information is sent yet
SENT = False

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

        encoded_text = encode(filename, AES_KEY)
        # plaintext = "asdjhcakjsncksan" #ideally take information from a file by reading bytes / bits and put it into a string

        for i in range(len(encoded_text) / 16):
            client_socket.send(encoded_text[16*i: 16 * (i + 1)])

        client_socket.send(b'0' * 16)

        # encoded_arr = encode(plaintext, AES_KEY)

        # print(AES_KEY)

        # close the connection after all the information is sent
        # SENT = True
        client_socket.close()
        
    elif (sys.argv[1] == "-RECIEVE"):
        server_socket = server_setup()
        recieved = b'a' * 16
        zeroes = b'0' * 16
        final = b''

        client, address = server_socket.accept()
        print ('established connection from', address )
        while (recieved != (zeroes)):
            # establish connection when client connects
            final += server_socket.recv(16)

        # Close the connection when all the required information is sent through the socket
        client.close()

    else:
        print("ERROR, IMPROPER ARGUMENTS!")
