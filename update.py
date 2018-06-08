import subprocess
import sys
import time

time.sleep(2)
proc = subprocess.Popen('python client.py', shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
sys.exit()
