import os
import subprocess
import  pathlib, urllib.request, urllib.error, json

def getCommandOutput(consoleCommand, consoleOutputEncoding="utf-8", timeout=2000):
    isRunCmdOk = False
    consoleOutput = ""
    try:
        consoleOutputByte = subprocess.check_output(consoleCommand, shell=True, timeout=timeout)
        consoleOutput = consoleOutputByte.decode(consoleOutputEncoding) # '640x360\n'
        consoleOutput = consoleOutput.strip() # '640x360'
        isRunCmdOk = True
    except subprocess.CalledProcessError as callProcessErr:
        cmdErrStr = str(callProcessErr)
        print("Error %s for run command %s" % (cmdErrStr, consoleCommand))
    return isRunCmdOk, consoleOutput
Mname=input("Marzban Name: ")
Port=input("Marzban Port: ")
UserName=input("Marzban UserName: ")
PassWord=input("Marzban PassWord: ")

getCommandOutput("sudo unzip MainFiles.zip","utf-8")
getCommandOutput("mv MainFiles "+Mname,"utf-8")
with open("/Marzban/"+Mname+"/.env","w") as f:
    f.writelines('UVICORN_PORT = '+Port+'\nSUDO_USERNAME = "'+UserName+'"\nSUDO_PASSWORD = "'+PassWord+'"')
    f.close()
getCommandOutput("cd "+Mname,"utf-8")
IP_SHECAN = "185.51.200.2"
try:
    res = urllib.request.urlopen(f'https://ipinfo.io/json').read().decode('utf8')
    res = json.loads(res)
    if res["country"] == "IR": IP_SHECAN = "185.51.200.2"
    else: IP_SHECAN = "1.1.1.1"
except urllib.error.HTTPError:
    IP_SHECAN = "185.51.200.2"
getCommandOutput('sudo echo "nameserver '+IP_SHECAN+'" > /etc/resolv.conf',"utf-8")
getCommandOutput("sudo pip3 install -r "+Mname+"/requirements.txt","utf-8")
getCommandOutput("sudo rm -rf /usr/lib/python3/dist-packages/OpenSSL")
getCommandOutput("sudo pip3 install pyopenssl --upgrade")
getCommandOutput('sudo echo "nameserver 1.1.1.1" > /etc/resolv.conf',"utf-8")
getCommandOutput("cd "+Mname+" && sudo alembic upgrade head","utf-8")



#getCommandOutput("","utf-8")


with open("/etc/systemd/system/Marzban"+Mname+".service","w") as f:
    f.writelines("[Unit]\nDescription=Marzban"+Mname+"\n\n[Service]\n\nExecStart=python3 /Marzban/"+Mname+"/main.py\n\n[Install]\nWantedBy=multi-user.target")
    f.close()
getCommandOutput("sudo systemctl daemon-reload","utf-8")
getCommandOutput("sudo systemctl start Marzban"+Mname,"utf-8")
getCommandOutput("sudo systemctl enable Marzban"+Mname,"utf-8")
