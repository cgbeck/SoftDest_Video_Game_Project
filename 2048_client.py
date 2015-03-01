
import CN_Sockets # CN_Sockets adds ability to interrupt "while True" loop with ctl-C

class UDP_echoclient(object):
    """ Computer Networks Lab 4: Introduction to Sockets.  UDP Transmit example.
This code only transmits a udp message to a known IP_address ("127.0.0.1") and port_number (5280)
The UDP_RX module recieves and prints messages it is sent.
In this example, the UDP_TX process is the client, because the port number of the server (5280) is known to it.
The server, runing UDP_RX, determines the client's port number from each message it receives.
"""
    
    
    def __init__(self,Server_Address=("127.0.0.1",5281)):   # create a socket instance.
                                                            # the "address" is IPv4 address ("127.0.0.1") and port number (5280)
                                                            # "127.0.0.1" is a special IPv4 address indicating that the socket will be communicating
                                                            # over a simulated layer 1 and 2 within a single machine (Laptop or Pi)

        socket, AF_INET, SOCK_DGRAM = CN_Sockets.socket, CN_Sockets.AF_INET, CN_Sockets.SOCK_DGRAM
        # socket = CN_sockets.socket, which is socket.socket with a slignt modification to allow you to use ctl-c to terminate a test safely
        # CN_sockets.AF_INET is the constant 2, indicating that the address is in IPv4 format
        # CN_sockets.SOCK_DGRAM is the constant 2, indicating that the programmer intends to use the Universal Datagram Protocol of the Transport Layer

        with socket(AF_INET,SOCK_DGRAM) as sock:  # open the socket
          
            
            print ("UDP_TX client started for UDP_Server at IP address {} on port {}".format(
                Server_Address[0],Server_Address[1])
                   )

    
            while True:
                
                str_message = input("Enter move:\n")

                if not str_message: # an return with no characters terminates the loop
                    break
                
                bytearray_message = bytearray(str_message,encoding="UTF-8") # note that sockets can only send 8-bit bytes.
                                                                            # Since Python 3 uses the Unicode character set,
                                                                            # we have to specify this to convert the message typed in by the user
                                                                            # (str_message) to 8-bit ascii 

                bytes_sent = sock.sendto(bytearray_message, Server_Address) # this is the command to send the bytes in bytearray to the server at "Server_Address"
                
                print ("{} bytes sent".format(bytes_sent)) #sock_sendto returns number of bytes send.

                # ----------------
                bytearray_msg, source_address = sock.recvfrom(1024) # 1024 is the buffer length
                                                                 # allocated for receiving the
                                                                 # datagram (i.e., the packet)
                                                                 
                source_IP, source_port = source_address    # the source iaddress is ("127.0.0.1",client port number)
                                                           # where client port number is allocated to the TX process
                                                           # by the Linux kernel as part of the TX network stack))
                #Print out the received message/game
                game = bytearray_msg.decode("UTF-8")
                print(game)
                game_data = game.split(' ')
                print(game_data)
                if game_data[0] == "OVER":
                    # OVER 12345
                    print('Game over. Your Score: ', game_data[1])
                    break
                elif game_data[0] == "INVALID":
                    print('Invalid move. Only takes keys: W A S D')
                else:
                    #Else assume have the array of matrix data (strings)
                    # 0 0 2 0 4 4 2 0 4 4 2 0 0 0 2 0 12345
                    gmatrix = [game_data[0:4], game_data[4:8], game_data[8:12],game_data[12:16]]
                    gscore = game_data[16]
                    for i in range(len(gmatrix)):
                        row = ''
                        for j in range(len(gmatrix[i])):
                            adj_len = ((6-len(gmatrix[i][j]))*' ') + gmatrix[i][j]
                            row += adj_len
                        print(row)
                    print('Score: ',gscore)
                    print('')


                #print ("\nMessage received from ip address {}, port {}:".format(
                #    source_IP,source_port))
                #print (bytearray_msg.decode("UTF-8")) # print the message sent by the user of the  UDP_TX module.

        print ("UDP_Client ended")    


if __name__ == "__main__":
    print('enter port number')
    port=input()
    port=int(port)
    Server_Address=("127.0.0.1",port)
    UDP_echoclient(Server_Address)
               
    
                
                
                
            



            
        
