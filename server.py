from socket import *
from threading import Thread

PORT: int = 4041
BACKLOG: int = 10

# Response Codes Used:
# 200 - Success (User logged in)
# 220 - Success (User disconnected)

def response_code(sock: socket, code: int, msg = ""):
    newMsg = str(code) + " " + msg
    sock.send(newMsg.encode())
    return (code < 400)

def client_handler(sock: socket, addr: tuple):
    print('Connection from ', addr)
    response_code(sock, 200, "Connection Successful. Welcome!\n")

    requireService = True

    while requireService:

        s = sock.recv(1024).decode().rstrip()
        print("(" + addr[0] + ") message: ", s)

        if s == 'quit':
            response_code(sock, 220, "SUCCESSFUL")
            requireService = False


    print(addr, ' is disconnected')
    sock.close()

def start_server():

    try:
        sock = socket(AF_INET, SOCK_STREAM)
    except:
        print("Error creating socket")

    sock.bind(('', PORT))

    sock.listen(BACKLOG)

    while True:
        acceptSoc, addr = sock.accept()

        newThread = Thread(target=client_handler, args=(acceptSoc, addr))
        newThread.run()
        # newThread.join()

    sock.close()


if __name__ == "__main__":
    start_server()