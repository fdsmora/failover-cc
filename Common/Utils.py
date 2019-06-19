#!/usr/bin/python
import subprocess
import os
from datetime import datetime

PRIMARY = "primary"
STANDBY = "standby"
PRIMARY_PORT = 8084
STANDBY_PORT = 8087
MONITOR_PORT = 8080 
CURL = "/usr/bin/curl"
HB_TIMEOUT = 3000 # milliseconds
HB_RETRIES = 3
HB_FRECUENCY = 1 # seconds

test_data =  {
    "id": "5d06aabffca870c0de76aa79",
    "index": "0",
    "guid": "8c6af915-c68b-4263-912a-08c56557acc0",
    "isActive": "True",
    "balance": "$3,029.87",
    "picture": "http://placehold.it/32x32",
    "age": "25",
    "eyeColor": "blue",
    "name": "Cecelia Morgan",
    "gender": "female",
    "company": "VERTON",
    "email": "ceciliamorgan@verton.com",
    "phone": "+1 (983) 578-2433",
    "address": "523 Miami Court, Starks, Minnesota, 2078",
    "about": "Proident sint ea incididunt et ea ipsum Lorem occaecat nostrud adipisicing elit. Nulla veniam non elit enim magna esse dolore incididunt non velit. Reprehenderit cillum duis reprehenderit nostrud consequat eu sunt ea magna voluptate fugiat eiusmod. Id id reprehenderit in id excepteur. Exercitation ullamco do esse officia quis quis.\r\n",
    "registered": "2019-01-09T03:13:07 +06:00",
    "latitude": "-8.768006",
    "longitude": "-103.11563"
}


def shell(cmd, args):
#debug
    #debug_str = " ".join(args)
    #print (str(args))
    args.insert(0,cmd)
    FNULL = open(os.devnull, 'w')
    with open(os.devnull, 'w') as FNULL:
        proc = subprocess.Popen(args, stdout=FNULL)
        out, err = proc.communicate()
    return out, err

# return current time epoch in milliseconds
def epoch_now():
    return int(datetime.now().timestamp()*1000)
