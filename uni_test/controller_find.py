import socket
import multiprocessing as mp


def client1():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.1.42", 5000))
    s.send("find test1 test2 TW".encode("utf-8"))
    data = s.recv(1024).decode("utf-8")
    print("client1: " + data)

def client2():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.1.42", 5000))
    s.send("find test2 test1 TW".encode("utf-8"))
    data = s.recv(1024).decode("utf-8")
    print("client2: " + data)

proc = mp.Process(target = client1)
proc.start()

client2()
