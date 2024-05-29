import sys
import socket
import random

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

        # close the connection after all the information is sent
        client_socket.close()
        
    elif (sys.argv[1] == "-RECIEVE"):
        server_socket = server_setup()
        while (not SENT):
            # establish connection when client connects
            client, address = server_socket.accept()
            print ('established connection from', address )

        # Close the connection when all the required information is sent through the socket
        client.close()

    else:
        print("ERROR, IMPROPER ARGUMENTS!")



    plaintext = "asdjhcakjsncksan" #ideally take information from a file by reading bytes / bits and put it into a string

    AES_KEY = random.getrandbits(16)

    # print(AES_KEY)