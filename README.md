# chia-plotter-logger

Logger for madMAx43v3r's chia-plotter
<br>https://github.com/madMAx43v3r/chia-plotter

I've only tested it using python3 on Ubuntu.

Prints the output of the terminal and stores it to the specified log file (plot.log)

Put this script in the build folder of Madmax's chia-plotter
Open the file and edit the command with your arguments in it

To use it: `python3 log.py`


Example Output:

```2021-06-11 20:52:35.449595: Multi-threaded pipelined Chia k32 plotter - 2920125
2021-06-11 20:52:35.449626: Final Directory: /mnt/SG8TB2/
2021-06-11 20:52:35.449635: Number of Plots: 1
2021-06-11 20:52:35.449830: Process ID: 1495658
2021-06-11 20:52:35.449835: Number of Threads: 16
2021-06-11 20:52:35.449839: Number of Buckets: 2^7 (128)
2021-06-11 20:52:35.458319: Pool Public Key: 
2021-06-11 20:52:35.458330: Farmer Public Key:
2021-06-11 20:52:35.463158: Working Directory:   /mnt/raid0/
2021-06-11 20:52:35.463165: Working Directory 2: /mnt/raid0/
2021-06-11 20:52:35.463170: Plot Name: plot-k32-2021-06-11-20-52-a248c78f42a9362687861376ea7ca9702d36
2021-06-11 20:52:53.530720: [P1] Table 1 took 18.0043 sec
2021-06-11 20:55:20.827694: [P1] Table 2 took 147.292 sec, found 4294903206 matches```
