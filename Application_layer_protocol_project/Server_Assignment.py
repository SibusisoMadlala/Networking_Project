import socket
import os
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 5007
ADDR = (IP, PORT)
FORMAT = "utf-8"
btarray = bytearray()

def main():

    # checks for the Open and Protected files directories and creates them
    checkDir()
    print("[STARTING] Server is starting.")
    """ Staring a TCP socket. """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """ Bind the IP and PORT to the server. """
    server.bind(ADDR)
    server.listen(10)
    print("[LISTENING] Server is listening.")
    
    while True:

        conn, addr = server.accept()
        t =threading.Thread(target =clients, args =(conn,addr))
        t.start()
    
def clients(conn,addr):
        
        while True:
            print()
            print(f"[NEW CONNECTION] {addr} connected.")

            # recieves message for operation to be completed
            ''' format: METHOD filename filetype PROTECTED KEY '''
            try:
                message = conn.recv(1024).decode()
                conn.send("command recieved".encode())
        
                print("message :"+ message)
                operation = message.split()
                
                print(operation[0])
                #WHEN UPLOADING'''
                if operation[0].upper() == "UPLOAD":
                    
                    recieve(conn, operation) 
                    
                    
                # WHEN DOWNLOADING'''
                elif operation[0].upper() == "DOWNLOAD":
                    try:
                        fil = downloadfile(operation[4],operation[1])
                        try:
                            readfile = open('./Protected_files/'+fil,'rb')
                        except:
                            
                            readfile = open('./Open_files/'+ operation[1], 'rb')
                        s = readfile.read()
                        length = len(s)
                        print("sending size")
                        conn.send(str(length).encode(FORMAT))
                        print("size sent")
                        message = conn.recv(1049).decode()
                        print("response recieved")
                        if message == "recieved":
                            print("sending file")
                            conn.sendall(s) #CLIENT MUST RECIEVE IN A WHILE LOOP
                            print("file sent")    
                    except:
                        print("file not found")
                        conn.send("file not found".encode())

                # checking for available public fiiles        
                elif operation[0].upper() == "LIST_FILES":
                    list_dir(conn)

                else:
                    conn.send("Invalid command".decode())

            except:
                print("")
            
            break


def recieve(conn, filename):
        print('sdsdsds')
    # recieves the message containing file size
        message = conn.recv(1024).decode()
        size =int(str(message).split()[1])

        # sends a response for recieved file size
        conn.send("file size recieved".encode(FORMAT))
        
        # loop to recieve bytes from the client
        data = bytes()
        while int(len(data) <size): #fix this
            mess = conn.recv(4096)
            data +=mess
            
        savefile(data,filename)
        conn.send("File recieved".encode(FORMAT))
        """ Closing the connection from the client. """
        
        print(f"[DISCONNECTED] {ADDR} disconnected.")
        #message = conn.recv(1024)
        conn.close()
        print()

def savefile(file,splt):
    print("in save file")
    open_directry = "./Open_files/"
    protected_directry = "./Protected_files/"
    filename = splt[1]

   # myfile = open("uploaded.txt", "a")
    print(splt[3])
    if splt[3].upper()=='OPEN':
        
        name = splt[1]
        print(name)
        filetpe = os.path.join(open_directry,filename)
        f = open(filetpe,"wb")
        f.write(file)
        #myfile.write(name+"\n")
        f.close()
       # myfile.close()
        
    elif splt[3].upper() == 'PROTECTED':
        
        name=splt[1]+'_'+splt[4]
        
        filetpe = os.path.join(protected_directry,name)
        f = open(filetpe,"wb")
        f.write(file)
        f.close()
    return

def downloadfile(keyy,name): 
    for f in os.listdir("Protected_files"):
        if f.endswith(name+"_"+keyy):
            return f
        
# creates the server files in running directory
def checkDir():
    if os.path.exists("Protected_files") == False:
        parent_dir = "./"
        path = os.path.join(parent_dir, "Protected_files")
        os.mkdir(path)
        path = os.path.join(parent_dir, "Open_files")
        os.mkdir(path)
    else:
        print("dir found")
    # creats the file which will store the names of pblic uploaded files
   # myfile = open("uploaded.txt", "x")
    #myfile.close()

# sends a text file which store the names of uploaded text files
def list_dir(conn):
    res = conn.recv(1049).decode()
    if res == "waiting for text":
        print("sending txt")
        myfile = open("uploaded.txt", "rb")
        myfile = myfile.read()
        if len(myfile) > 0:
            conn.sendall(myfile)
            print("txt sent")
            if (conn.recv(1049).decode() == "recieved"):
                print("Done")
        else:
            conn.send("No files uploaded yet".encode())
            return

if __name__ == "__main__":
    main()