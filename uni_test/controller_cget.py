import socket
import multiprocessing as mp


def client1():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.1.201", 5000))
    s.send("cget test1".encode("utf-8"))
    data = s.recv(1024).decode("utf-8")
    print("client1: " + data)

def client2():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.1.201", 5000))
    s.send("cget test2".encode("utf-8"))
    data = s.recv(1024).decode("utf-8")
    print("client2: " + data)

proc = mp.Process(target = client1)
proc.start()

client2()
