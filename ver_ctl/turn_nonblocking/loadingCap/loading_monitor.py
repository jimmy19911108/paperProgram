#!/usr/bin/env python3.5

import psutil
import time
from multiprocessing.pool import ThreadPool


def get_cpu_usage():
    '''
    get the average usage of cpus\n
    '''

    return psutil.cpu_percent()

def get_mem_usage():
    '''
    get the usage of memory
    '''

    return psutil.virtual_memory()[2]

def get_disk_usage():
    '''
    get the usage of disk
    '''

    return psutil.disk_usage("/")[3]

def get_bandwidth():
    '''
    get the network usage
    '''

    io_bytes_old = psutil.net_io_counters().bytes_recv + psutil.net_io_counters().bytes_sent
    time.sleep(1)
    
    return (psutil.net_io_counters().bytes_recv + psutil.net_io_counters().bytes_sent - io_bytes_old)/1024/1024*8


with open("throughput.txt", "w") as fopen_th, open("cpu.txt", "w") as fopen_cpu, open("mem.txt", "w") as fopen_mem, open("disk.txt", "w") as fopen_disk :
    
    pool = ThreadPool(processes=1)
        
    while True:
        cpu_usage = pool.apply_async(get_cpu_usage).get()
        throughput = pool.apply_async(get_bandwidth).get()
        disk_usage = pool.apply_async(get_disk_usage).get()
        mem_usage = pool.apply_async(get_mem_usage).get()

        print(cpu_usage)
        print(throughput)
        print(disk_usage)
        print(mem_usage)

        fopen_th.write(str(throughput)+"\n")
        fopen_cpu.write(str(cpu_usage)+"\n")
        fopen_disk.write(str(disk_usage)+"\n")
        fopen_mem.write(str(mem_usage)+"\n")
