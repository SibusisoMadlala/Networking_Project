import socket
import sys

IP = socket.gethostbyname(socket.gethostname())
PORT = 5007
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = bytes(28936)

def main():
    """ Staring a TCP socket. """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """ Connecting to the server. """
    client.connect(ADDR)

    """ Sending the filename to the server. """
    
    protocol = sys.argv[1].upper()+' '+sys.argv[2]+' '+sys.argv[3]+' '+sys.argv[4].upper()+' '+sys.argv[5]
    print(protocol)
    
    fileNamelist = sys.argv[2].split('/')
    
    filename = fileNamelist[len(fileNamelist)-1]
    if sys.argv[1].upper() == 'DOWNLOAD':
        
        
        ''' sending request line '''
        client.send(protocol.encode(FORMAT))
        client.recv(1024).decode(FORMAT)
        
        ''' recieving size of file '''
        sizeoffile = client.recv(1024).decode(FORMAT)
        client.send("recieved".encode(FORMAT))
        
        '''  recieving bytes'''
        data = bytes()
        while int(len(data)) < int(sizeoffile):
            mess = client.recv(4096)
            data+=mess
            
        ''' writing bytes to file '''
        recvedfile = open(sys.argv[2],'wb')
        recvedfile.write(data)
      
   
    elif sys.argv[1].upper() == 'UPLOAD':
        
        protocol = sys.argv[1].upper()+' '+filename+' '+sys.argv[3]+' '+sys.argv[4].upper()+' '+sys.argv[5]
        client.send(protocol.encode(FORMAT))
        client.recv(1024).decode(FORMAT)
        
        ''' sending size of file '''
        file = open(str(sys.argv[2]),'rb')
        r = file.read()
        length = len(r)
        client.send(("size: "+str(length)).encode(FORMAT))
        
        ''' confirmation that size recieved '''
        client.recv(1024).decode(FORMAT)
        
        '''sending file'''
        client.sendall(r)
        file.close()
        
        ''' confirmation that file recved'''
        client.recv(1024).decode(FORMAT)    
    
    """ Closing the connection from the server. """
    client.close()


if __name__ == "__main__":
    main()