# Splits the file into blocks with 128 bits. Pads the file with 0s if it the number of bytes isn't a multipl of 16.
def split_file(file):
    blocks =[]
    with open(file, 'rb') as f:
        data = f.read()

    # Pads the file contents with 0s so that it can be split up into 16 byte sections
    numOfPaddingBytes = 16 - (len(data) % 16)
    for i in range (numOfPaddingBytes):
        data += b'\x00'

    # Splits the data into 16 byte sections and appends them to blocks
    i = 0
    while(i < len(data)):
        blocks.append(data[i:i + 16])
        i += 16
    
    return blocks
