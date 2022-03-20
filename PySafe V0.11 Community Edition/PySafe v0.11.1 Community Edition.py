from win10toast import ToastNotifier
from datetime import datetime
import time as time
import os, hashlib

#PySafe v0.11

#Changelog: 
#New log data added and upgraded the file checking algorithm with hashlib!
#Detection of network drives like dev/sda1 etc...
#Finally a complete terminal menu!
#Multi-File support!

#Default settings' backup
toaster = ToastNotifier()
PySafeRuntime = str(datetime.now())
ScriptPath = os.path.dirname(os.path.abspath(__file__))
DesktopPath = "C:" + os.environ["HOMEPATH"] + "\\Desktop\\"
Delay = 10
BlockAccess = False
inBackground = False
Backup = False
Encrypt = False
NotifyWhenChanged = False
RunOnStartup = False
OnlyWindows = False
RefuseTerminating = False
WriteLog = False

#Gets default settings if there is a file that contains them. İf this file doesn't exist, PySafe writes the file itself.
def GetDefaults():
    if os.path.exists(f"{ScriptPath}\DefaultSettings.txt"):
        DefaultSettings = open(f"{ScriptPath}\DefaultSettings.txt", "r")
        Delay = str(DefaultSettings.readlines(1)).split(" ")[2]
        DefaultSettings.close()
    
    else:
        DefaultSettings = open(f"{ScriptPath}\DefaultSettings.txt", "w")
        DefaultSettings.write(f"ScriptPath = {ScriptPath}\n")
        DefaultSettings.write(f"DesktopPath = {DesktopPath}\n")
        DefaultSettings.write("Delay = 5\n")
        DefaultSettings.write(f"BlockAccess = {BlockAccess}\n")
        DefaultSettings.write(f"inBackground = {inBackground}\n")
        DefaultSettings.write(f"Backup = {Backup}\n")
        DefaultSettings.write(f"Encrypt = {Encrypt}\n")
        DefaultSettings.write(f"NotifyWhenStarted = {NotifyWhenChanged}\n")
        DefaultSettings.write(f"RunOnStartup = {RunOnStartup}\n")
        DefaultSettings.write(f"OnlyWindows = {OnlyWindows}\n")
        DefaultSettings.write(f"RefuseTerminating = {RefuseTerminating}\n")
        DefaultSettings.write(f"WriteLog = {WriteLog}")
        DefaultSettings.close()

#This function is used to log the PySafe actions and errors if permission is permitted.
def PySafelog():
    if WriteLog:
        PySafelog = open(f"{ScriptPath}\\{PySafeRuntime[:10]}.txt", "w")
        PySafelog.write(f"Pysafe Opened: {PySafeRuntime}")
        PySafelog.close()

#Default functions
GetDefaults()
PySafelog()

print("PySafe v0.11")
print("Choose a scanning method:")
print("1. Basic (scans desktop files)")
print("2. Advanced (scans a specified directory path)")
Choose = input("")

if Choose == "1":
    Files = os.listdir(DesktopPath)
elif Choose == "2":
    Files = input("Please specify a file checking path: ")
    if Files.find("dev\\sda1") != -1:
        print("Network drive detected. This is not tested and not guaranteed to work at all!")

print("\nPySafe started to scan the file. Press 'Control + C' to terminate the scan.\n")
        
#Caches for Files' MetaData
Cache1 = [] #FileSizeDictionary
Cache2 = [] #LastChangeTimeDictionary
Cache3 = [] #isFileDirectoryBooleans
Cache4 = [] #FileHashes
for File in os.listdir(Files):
    FilePath = Files + File
    Cache1.append(os.stat(FilePath).st_size)
    Cache2.append(str(datetime.fromtimestamp(os.stat(FilePath).st_mtime))[:-7])
    Cache3.append(os.path.isdir(FilePath))
    if os.path.isdir(FilePath) == False:
        OpenFile = open(FilePath, "r", encoding="utf8")
        FileData = OpenFile.read()
        OpenFile.close()
        Cache4.append(hashlib.sha1(bytes(FileData, "utf8")).hexdigest())
        FileData = None

#Warning Codes:

#0 = NoWarning
#1 = File Changed
#2 = File is a Directory (but changed anyway)
#3 = Unknown Error

WarningCode = 0

#The loop that checks the file's data for modification.
while True:
    for File in os.listdir(Files):
        FilePath = Files + File
        DirFiles = os.listdir(Files)
        Time = datetime.now()

        if Cache3[DirFiles.index(File)] == True:
            try:
                New_Last_Change_Time = str(datetime.fromtimestamp(os.stat(FilePath).st_mtime))[:-7]
                New_Size = os.stat(FilePath).st_size

                if New_Size != Cache1[DirFiles.index(File)] or New_Last_Change_Time != Cache2[DirFiles.index(File)]:
                    WarningCode = 2
                    break
                else:
                    print(Time)
                    print(f"Directory size: {New_Size}")
                    print(f"Last Changed: {New_Last_Change_Time}")
                    print(f"Directory: {File}\n")
                
                time.sleep(1)

            except Exception as Error:
                print(f"[ERROR: {Error}] Cant find the Directory: {File}")
                toaster.show_toast("PySafe Notification Service", "PySafe can't find the Directory!", duration=8)
                exit()

        else:
            try:
                New_Last_Change_Time = str(datetime.fromtimestamp(os.stat(FilePath).st_mtime))[:-7]
                New_Size = os.stat(FilePath).st_size

                OpenFile = open(FilePath, "r", encoding="utf8")
                FileData = OpenFile.read()
                OpenFile.close()
                NewFileHash = hashlib.sha1(bytes(FileData,"utf8")).hexdigest()
                FileData = None

                if New_Size != Cache1[DirFiles.index(File)] or New_Last_Change_Time != Cache2[DirFiles.index(File)] or NewFileHash != Cache4[DirFiles.index(File)]:
                    WarningCode = 1
                    break
                else:
                    print(Time)
                    print(f"File size: {New_Size}")
                    print(f"Last Changed: {New_Last_Change_Time}")
                    print(f"File SHA1: {NewFileHash}")
                    print(f"File: {File}\n")
                
                time.sleep(1)

            except Exception as Error:
                print(f"[ERROR: {Error}] Cant find the file: {File}")
                toaster.show_toast("PySafe Notification Service", "PySafe can't find the file!", duration=8, icon_path="Warning.ico")
                exit()

    if WarningCode == 1:
        print(Time)
        print(f"File Changed!")
        print(f"Old Size: {Cache1[DirFiles.index(File)]}")
        print(f"Old Last Changed: {Cache2[DirFiles.index(File)]}")
        print(f"New Size: {New_Size}")
        print(f"New Last Changed: {New_Last_Change_Time}")
        print(f"File: {File}\n")
        toaster.show_toast("PySafe Notification Service", "Protected file changed!", duration=10, icon_path="Warning.ico")

    if WarningCode == 2:
        print(Time)
        print(f"Directory Changed!")
        print(f"Old Size: {Cache1[DirFiles.index(File)]}")
        print(f"Old Last Changed: {Cache2[DirFiles.index(File)]}")
        print(f"New Size: {New_Size}")
        print(f"New Last Changed: {New_Last_Change_Time}")
        print(f"Directory: {File}\n")
        toaster.show_toast("PySafe Notification Service", "Protected Directory changed!", duration=10, icon_path="Warning.ico")