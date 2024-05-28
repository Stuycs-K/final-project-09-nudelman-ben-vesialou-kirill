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

if __name__ == "__main__":
    #user input will be in one the following forms:
        #python3 user.py -SEND FILENAME IP
        #python3 user.py -RECIEVE
        #the port for the user will be in the program

    if (sys.argv[1] == "-SEND"):
        file_path = sys.argv[2]
        server_ip = sys.argv[3]
        
    else if (sys.argv[1] == "-RECIEVE"):
        while !(SENT):
            socket = server_setup()

            # establish connection when client connects
            client, address = s.accept()
            print ('established connection from', address )

        # Close the connection
        client.close()

    else:
        print("ERROR, IMPROPER ARGUMENTS!")



    plaintext = "asdjhcakjsncksan" #ideally take information from a file by reading bytes / bits and put it into a string

    AES_KEY = random.getrandbits(16)

    # print(AES_KEY)