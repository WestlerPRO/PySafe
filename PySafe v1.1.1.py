#Made by WestlerPro
from win10toast import ToastNotifier
from stat import S_IWRITE, S_IREAD
from datetime import datetime
import os, hashlib, psutil
import time as time

#S_IWRITE = Read-Only mode off
#S_IREAD = Read-Only mode on

#PySafe v1.1.1

#Changelog:
#Grammar fixes
#If conditions are shortened.
#Fixed constant notification warnings.
#Added duration variable for notifications.
#Added console clearing option to the main menu.
#Fixes read-only warning to be printed only once.
#Added the file paths as variables to make the code look more clean.

#C = Colors
#D = Default
#W = Warning
#E = Error
#T = Title

class c:
    d = "\033[1;37;40m"
    w = "\033[1;33;40m"
    e = "\033[1;35;40m"
    t = "\033[1;32;40m"

#Defaults
#Not Saved to DefaultSettings.txt:
toaster        = ToastNotifier()
PySafeRuntime  = str(datetime.now())
ScriptPath     = os.path.dirname(os.path.abspath(__file__))
LogPath        = f"{ScriptPath}\\Logs\\{PySafeRuntime[:10]}.txt"
DefaultPath    = f"{ScriptPath}\\DefaultSettings.txt"
NumberOfChecks = 0
NumberOfLaps   = 0

#Saved
DesktopPath       = f"C:{os.environ['HOMEPATH']}\\Desktop\\"
InnerInterval     = 1
OuterInterval     = 10
NotifyWhenChanged = True
WriteLog          = True
PrintLog          = True
DeveloperMode     = True
DefaultFile       = None
ReadOnly          = False
Duration          = 8

def Bool(arg):
    if arg.lower() == "false": return False
    else: return True

#This function is used to log the PySafe actions and errors if permission is permitted.
def PySafeLog(Data):
    if WriteLog:
        open(LogPath, "a+").write(Data)
        open(LogPath, "a+").close()

#Gets default settings if there is a file that contains them. If this file doesn't exist, PySafe writes the file itself.
def Defaults():
    global DesktopPath, InnerInterval, OuterInterval, NotifyWhenChanged, WriteLog, PrintLog, DeveloperMode, DefaultFile, ReadOnly, Duration

    if os.path.exists(DefaultPath):
        Settings = []
        #DS = DefaultSettings
        DS = open(DefaultPath, "r", encoding="utf-8")
        for line in DS: Settings.append(str(line.split(" = ", 1)[1]).strip())
        DS.close()

        try:
            DesktopPath       = Settings[0]
            InnerInterval     = int(Settings[1])
            OuterInterval     = int(Settings[2])
            NotifyWhenChanged = Bool(Settings[3])
            WriteLog          = Bool(Settings[4])
            PrintLog          = Bool(Settings[5])
            DeveloperMode     = Bool(Settings[6])
            DefaultFile       = Settings[7]
            ReadOnly          = Bool(Settings[8])
            Duration          = int(Settings[9])
        
        except: PySafeLog(Exception)

    else:
        DS = open(DefaultPath, "w")
        DS.write(f"Desktop Path = {DesktopPath}\n")
        DS.write(f"Inner Interval = {InnerInterval}\n")
        DS.write(f"Outer Interval = {OuterInterval}\n")
        DS.write(f"Notify When Started = {NotifyWhenChanged}\n")
        DS.write(f"Write Log = {WriteLog}\n")
        DS.write(f"Print Log = {PrintLog}\n")
        DS.write(f"Developer Mode = {DeveloperMode}\n")
        DS.write(f"Default File = {DefaultFile}\n")
        DS.write(f"Read-Only = {ReadOnly}\n")
        DS.write(f"Duration = {Duration}")
        DS.close()

if not os.path.exists(f"{ScriptPath}\\Logs"): os.mkdir(f"{ScriptPath}\\Logs")
PySafeLog(f"[Pysafe Opened: {PySafeRuntime}]\n\n")
Defaults()

print(c.t + "PySafe version 1.1.1\n" + c.d)
while True:
    print("[Main Menu]")
    print("1| Basic (Scans desktop files)")
    print("2| Advanced (Scans a specified directory path)")
    print("3| Scan DefaultFile")
    print("4| Change PySafe Settings")
    print("5| Close PySafe")
    print("6| View most recent log")
    print("7| Clear the console")
    Choose = input("")

    if Choose == "1":
        Files = os.listdir(DesktopPath)
        break

    elif Choose == "2":
        flag = False
        while True:
            Files = input("Please specify a path (Press Enter to go back): ")
            if Files == "": break
            elif os.path.exists(Files):
                flag = True
                break
        if flag: break

    elif Choose == "3":
        if os.path.exists(DefaultFile):
            Files = DefaultFile
            break
        print("DefaultFile path does not exist.")

    elif Choose == "4":
        print("[PySafe Current Values]")
        print(f"1| Inner Interval: {InnerInterval}")
        print(f"2| Outer Interval: {OuterInterval}")
        print(f"3| Notify When Changed: {NotifyWhenChanged}")
        print(f"4| Write Log: {WriteLog}")
        print(f"5| Print Log: {PrintLog}")
        print(f"6| Developer Mode: {DeveloperMode}")
        print(f"7| Read-Only: {ReadOnly}")
        print(f"(Enter): Go back\n")
        Change = input("Select an option to change: ")

        if Change == "1": InnerInterval      = int(input("Set new value (Inner Interval): "))
        if Change == "2": OuterInterval      = int(input("Set new value (Outer Interval): "))
        if Change == "3": NotiftyWhenChanged = Bool(input("Set new value (Notify When Changed): "))
        if Change == "4": WriteLog           = Bool(input("Set new value (Write Log): "))
        if Change == "5": PrintLog           = Bool(input("Set new value (Print Log): "))
        if Change == "6": DeveloperMode      = Bool(input("Set new value (Developer Mode): "))
        if Change == "7": ReadOnly           = Bool(input("Set new value (Read-Only): "))

    elif Choose == "5":
        print("Closing PySafe...")
        quit()

    elif Choose == "6" and os.path.exists(LogPath):
        os.system("cls")
        LogFile = open(LogPath, "r")
        index = 1
        for line in LogFile:
            print(f"{index}| {line.strip()}")
            index += 1
        LogFile.close()
    
    elif Choose == "7": os.system("cls")

print("PySafe started to scan the file(s). Press 'Control + C' to terminate the scan.\n")

#Caches for Files' Metadata (and hashes)
Cache1 = [] #FileSizeDictionary
Cache2 = [] #LastChangeTimeDictionary
Cache3 = [] #isFileDirectoryBooleans
Cache4 = [] #FileHashes
for File in os.listdir(Files):
    if Files[-1] != "\\": FilePath = Files + "\\" + File
    else: FilePath = Files + File

    if ReadOnly: os.chmod(FilePath, S_IREAD)

    if DeveloperMode: print(f"File path: {FilePath}")
    Cache1.append(os.stat(FilePath).st_size)
    Cache2.append(str(datetime.fromtimestamp(os.stat(FilePath).st_mtime))[:-7])
    Cache3.append(os.path.isdir(FilePath))

    #Not finished
    if os.path.isdir(FilePath) == False and os.stat(FilePath).st_size < 209715200:
        OpenFile = open(FilePath, "rb")
        FileData = OpenFile.read()
        OpenFile.close()
        Cache4.append(hashlib.sha1(FileData).hexdigest())
        FileData = None
    else: Cache4.append(None)

if DeveloperMode:
    print(c.t + "[Cache1: Size]" + c.d)
    for index in range(len(Cache1)): print(f"{list(os.listdir(Files))[index]}: {Cache1[index]} Bytes")
    print()

    print(c.t + "[Cache2: Last Modifying Time]" + c.d)
    for index in range(len(Cache2)): print(f"{list(os.listdir(Files))[index]}: {Cache2[index]}")
    print()

    print(c.t + "[Cache3: Directory]" + c.d)
    for index in range(len(Cache3)): print(f"{list(os.listdir(Files))[index]}: {Cache3[index]}")
    print()

    print(c.t + "[Cache4: Hash]" + c.d)
    for index in range(len(Cache4)): print(f"{list(os.listdir(Files))[index]}: {Cache4[index]}")
    print()

#The loop that checks the file's data for modification.
if ReadOnly != True: print(c.w + "[WARNING] Read-Only mode is not on. The files are not protected by PySafe!" + c.d)
while True:
    for File in os.listdir(Files):
        if Files[len(Files) - 1] != "\\": FilePath = Files + "\\" + File
        else: FilePath = Files + File

        DirFiles = os.listdir(Files)
        Time = datetime.now()

        try:
            NumberOfChecks += 1
            New_Last_Change_Time = str(datetime.fromtimestamp(os.stat(FilePath).st_mtime))[:-7]
            New_Size = os.stat(FilePath).st_size

            #Not finished
            if bool(Cache3[DirFiles.index(File)]) == False and os.stat(FilePath).st_size < 209715200:
                OpenFile = open(FilePath, "rb")
                FileData = OpenFile.read()
                OpenFile.close()
                NewFileHash = hashlib.sha1(FileData).hexdigest()
                FileData = None

            if New_Size != Cache1[DirFiles.index(File)] or New_Last_Change_Time != Cache2[DirFiles.index(File)]:
                if bool(Cache3[DirFiles.index(File)]):
                    if PrintLog:
                        print(c.t + f"[Time: {Time} | File checking number: {NumberOfChecks} | Lap number: {NumberOfLaps}] [Control + C to terminate]" + c.d)
                        print(f"Folder Changed!")
                        print(f"Folder: {File}")
                        print(f"Old Size: {Cache1[DirFiles.index(File)]}")
                        print(f"Old Last Changed: {Cache2[DirFiles.index(File)]}")
                        print(f"New Size: {New_Size}")
                        print(f"New Last Changed: {New_Last_Change_Time}")
                        print(f"RAM Available: {int(psutil.virtual_memory().available / 2 ** 20)} MB\n")

                    if WriteLog:
                        PySafeLog(f"[Time: {Time} | File checking number: {NumberOfChecks} | Lap number: {NumberOfLaps}]\n")
                        PySafeLog(f"Folder Changed!\n")
                        PySafeLog(f"Folder: {File}\n")
                        PySafeLog(f"Old Size: {Cache1[DirFiles.index(File)]}\n")
                        PySafeLog(f"Old Last Changed: {Cache2[DirFiles.index(File)]}\n")
                        PySafeLog(f"New Size: {New_Size}\n")
                        PySafeLog(f"New Last Changed: {New_Last_Change_Time}\n\n")

                    Cache1[DirFiles.index(File)] = New_Size
                    Cache2[DirFiles.index(File)] = New_Last_Change_Time

                else:
                    if PrintLog:
                        print(c.t + f"[Time: {Time} | File checking number: {NumberOfChecks} | Lap number: {NumberOfLaps}] [Control + C to terminate]" + c.d)
                        print(f"File Changed!")
                        print(f"File: {File}")
                        print(f"Old Size: {Cache1[DirFiles.index(File)]}")
                        print(f"Old Last Changed: {Cache2[DirFiles.index(File)]}")
                        print(f"New Size: {New_Size}")
                        print(f"New Last Changed: {New_Last_Change_Time}")
                        print(f"Old Hash: {Cache4[DirFiles.index(File)]}")
                        print(f"New Hash: {NewFileHash}")
                        print(f"RAM Available: {int(psutil.virtual_memory().available / 2 ** 20)} MB\n")

                    if WriteLog:
                        PySafeLog(f"[Time: {Time} | File checking number: {NumberOfChecks} | Lap number: {NumberOfLaps}]\n")
                        PySafeLog(f"File Changed!\n")
                        PySafeLog(f"File: {File}\n")
                        PySafeLog(f"Old Size: {Cache1[DirFiles.index(File)]}\n")
                        PySafeLog(f"Old Last Changed: {Cache2[DirFiles.index(File)]}\n")
                        PySafeLog(f"New Size: {New_Size}\n")
                        PySafeLog(f"New Last Changed: {New_Last_Change_Time}\n")
                        PySafeLog(f"Old Hash: {Cache4[DirFiles.index(File)]}\n")
                        PySafeLog(f"New Hash: {NewFileHash}\n\n")

                    Cache1[DirFiles.index(File)] = New_Size
                    Cache2[DirFiles.index(File)] = New_Last_Change_Time

                if NotifyWhenChanged: toaster.show_toast("PySafe Notification Service", "Protected file or folder changed!", duration=Duration)

            else:
                if bool(Cache3[DirFiles.index(File)]):
                    if PrintLog:
                        print(c.t + f"[Time: {Time} | File checking number: {NumberOfChecks} | Lap number: {NumberOfLaps}] [Control + C to terminate]" + c.d)
                        print(f"Folder: {File}")
                        print(f"Folder size: {New_Size}")
                        print(f"Last Changed: {New_Last_Change_Time}")
                        print(f"RAM Available: {int(psutil.virtual_memory().available / 2 ** 20)} MB\n")

                    if WriteLog:
                        PySafeLog(f"[Time: {Time} | File checking number: {NumberOfChecks} | Lap number: {NumberOfLaps}]\n")
                        PySafeLog(f"Folder: {File}\n")
                        PySafeLog(f"Folder size: {New_Size}\n")
                        PySafeLog(f"Last Changed: {New_Last_Change_Time}\n\n")

                else:
                    if PrintLog:
                        print(c.t + f"[Time: {Time} | File checking number: {NumberOfChecks} | Lap number: {NumberOfLaps}] [Control + C to terminate]" + c.d)
                        print(f"File: {File}")
                        print(f"File size: {New_Size}")
                        print(f"Last Changed: {New_Last_Change_Time}")
                        print(f"File SHA1: {NewFileHash}")
                        print(f"RAM Available: {int(psutil.virtual_memory().available / 2 ** 20)} MB\n")

                    if WriteLog:
                        PySafeLog(f"[Time: {Time} | File checking number: {NumberOfChecks} | Lap number: {NumberOfLaps}]\n")
                        PySafeLog(f"File: {File}\n")
                        PySafeLog(f"File size: {New_Size}\n")
                        PySafeLog(f"Last Changed: {New_Last_Change_Time}\n")
                        PySafeLog(f"File SHA1: {NewFileHash}\n\n")

            time.sleep(InnerInterval)

        except:
            print(c.e + f"[Time: {Time}]" + c.d)
            print(f"[ERROR: {Exception}] PySafe can't find the file or folder: {File}")
            if WriteLog: PySafeLog(f"[Time: {Time}]\n")
            if WriteLog: PySafeLog(f"[ERROR: {Exception}] PySafe can't find the file or folder: {File}\n\n")

            if NotifyWhenChanged: toaster.show_toast("PySafe Notification Service", "PySafe encountered an error!", duration=Duration)
            exit()

    NumberOfLaps += 1
    time.sleep(OuterInterval)