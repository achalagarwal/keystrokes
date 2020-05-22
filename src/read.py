#!python3
# file1 = open("/var/log/logkeys.log","r") 
# print(file1.read())
from sh import tail
import subprocess
tail = tail("-F", "/var/log/logkeys.log", _iter=True, _out_bufsize=0)
f = subprocess.Popen(['tail','-F',"/var/log/logkeys.log"],\
        stdout=subprocess.PIPE,stderr=subprocess.PIPE)

while True:
#     line = f.stdout.readline()
#     print(line)
        print(tail.next())
