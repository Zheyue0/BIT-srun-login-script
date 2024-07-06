import os
import time
import subprocess
from configparser import ConfigParser
from BitSrunLogin.LoginManager import LoginManager

def get_ssid():
    result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if 'SSID' in line:
            ssid = line.split(':')[1].strip()
            return ssid
    return None

def is_connect_internet(testip):
    status = os.system(u"ping {} -n 8".format(testip))
    return status == 0

def always_login(username, password, testip, checkinterval):
    lm = LoginManager()
    login = lambda : lm.login(username=username, password=password)
    timestamp = lambda : print(time.asctime(time.localtime(time.time())))
    while 1:
        if (not is_connect_internet(testip)) and (get_ssid() == "BIT-Web"):
            timestamp()
            try:
                login()
            except Exception:
                pass
        time.sleep(checkinterval) 
        
if __name__ == "__main__":
    config = ConfigParser()
    config.read('config.ini')
    username = config['Auth']['username']
    password = config['Auth']['password']
    testip = '114.114.114.114'
    checkinterval = 5
    always_login(username, password, testip, checkinterval)
