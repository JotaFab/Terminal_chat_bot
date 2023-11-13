import time 
import os
import json

path = os.getcwd()
def log_to_file(log_name,val):
    """Log a value to a _log.txt file and the app_log.txt file"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    
    with open(f"{path}/logs/{log_name}_log.json", 'a') as f:
        f.write(f"{timestamp}: \n{val} \n")
        
    with open(f"{path}/logs/app_log.json", "a") as f:
        f.write(f"{timestamp}: \n{val} \n")
        
    f.close()