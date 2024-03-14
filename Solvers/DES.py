pc1=[
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
    ]

number_left_shifts = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

pc2=[
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
    ]

def convert_hex2bin(hex):
    hex_bin =[]
    for i in hex:
        binary_number = bin(int(i, 16))[2:].zfill(4)
        #hex_bin.append(binary_number)
        hex_bin += binary_number
    return hex_bin


def permutate_key(key):
    permutated_key = []
    for i in pc1:
        permutated_key += key[i-1]
    return permutated_key

def split_key_toC0D0(key):
    C0 =D0= []
    C0 = key[:28]
    D0 = key[28:]
    return C0 , D0

def shift_the_C0D0(C0,D0):
    C=[]
    D=[]
    C.append(C0)
    D.append(D0)

    for i in number_left_shifts:
        current_C = C[-1]
        current_D = D[-1]
        next_C = current_C[i:]+current_C[:i]
        next_D = current_D[i:]+current_D[:i]
        C.append(next_C)
        D.append(next_D)
    return C , D

def permutate_CD(CD):
    permutated_CD = []
    for i in pc2:
        permutated_CD += CD[i-1]
        #print(permutated_CD)
    return permutated_CD

def make_16_key(C,D):
    K=[]
    for i in range(len(C)-1):
       CD = C[i+1][:] + D[i+1][:] 
       #print(CD)
       temp_k = permutate_CD(CD)
       K.append(temp_k)
    return K

# the above functions are to generate the keys
######################################################################
# the below functions are to manipulate the msg

ip = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
    ]

E = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
    ]

S = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7 ],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8 ],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0 ],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13 ]
    ],
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10 ],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5 ],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15 ],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9 ]
    ],
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8 ],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1 ],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7 ],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12 ]
    ],
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

P = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
    ]

ip_1 = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29 ,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
    ]

def permutate_msg(msg):
    permutated_msg = []
    for i in ip:
        permutated_msg += msg[i-1]
        #print(permutated_msg)
    return permutated_msg

def split_key_toL0R0(key):
    L =R= []
    L = key[:32]
    R = key[32:]
    return L , R

def expand(R):
    expanded_R = []
    for i in E:
        expanded_R += R[i-1]
        #print(expanded_R)
    return expanded_R

def convert_S2bin():
    #print("this is the S",len(S))
    element = 0
    newrow = []
    news = []
    newS = []
    for s in S:
        news = []
        for row in s:
            newrow = []
            for i in row:
                element = bin(i)[2:].zfill(4)
                newrow.append(element)
            news.append(newrow)
        newS.append(news)
    return newS

def S_box():
    pass

def mangular_permutation(R):
    premutated_mangular = []
    for i in P:
        #print(i)
        premutated_mangular += R[i-1]
    #print(premutated_mangular)
    return premutated_mangular

def mangular(R,K,binS):
    XOR_out = []
    R = expand(R) 
    newR =[]
    for i in range(len(R)):
        intR = int(R[i],2)
        intK = int(K[i],2)
        XOR = intR ^ intK
        XOR_out.append(XOR)
    for i in range(8):
        wordOf6 = XOR_out[i*6:(i+1)*6]
        #print(wordOf6)
        rowidx =  wordOf6[0]*2 + wordOf6[-1]
        columnidx=wordOf6[1]*8 + wordOf6[2]*4 + wordOf6[3]*2 + wordOf6[4]
        #print("rowidx",rowidx)
        #print("columnidx",columnidx)
        newR.append(binS[i][rowidx][columnidx])
    #print(newR)
    newerR = []
    for i in newR:
        for j in i:
            newerR.append(j)
    #print(mangular_permutation(newerR))
    return mangular_permutation(newerR)

def premutate_RL(RL):
    premutated_RL = []
    for i in ip_1:
        #print(i)
        premutated_RL += RL[i-1]
    #print(premutated_RL)
    return premutated_RL

def data_encryption(L0,R0,K,binS):
    L = []
    R = []
    L.append(L0)
    R.append(R0)
    for i in range(16):
        Lnew = R[-1]

        #Rnew = L[-1] + mangular(R[-1],K[i],binS)
        Rnew = []
        Ldash = L[-1]
        #print(R[-1])
        Rdash = mangular(R[-1],K[i],binS)
        for i in range (len(Rdash)):
            temp = int(Ldash[i]) ^ int(Rdash[i])
            temp = str(temp)
            Rnew.append(temp)
        #print(Rnew)
        L.append(Lnew)
        R.append(Rnew)
    #print("this is the L16",L[-1])
    #print("this is the R16",R[-1])

    RL = R[-1][:] + L[-1][:]
    #print(RL)

    output = premutate_RL(RL)
    #print(output)
    return output

def convert_data2hex(output_bin):
    output=[]
    #print(output_bin)
    for i in range(16):
        temp = int(output_bin[i*4])*8 + int(output_bin[i*4+1])*4 + int(output_bin[i*4+2])*2 + int(output_bin[i*4+3])
        tempInHex = hex(temp)[2:]
        output+=tempInHex.upper()
    output=''.join(output)
    #rint(output)
    return output

def main(input_tuple):
    try:
        #scan this later
        key = input_tuple[0]  

        #convert it from hexa to binary
        key = convert_hex2bin(key)
        #print(key)

        # permutate the key
        key = permutate_key(key)
        #print(key)

        # extract C0 , D0 from the key
        C0 , D0 = split_key_toC0D0(key)
        #print("C0",C0)
        #print("D0",D0)

        # make the rest of the 16 Cs and Ds
        C , D = shift_the_C0D0(C0,D0)
        #print("the Cs",C)
        #print("the Ds",D)

        #make the 16 keys 
        K = make_16_key(C,D)
        #print(K)
        # the above functions are to generate the keys
        ###############################################################
        # the below functions are to manipulate the msg

        msg = input_tuple[1]
        
        #convert it from hexa to binary
        msg = convert_hex2bin(msg)
        #print(msg)

        # permutate the msg
        msg = permutate_msg(msg) 
        #print(msg)

        # split the msg to L0 , R0
        L0 , R0 = split_key_toL0R0(msg)
        #print("L0",L0)
        #print("R0",R0)

        # convert 
        binS = convert_S2bin()
        #print(binS[0])

        #encrypt the data
        output_bin = data_encryption(L0,R0,K,binS)
        
        output = convert_data2hex(output_bin)
        #print(output)
        return output
    except Exception as e:
        print("Failed to solve DES due to exception:", e)
        return ""
            
            
        

if __name__ == '__main__':
    key = "266200199BBCDFF1"
    msg = "0123456789ABCDEF"
    default =(key,msg)
    main(default)


#reference
#https://www.youtube.com/watch?v=AoLbJKh9X2A
#https://csrc.nist.gov/files/pubs/fips/46-3/final/docs/fips46-3.pdf