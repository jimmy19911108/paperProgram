#!/usr/bin/env python3.5

import socket
import multiprocessing as mp
import time

def send_data(port, user1):
  while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(("stream"+user1).encode("utf-8"), ("192.168.1.122", port))
    time.sleep(1)

def test(user1, user2, sleep):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  # local: test1, remote: test2
  s.sendto(("allocate " + user1 + " " + user2).encode("utf-8"), ("192.168.1.122", 3478))
  data, addr = s.recvfrom(65515)
  data = data.decode("utf-8").split(" ")

  print(addr[0])
  print(data)
  local_port = int(data[0])
  port = int(data[1])
  s.sendto("bind".encode("utf-8"), (addr[0], int(data[1])))
  data, addr = s.recvfrom(65515)
  print(data.decode("utf-8"))
  proc = mp.Process(target = send_data, args = (local_port, user1))
  proc.start()
  while True:
    data, addr = s.recvfrom(65515)
    print(str(addr) + data.decode("utf-8"))
    time.sleep(1)
    s.close()

proc = mp.Process(target = test, args = ("test1", "test2", False))
proc.start()

#proc = mp.Process(target = test, args = ("test2", "test1", True))
#proc.start()
