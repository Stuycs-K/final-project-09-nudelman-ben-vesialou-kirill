import numpy as np
import random

SBOX = [
            0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
            0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
            0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
            0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
            0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
            0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
            0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
            0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
            0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
            0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
            0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
            0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
            0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
            0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
            0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
            0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
        ]

rounds = 10
        
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

def xor(first, second):
    first = bytearray(first)
    second = bytearray(second)
    encoded = bytes(a ^ b for a,b in zip(first, second))
    return encoded

# testMatrix = [[0,1,2,3],[0,1,2,3],[0,1,2,3],[0,1,2,3]]

def rowShift(matrix):
    matrix = np.array(matrix, dtype=np.uint8)
    index = 1
    while index < 4:
        matrix[index] = np.roll(matrix[index], -index) #roll shifts over the last n elements to the front
        index += 1
    return matrix

# print(rowShift(testMatrix))

def mixColumns(matrix):
    matrix = np.array(matrix, dtype=np.uint8)
    operationMatrix = np.array([[0x02, 0x03, 0x01, 0x01], [0x01, 0x02, 0x03, 0x01], [0x01, 0x01, 0x02, 0x03], [0x03, 0x01, 0x01, 0x02]], dtype=np.uint8)
    output = np.zeros((4, 4), dtype=np.uint8)

    for i in range(4):
        for j in range(4):
            output[i][j] = (galoismul(operationMatrix[i][0], matrix[0][j]) ^
                            galoismul(operationMatrix[i][1], matrix[1][j]) ^
                            galoismul(operationMatrix[i][2], matrix[2][j]) ^
                            galoismul(operationMatrix[i][3], matrix[3][j]))
    return output

def galoismul(first, second):
    out = 0  
    for i in range(8):  
        if second & 1:  
            out ^= first  
        high = first & 0x80 
        first <<= 1  
        if high:  
            first ^= 0x1b  #irreducible polynomial
        second >>= 1  
    return out
# print(mixColumns(testMatrix))

# testWords = [0x4D.to_bytes(4, byteorder = "little"), 0x3F.to_bytes(4, byteorder = "little"), 0x03.to_bytes(4, byteorder = "little"), 0x10.to_bytes(4, byteorder = "little")]

def RC(roundNum):
    constant = [0x8d]
    a = 1
    for k in range(1, roundNum + 1):
        a = a << 1 #multiplication by 2 using bit shifting
        if a & 0x100: #checks if a exceeds 8 byte
            a ^= 0x11b #keeps a within the 8 byte length using bit modulus 
        constant.append(a)
    return constant[roundNum]

def g(word, roundNum):

    # step 1
    # print(word)
    # print(word[1:])
    # print(word[0: 1])
    word = word[1:] + word[:1]
    # print(word)
    
    # step 2
        # print(newBytes)
    # print(newBytes)
    newbytes = bytearray([SBOX[b] for b in word])
    # step 3
    roundConst = RC(roundNum).to_bytes(1, byteorder="little") + b'\x00\x00\x00'
    # print(roundConst)
    final = bytearray(a ^ b for a, b in zip(word, roundConst)) #the xor function but with byte array instead of bytes

    return final


def keyExpansion(words, roundNumber):
    # print(words)
    w1 = xor(words[0], g(words[3], roundNumber))
    w2 = xor(w1, words[1])
    w3 = xor(w2, words[2])
    w4 = xor(w3, words[3])
    newKey = b''
    newKey += w1 + w2 + w3 + w4
    
    return newKey

# print(keyExpansion(testWords, 1))
def toMatrix(string):
    arr = [int.from_bytes(string[i:i+1], byteorder='little') for i in range(len(string))]
    matrix = np.array(arr, dtype=np.uint8).reshape((4, 4)).T
    # print(matrix)
    return matrix

def bytesubstitution(state):
    newbytes = b''
    for i, k in enumerate(state):
        newbytes += SBOX[k].to_bytes(1, byteorder = "little")
    return state

def key_to_words(key):
    word_arr = []
    for i in range(4):
        word_arr.append(key[4*i : 4*(i+1)])
    return word_arr

def encode(filename, key):
    blocks = split_file(filename)
    key = key.to_bytes(16, byteorder = "little")
    encoded = b''
    
    for i in range(len(blocks)):
        lastkey = key
        laststate = blocks[i]
        for i in range(rounds):
            after_key = xor(laststate, lastkey)
            aftersub = bytesubstitution(after_key)
            state = toMatrix(aftersub)
            afterrows = rowShift(state)
            aftercols = mixColumns(afterrows)
            round_key = keyExpansion(key_to_words(lastkey), i)
            lastkey = round_key
            newstate = xor(aftercols, round_key) 
            laststate = newstate
        encoded += laststate
    return encoded

# inp = str.encode('thisissixteencha')
# print(inp)
# AES_KEY = random.getrandbits(128).to_bytes(16, byteorder = "little")
# # print(AES_KEY)
# round_key = xor(inp, AES_KEY)
# aftersub = bytesubstitution(round_key)
# state = toMatrix(aftersub)
# # print(state[0][0])
# print(state)
# print(round_key)
# nextkey = key_to_words(round_key)
# print(nextkey[0])
# g(nextkey[0])



