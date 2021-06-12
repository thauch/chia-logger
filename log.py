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
import psutil
import json
import requests
import logging
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT
from requests.exceptions import HTTPError

## Put your command here
#
plot = "./chia_plot -n -1 -p -f -t /home/plotter1/raid0/ -d /media/plotter1/SG8TB2/ -r 16 -u 7"

## Dashboard settings
updateDashboard = True
dashboardApiKey = 'XXXXXXXXXXXXXXXXXXXXXXXX'

dir = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(filename='dashboard.log', format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.ERROR)
logfile = 'plot.log'

## Phase weight
phase1_weight = 43.6
phase2_weight = 22.9
phase3_weight = 29.4
phase4_weight = 4.0

## Check if process is still running
def check_pid(pid):        
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

## Update dashboard satellite
def dashboard_request(id, startTime, phase, progress):
    data = {
        "plotter": {
        "jobs": [{
            "id": id,
            "startedAt": str(startTime),
            "state": "RUNNING",
            "kSize": 32,
            "phase": phase,
            "progress": progress
        }]
    }
    }
    data = json.dumps(data)
    # url = dashboard_settings.get('dashboard_update_url')
    url = "https://us.chiadashboard.com"
    headers = {
        # 'Authorization': "Bearer " + dashboard_settings.get('dashboard_api_key'),
        'Authorization': 'Bearer ' + dashboardApiKey,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.patch(url + '/api/satellite', headers=headers, data=data)
        if response.status_code == 204:
            dashboard_status = "[Dashboard] Connected"
            logging.info(dashboard_status)
        elif  response.status_code == 429:
            dashboard_status = "[Dashboard] Too many Requests. Slow down."
            logging.error(dashboard_status + str(response))
        else:
            response.raise_for_status()
    except HTTPError:
        if response.status_code == 401:
            dashboard_status = "[Dashboard] Unauthorized. Possibly invalid API key?"
            logging.error(dashboard_status + str(response))
        else:
            dashboard_status = "[Dashboard] Unable to connect."
            logging.error(dashboard_status + str(response))
    except requests.exceptions.ConnectionError:
        dashboard_status = "[Dashboard] Connection Error. Chiadashboard.com may not be responding."
        logging.error(dashboard_status)
    return dashboard_status

phase1_count = phase2_count = phase3_count = phase4_count = 0
plot = subprocess.Popen(shlex.split(plot), cwd=dir, stdout=PIPE, stderr=STDOUT, universal_newlines=True)
with open(logfile, 'a') as log:
    for line in plot.stdout:
        sys.stdout.write(line)
        log.write(str(datetime.now()) + " => " + line)
        if updateDashboard == True:
            if "Process ID" in line:
                id = line.split("Process ID: ")[1]
            if "Plot Name" in line:
                startTime = datetime.now()
            if "[P1]" in line:
                phase = 1
                phase1_count += 1
                progress = (phase1_count*(phase1_weight/7)) / 100
                dashboard_request(id, startTime, phase, progress)
                if phase1_count == 7:
                    phase1_count = 0
            if "[P2]" in line:
                phase = 2
                phase2_count += 1
                progress = ((phase2_count*(phase2_weight/13)) + phase1_weight) / 100
                dashboard_request(id, startTime, phase, progress)
                if phase2_count == 13:
                    phase2_count = 0
            if "[P3-" in line:
                phase = 3
                phase3_count += 1
                progress = ((phase3_count*(phase3_weight/12)) + phase1_weight + phase2_weight) / 100
                dashboard_request(id, startTime, phase, progress)
                if phase3_count == 12:
                    phase3_count = 0
            if "[P4]" in line:
                phase = 4
                phase1_count += 1
                progress = ((phase4_count*(phase4_weight/4)) + phase1_weight + phase2_weight + phase3_weight) / 100
                dashboard_request(id, startTime, phase, progress)
                if phase4_count == 4:
                    phase4_count = 0
            if "Started copy to" in line:
                phase = 5
                progress = 1.00
                dashboard_request(id, startTime, phase, progress)
            
            #     if check_pid(id) == False:
            #         dashboard_request(id, startTime, phase, progress)
        log.flush()
    




