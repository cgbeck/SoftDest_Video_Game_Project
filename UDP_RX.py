import CN_Sockets

import math
import random
points=0

class UDP_RX(object):
    """1. READ the UDP_TX module before reading or using this one.

This module demonstrates receiving a transmission sent by the UDP_TX module
on a SOCK_DGRAM (UDP) socket.  This module must be started first, so that it
can publish its port address (5280).

2. Run this module before starting UDP_TX.

UDP_TX and UDP_RX will be started on separate (laptop OS) processes.
UDP_TX will prompt for a message, then transmit it to the UDP_RX module over the
loopback IP address ("127.0.0.1").

UDP_RX will receive the message and print it.
While waiting for a message UDP_RX to be started or to send another message, UDP_TX will print a line of "."s one every 2 seonds.


 
 

    """

    
    def __init__(self,IP,port):

        socket, AF_INET, SOCK_DGRAM, timeout = CN_Sockets.socket, CN_Sockets.AF_INET, CN_Sockets.SOCK_DGRAM, CN_Sockets.timeout
        #                                      the socket class    the IPv4 address model    The UDP layer 4 protocol    The event name for a socket timout
        
        
        with socket(AF_INET, SOCK_DGRAM) as sock:
            sock.bind((IP,port))  # bind sets up a relationship in the linux
                                  # kernel between the process running
                                  # UCP_RX and the port number (5280 by default)
                                  # 5280 is an arbitrary port number.
                                  # It is possible to register a protocol
                                  # with the IANA.  Such registered ports
                                  # are lower than 5000. e.g. HTTP (
                                  # for browser clients and web servers)
                                  # is registered by IANA as port 80
                                  #
                                  
            sock.settimeout(2.0) # create a 2 second timeout so that we
                                 # can use ctrl-c to stop a blocked server
                                 # if, for example, the client doesn't work.
            
            print ("UDP Server started on IP Address {}, port {}".format(IP,port))
            
            while True:
                try:
                    bytearray_msg, source_address = sock.recvfrom(1024) # 1024 is the buffer length
                                                                 # allocated for receiving the
                                                                 # datagram (i.e., the packet)
                                                                 
                    source_IP, source_port = source_address    # the source iaddress is ("127.0.0.1",client port number)
                                                               # where client port number is allocated to the TX process
                                                               # by the Linux kernel as part of the TX network stack))          
                    
                    print ("\nMessage received from ip address {}, port {}:".format(
                        source_IP,source_port))
                    command=bytearray_msg.decode("UTF-8")
                    print("receiving message:"+bytearray_msg.decode("UTF-8"))
                    if command == 'g':
                      olist = [[0]*4,[0]*4,[0]*4,[0]*4]
                      # olist = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,15]]
                      update = rand_add(olist)
                      olist = update[0]
                      str_message=print_game(olist)
                    else:
                      olist= run_command(olist, command)
                      if olist==0:
                        str_message="INVALID"
                      else: 
                        global points
                        if update[1] == False:
                          # if Game Over
                          points = str(points)
                          str_message="OVER "+points
                          print("***Game Over***")
                          print(str_message)
                          bytearray_message = bytearray(str_message,encoding="UTF-8")  
                          bytes_sent = sock.sendto(bytearray_message, source_address)
                          break
                        update = rand_add(olist)
                        olist = update[0]
                        str_message = print_game(olist)

                    bytearray_message = bytearray(str_message,encoding="UTF-8")  
                    bytes_sent = sock.sendto(bytearray_message, source_address) 


                except timeout: 
                                
                    print (".",end="",flush=True)  # if process times out, just print a "dot" and continue waiting.  The effect is to have the server print  a line of dots
                                                   # so that you can see if it's still working.
                    continue  # go wait again

    
                
                
            



def move(olist, direction):
    # The basic structure in this function is to move all the numbers in the matrix upward.
    # rotate() function helps to transfer other direction request cases into upward moving case.
    if direction == 'up':
        pass
    elif direction == 'down':
        olist = uptodown(olist)
    elif direction == 'right':
        olist = rotate(olist)
    elif direction == 'left':
        olist = rotate(olist)
        olist = rotate(olist)
        olist = rotate(olist)
    global points
    # The above code using rotate function to transfer the matrix into upward cases
    # global points
    for j in range(4):
        mlist=olist[j]
        nlist=clean(mlist)
        i=0
        for i in range(len(nlist)-1):
            if nlist[i]==nlist[i+1]:
                nlist[i]+=nlist[i+1]
                points += int(nlist[i])
                nlist[i+1]=0
            #print(points)
        # print ("Points:", str(points))
        nlist=clean(nlist)
        #check if every two cells have the same number. if so, adding them up.
        x=0
        for x in range(4-len(nlist)):
            nlist.append(0)
            #fullfill the rest of the space in the matrix by 0s.
        olist[j]=nlist
    if direction == 'down':
        olist = uptodown(olist)
    elif direction == 'right':
        olist = rotate(olist)
        olist = rotate(olist)
        olist = rotate(olist)
    elif direction == 'left':
        olist = rotate(olist)
    #The above code using rotate function to transfer other direction request cases back
    return olist

def clean(mlist):
    # This function erase all the 0s in the matrix and only leave "real" numbers there.
    nlist = []
    for item in mlist:
        if item != 0:
            nlist.append(item)
    return nlist

def uptodown(qlist):
    #This function flip the matrix upside down
    newlist=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for i in range(len(qlist)):
        for j in range(len(qlist[i])):
            newlist[i][len(qlist)-j-1]=qlist[i][j]
    return newlist

def rotate(qlist):
    #This function  rotates the matrix in 90 degree everytime when being called.
    newlist=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for i in range(len(qlist)):
        for j in range(len(qlist[i])):
            newlist[j][len(qlist)-i-1]=qlist[i][j]
    return newlist

def print_game(glist):
    #Prints the given list
    # for i in range(len(glist)):
    # print(glist[0][i],'\t',glist[1][i],'\t',glist[2][i],'\t',glist[3][i])
    message=""
    for i in range(len(glist)):
      message+=(str(glist[0][i])+" "+str(glist[1][i])+" "+str(glist[2][i])+" "+str(glist[3][i]) + " ")
      print (glist[0][i],'\t',glist[1][i],'\t',glist[2][i],'\t',glist[3][i])
    global points
    print("")
    print('Points:',points)
    points_str=str(points)
    print("")
    return message+points_str


def check_if_doubles(olist):
    #Goes through a list and checks if there is still a move left
    still_move = False
    for i in range(len(olist)):
        for j in range(1,len(olist[i])):
            if olist[i][j] == olist[i][j-1]:
                still_move = True
    #Checks columns
    templist = rotate(olist)
    for i in range(len(templist)):
        for j in range(1,len(templist[i])):
            if templist[i][j] == templist[i][j-1]:
                still_move = True
    
    return still_move


def rand_add(glist):
    #Randomly replaces a 0 with a 2 in a list
    possible_i = []
    for i in range(len(glist)):
        for j in range(len(glist[i])):
            #For each row and each column
            if glist[i][j] == 0:
                #If the space has a zero save te index
                possible_i.append((i,j))
    if len(possible_i) > 0:
        #Get random index of possible zeroes IF there are zeroes
        index = possible_i[math.floor(random.random()*len(possible_i))]
        glist[index[0]][index[1]] = 2   #Add in the next
        return glist, True
    else:
        #If no zeroes to add, see if can still make a move
        still_move = check_if_doubles(glist)
        if still_move:
            return glist, True
        else:
            return glist, False

def run_command(olist, comi):
    #Basic run function of user input
    if comi == 'w':
        olist=move(olist,'up')
    elif comi == 'a':
        olist=move(olist,'left')
    elif comi == 's':
        olist=move(olist,'down')
    elif comi == 'd':
        olist=move(olist,'right')
    else:
        #If did not enter valid key, notify user and ask for input again
        return 0
    return olist



            

if __name__ == "__main__":
    print('enter port number')
    port=input()
    port=int(port)
    UDP_RX("127.0.0.1",port)
