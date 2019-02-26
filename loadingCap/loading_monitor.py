#!/usr/bin/env python3.5

import psutil
import time
import multiprocessing

def get_cpu_usage():
    '''
    get the average usage of cpus\n
    '''

    with open("cpu.txt", "w") as fopen:
        while True:
            fopen.write(str(psutil.cpu_percent())+"\n")
            time.sleep(1)

def get_mem_usage():
    '''
    get the usage of memory
    '''

    with open("mem.txt", "w") as fopen:
        while True:
            fopen.write(str(round((1-psutil.virtual_memory()[1]/psutil.virtual_memory()[0])*100, 4))+"\n")
            time.sleep(1)

def get_disk_usage():
    '''
    get the usage of disk
    '''

    with open("disk.txt", "w") as fopen:
        while True:
            fopen.write(str(psutil.disk_usage("/")[3])+"\n")
            time.sleep(1)

def get_bandwidth():
    '''
    get the network usage
    '''

    io_bytes_old = psutil.net_io_counters().bytes_recv + psutil.net_io_counters().bytes_sent

    with open("throughput.txt", "w") as fopen:
        while True:
            time.sleep(1)
            io_bytes_new = psutil.net_io_counters().bytes_recv + psutil.net_io_counters().bytes_sent
            
            fopen.write(str((io_bytes_new-io_bytes_old)/1024/1024*8)+"\n")
            
            io_bytes_old = io_bytes_new


t1 = multiprocessing.Process(target = get_cpu_usage)
t1.start()

t2 = multiprocessing.Process(target = get_mem_usage)
t2.start()

t3 = multiprocessing.Process(target = get_disk_usage)
t3.start()

t4 = multiprocessing.Process(target = get_bandwidth)
t4.start()
