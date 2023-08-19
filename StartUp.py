import os
import subprocess

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
with open("/Marzban/"+Mname+"/.env","w") as f:
    f.writelines('UVICORN_PORT = '+Port+'\nSUDO_USERNAME = "'+UserName+'"\nSUDO_PASSWORD = "'+PassWord+'"')
    f.close()
getCommandOutput("sudo unzip MainFiles.zip","utf-8")
getCommandOutput("mv MainFiles "+Mname,"utf-8")
getCommandOutput("cd "+Mname,"utf-8")
getCommandOutput('sudo echo "nameserver 178.22.122.100" > /etc/resolv.conf',"utf-8")
getCommandOutput("sudo pip3 install -r "+Mname+"/requirements.txt","utf-8")
getCommandOutput('sudo echo "nameserver 1.1.1.1" > /etc/resolv.conf',"utf-8")
getCommandOutput("sudo cd "+Mname+" && alembic upgrade head","utf-8")



#getCommandOutput("","utf-8")


with open("/etc/systemd/system/Marzban"+Mname+".service","w") as f:
    f.writelines("[Unit]\nDescription=Marzban"+Mname+"\n\n[Service]\n\nExecStart=python3 /Marzban/"+Mname+"/main.py\n\n[Install]\nWantedBy=multi-user.target")
    f.close()
getCommandOutput("sudo systemctl daemon-reload","utf-8")
getCommandOutput("sudo systemctl start Marzban"+Mname,"utf-8")
getCommandOutput("sudo systemctl enable Marzban"+Mname,"utf-8")