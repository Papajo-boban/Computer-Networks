import socket
import threading

so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host_port = ("143.47.184.219", 5378)
so.connect(host_port)

encoder = "utf-8"
bytes = 1024

def receive_messages(so):
    while True:
        threadResp = ""
        while True:
            data = so.recv(1024).decode()            
            if "\n" not in data:
                threadResp += data
                continue
            else:
                break
        
        if data.startswith("DELIVERY"):
            sender, message = data.split(maxsplit=2)[1:]
            print(f"Received message from {sender}: {message}")
        
            
myThread = threading.Thread(target=receive_messages, args=(so,))
myThread.setDaemon(True)

while True:
   
    userInpt = input("Provide input..." + "\n")
    inpt = ("HELLO-FROM " + userInpt + "\n").encode(encoder)
    
    bytes_len = len(inpt)
    num_bytes_to_send = bytes_len

    if userInpt == "!who":
        r = "LIST\n"
        so.send(r.encode(encoder))
        res = so.recv(bytes)            
        if res:
            res=res[8:]
            serverInputs = res.decode().split(',')
            serverInputs=serverInputs[:-2]
            print("Users on server: ")
            cnt = 0
            for i in serverInputs:
                cnt+=1
                if cnt == (len(serverInputs) - 1):
                    print(i)
                    break
                print(i,end=", ")
            print("\n")
            
        else:
            print("No inputs received")
    
    elif userInpt == "!quit":                                        #quit statement
        break
    
    elif "@" in userInpt:
         inp_parts = userInpt.split(" ", 1)
         username = inp_parts[0][1:]
         message = inp_parts[1]
         if inp_parts[1]=="":
             print("No input provided, try again"+"\n")
             continue
         else:
             so.send(("SEND {} {}\n".format(username, message)).encode(encoder))
         res = so.recv(1024).decode()
         print("Message sent successfully")   
    else:
        while num_bytes_to_send > 0:
            
            num_bytes_to_send -= so.send(inpt[bytes_len-num_bytes_to_send:])
            res = so.recv(1024).decode()

            if res =="IN-USE\n":
                so.close()
                so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                so.connect(host_port)
                print("Username in use, try another username!")
            else:    
                print("Log in successful!")
                myThread.start()           

print("Server link closed")
so.close()  
