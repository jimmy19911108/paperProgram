#!/usr/bin/env python3.5

import matplotlib.pyplot as plt


filename = input("Input file name: ")

if filename.split(".")[0] in ["cpu", "mem", "disk"]:
    ylabel_name = "%"
else:
    ylabel_name = "Mbps"

with open(filename, "r") as fread:
    temp = fread.readlines()

    for i in range(0, len(temp)):
        temp[i] = float(temp[i])

    plt.plot(range(1,len(temp)+1), temp)
    plt.ylabel(ylabel_name)
    plt.xlabel("second")
    plt.ylim(ymax = 100)
    plt.xlim(xmin = 1)
    plt.grid(True)
    plt.show()