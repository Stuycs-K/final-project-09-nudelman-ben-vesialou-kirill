# Work Log

## Benjamin Nudelman

### 05/23

Completed initialization of variables for aes encryption and began to write helper functions such as xor.

### 5/24 and weekend

Mostly researched the specific functions of each round of AES as well as the implementation of the network layer in python. Began putting it into code.

### 5/28

Completed client and server setup of the network connections, tested and debugged the functions.

### 5/29 

Fixed xor function and added function to convert byte string into matrix for further use.

### 5/30

Added round key and byte substitution steps of one round of AES.

### 5/31 and Weekend

Added more testing for byte substitution and revised byte substitution to work with matrices and bytes. Researched final step of each round of AES.

### 6/3

Created two functions for splitting up the AES functions per round and for the general encoding process and keeping track of the round keys. Yet to complete it.

### 6/4 and 6/5

Changed the structure of the encoding functions to make them one larger and more understandable function. Completed it, yet to complete testing. Took file name as input, converted it to array of 16 byte blocks and encrypted each block through ten rounds, appending it back to a large byte string after and returning it.

### 6/7

Updated networking portion of the code so that the user inputs a filename and the properly encoded information is sent through the network.

### 6/8 and 6/9

Fixed many of the functions to properly store bytes and byte arrays instead of ints, and fixed the broken socket issue in the networking.

## Kirill Vesialou

### 05/23

Researched the AES algorithm and found a source that could be used in order to understand each step of AES (https://engineering.purdue.edu/kak/compsec/NewLectures/Lecture8.pdf).

### 5/24 and weekend

Read up to page 27 of the source that I found.

### 5/28

Wrote code meant to split up files into chunks of data (128 bits long).

### 5/29 

Read up to page 37 of the source that I found.

### 5/30

Read up to page 46 of the source that I found.

### 5/31 and Weekend

Wrote the functions for row shift and mix columns.

### 6/3

Worked on the key expansion function.

### 6/4 and 6/5

Worked on the key expansion function, and the g function that is used in the key expansion function.

### 6/7

Finished debugging the g function.
