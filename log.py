## Author Giro
#
## Prints the output of the terminal and stores it to the specified log file (plot.log)
#
## Put this script in the build folder of Madmax's chia-plotter
#
import os
import sys
import subprocess
import shlex
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT
dir = os.path.dirname(os.path.realpath(__file__))
logfile = 'plot.log'


## Put your command here
#
plot = "./chia_plot -n 1 -p your-public-key -f your-farmer-key -t /mnt/raid0/ -d /mnt/18TB/ -r 16 -u 7"


plot = subprocess.Popen(shlex.split(plot), cwd=dir, stdout=PIPE, stderr=STDOUT, universal_newlines=True)
with open(logfile, 'a') as log:
	for line in plot.stdout:
	    sys.stdout.write(line)
	    log.write(str(datetime.now()) + ": " + line)
	    log.flush()
