'''
Monitor the resource of this computer
'''

import psutil
import iperf3
import time
import threading
import network_interface as net_if
from multiprocessing.pool import ThreadPool


class RsourceMonitor():

    def __init__(self):
        self.set_bandwidth()

    def set_bandwidth(self):
        '''
        set the total bandwidth
        '''

        client = iperf3.Client()
        client.duration = 10
        client.server_hostname = net_if.get_ctrller_ip()
        self.total_bandwidth = client.run().sent_Mbps

    def get_cpu_usage(self):
        '''
        get the average usage of cpus\n
        ( get the average usage of each core in 10 seconds for 0.1 second interval )
        '''

        usage_sum = 0

        for i in range(10):
            usage_sum += psutil.cpu_percent(interval=0.1)

        return usage_sum/10

    def get_mem_usage(self):
        '''
        get the usage of memory
        '''

        return psutil.virtual_memory()[2]

    def get_disk_usage(self):
        '''
        get the usage of disk
        '''

        return psutil.disk_usage("/")[3]

    def get_bandwidth(self):
        '''
        get the network usage
        '''

        io_bytes_old = psutil.net_io_counters().bytes_recv + psutil.net_io_counters().bytes_sent
        time.sleep(1)
        io_bytes = psutil.net_io_counters().bytes_recv + psutil.net_io_counters().bytes_sent

        io_mega_bits = (io_bytes - io_bytes_old)/1024/1024*8

        return io_mega_bits/self.total_bandwidth*100

    def get_all_info(self):
        '''
        get all resource info
        '''

        # threading pool for getting return value
        pool = ThreadPool(processes=1)

        cpu_usage = pool.apply_async(self.get_cpu_usage).get()
        bandwidth_usage = pool.apply_async(self.get_bandwidth).get()
        disk_usage = pool.apply_async(self.get_disk_usage).get()
        mem_usage = pool.apply_async(self.get_mem_usage).get()

        return cpu_usage, bandwidth_usage, disk_usage, mem_usage