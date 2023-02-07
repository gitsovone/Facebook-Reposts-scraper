import os
import time
import psutil
import subprocess

names_start=["python3 add_reposts_chrome.py"]

find=[]

for name in names_start:
    for proc in psutil.process_iter():
        pinfo = proc.as_dict(attrs=['pid','name', 'cmdline'])
        if str(name).split("|")[1] in str(pinfo['cmdline']):
            try:
                pid =pinfo['pid']
                print(pid)
                print(pinfo['cmdline'])

                find.append(name)
            except Exception as e:
                print("e",e)

print("find",find)
f = open("/start_process.sh", "w")
f.write('')

for o in names_start:
    
    if o not in find:

        print("o", o)

        process = ["Xvfb",
                    "add_reposts_chrome.py",
                    "chromedriver", 
                    "chromium"]

        for name in process:
            for proc in psutil.process_iter():
                pinfo = proc.as_dict(attrs=['pid', 'name', 'cmdline'])
                if name in str(pinfo['cmdline']):
                    try:
                        pid = pinfo['pid']
                        parent = psutil.Process(pid)
                        for child in parent.children(
                                recursive=True):
                            child.kill()
                        parent.kill()
                    except Exception as e:
                        print("e", e)

        f.write(o.replace("|","") + " >>"+ o.replace("/usr/bin/python3","").replace("|","").replace(".py", ".logs") + " &\n" )
        f.write("sleep 3 \n")
f.close()

subprocess.call("start_process.sh", shell=True)

f = open("start_process.sh", "w")
f.write('')