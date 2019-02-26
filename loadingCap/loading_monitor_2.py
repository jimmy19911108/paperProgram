#!/usr/bin/env python3.5

import psutil
import time
import multiprocessing

def get_cpu_usage():
    '''
    get the average usage of cpus\n
    '''

    with open("cpu.txt", "w", 1) as fopen:
        while True:
            fopen.write(str(psutil.cpu_percent())+"\n")
            time.sleep(1)

def get_mem_usage():
    '''
    get the usage of memory
    '''

    with open("mem.txt", "w", 1) as fopen:
        while True:
            fopen.write(str(psutil.virtual_memory()[2])+"\n")
            time.sleep(1)

"""def get_disk_usage():
    '''
    get the usage of disk
    '''

    with open("disk.txt", "w", 1) as fopen:
        while True:
            fopen.write(str(psutil.disk_usage("/")[3])+"\n")
            time.sleep(1)"""

def get_net_loading_sent():
    '''
    get the network usage
    '''

    io_byte_old = psutil.net_io_counters().bytes_sent

    with open("net_sent.txt", "w", 1) as fopen:
        while True:
            time.sleep(1)
            io_byte_new = psutil.net_io_counters().bytes_sent

            fopen.write(str((io_byte_new - io_byte_old)/1024/1024*8)+"\n")
            
            io_byte_old = io_byte_new


def get_net_loading_recv():
    '''
    get the network usage for sending data
    '''

    io_byte_old = psutil.net_io_counters().bytes_recv
    
    with open("net_recv.txt", "w", 1) as fopen:
        while True:
            time.sleep(1)
            io_byte_new = psutil.net_io_counters().bytes_recv
            
            fopen.write(str((io_byte_new - io_byte_old)/1024/1024*8)+"\n")

            io_byte_old = io_byte_new


t1 = multiprocessing.Process(target = get_cpu_usage)
t1.start()

t2 = multiprocessing.Process(target = get_mem_usage)
t2.start()

"""t3 = multiprocessing.Process(target = get_disk_usage)
t3.start()"""

t4 = multiprocessing.Process(target = get_net_loading_sent)
t4.start()

t5 = multiprocessing.Process(target = get_net_loading_recv)
t5.start()
