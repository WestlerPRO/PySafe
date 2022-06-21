#Made by WestlerPro
from win10toast import ToastNotifier
from datetime import datetime
import time as time
import os, hashlib, psutil
from stat import S_IWRITE, S_IREAD

#S_IWRITE = Read-Only mode off
#S_IREAD = Read-Only mode on

#PySafe v1.0

#Changelog:
#Delay variable didn't end up being used in the version 11.1 is now fixed.
#Changed the function named "GetDefaults" to "Defaults" for generalizing.
#NotifyWhenChanged variable is now added.
#ScriptPath is not saved by PySafe now.
#Variables are now global to use in functions.
#Added new log data.
#Variables are converted to their proper type when loaded from the DefaultSettings.txt file.
#PrintLog boolean value is now added.
#Logs are used now.
#Close PySafe option is now added to the main menu.
#DeveloperMode boolean value is now added.
#Values now can be changed in the script menu.
#Ram monitoring added.
#PySafe is now using one line if conditions for less lines.
#Added DefaultFile variable and a menu choice for faster use.
#Added a built-in file viewer to view most recent log.
#Added protecting feature that blocks writing permissions to files.
#Fixed bool() function.
#Delay variable is replaced with InnerInterval and OuterInterval.
#NumberOfChecks and NumberOfLaps variables added.
#Added "go back" choice to menu.
#Added text colors.

#Known Issues:
#The notifications and printlogs are constantly triggered when the corresponding file is changed.

class Colors:
    default = "\033[1;37;40m"
    warning = "\033[1;33;40m"
    error = "\033[1;35;40m"
    title = "\033[1;32;40m"

#Defaults
#Not Saved to DefaultSettings.txt:
toaster = ToastNotifier()
PySafeRuntime = str(datetime.now())
ScriptPath = os.path.dirname(os.path.abspath(__file__))
NumberOfChecks = 0
NumberOfLaps = 0

#Saved
DesktopPath = "C:" + os.environ["HOMEPATH"] + "\\Desktop\\"
InnerInterval = 1
OuterInterval = 10
NotifyWhenChanged = True
WriteLog = True
PrintLog = True
DeveloperMode = True
DefaultFile = None
ReadOnly = False

def Bool(arg):
    if arg.lower() == "false":
        return False
    elif arg.lower() == "true":
        return True

#Gets default settings if there is a file that contains them. If this file doesn't exist, PySafe writes the file itself.
def Defaults():
    global DesktopPath, InnerInterval, OuterInterval, NotifyWhenChanged, WriteLog, PrintLog, DeveloperMode, DefaultFile, ReadOnly

    if os.path.exists(f"{ScriptPath}\\DefaultSettings.txt"):
        Settings = []
        DefaultSettings = open(f"{ScriptPath}\\DefaultSettings.txt", "r", encoding="utf-8")
        for line in DefaultSettings: Settings.append(str(line.split(" = ", 1)[1]).strip())
        DefaultSettings.close()
        DesktopPath = Settings[0]
        InnerInterval = int(Settings[1])
        OuterInterval = int(Settings[2])
        NotifyWhenChanged = Bool(Settings[3])
        WriteLog = Bool(Settings[4])
        PrintLog = Bool(Settings[5])
        DeveloperMode = Bool(Settings[6])
        DefaultFile = Settings[7]
        ReadOnly = Bool(Settings[8])

    else:
        DefaultSettings = open(f"{ScriptPath}\DefaultSettings.txt", "w")
        DefaultSettings.write(f"Desktop Path = {DesktopPath}\n")
        DefaultSettings.write(f"Inner Interval = {InnerInterval}\n")
        DefaultSettings.write(f"Outer Interval = {OuterInterval}\n")
        DefaultSettings.write(f"Notify When Started = {NotifyWhenChanged}\n")
        DefaultSettings.write(f"Write Log = {WriteLog}\n")
        DefaultSettings.write(f"Print Log = {PrintLog}\n")
        DefaultSettings.write(f"Developer Mode = {DeveloperMode}\n")
        DefaultSettings.write(f"Default File = {DefaultFile if DefaultFile != None else ''}\n")
        DefaultSettings.write(f"Read-Only = {ReadOnly}")
        DefaultSettings.close()

#This function is used to log the PySafe actions and errors if permission is permitted.
def PySafeLog(Data):
    if WriteLog:
        open(f"{ScriptPath}\\Logs\\{PySafeRuntime[:10]}.txt", "a+").write(Data)
        open(f"{ScriptPath}\\Logs\\{PySafeRuntime[:10]}.txt", "a+").close()

os.mkdir(f"{ScriptPath}\\Logs") if os.path.exists(f"{ScriptPath}\\Logs") == False else None
Defaults()
PySafeLog(f"[Pysafe Opened: {PySafeRuntime}]\n\n")

print(Colors.title + "PySafe v1.0\n" + Colors.default)
while True:
    print("[Main Menu]")
    print("1| Basic (scans desktop files)")
    print("2| Advanced (scans a specified directory path)")
    print("3| Scan DefaultFile")
    print("4| Change PySafe Settings")
    print("5| Close PySafe")
    print("6| View most recent log")
    Choose = input("")

    if Choose == "1":
        Files = os.listdir(DesktopPath)
        break

    elif Choose == "2":
        flag = 0
        while True:
            Files = input("Please specify a path (or press enter to go back): ")
            if Files == "":
                break
            elif os.path.exists(Files):
                flag = 1
                break
        if flag == 1:
            break

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

        InnerInterval = int(input("Set new value (Inner Interval): ")) if Change == "1" else InnerInterval
        OuterInterval = int(input("Set new value (Outer Interval): ")) if Change == "2" else OuterInterval
        NotiftyWhenChanged = Bool(input("Set new value (Notify When Changed): ")) if Change == "3" else NotifyWhenChanged
        WriteLog = Bool(input("Set new value (Write Log): ")) if Change == "4" else WriteLog
        PrintLog = Bool(input("Set new value (Print Log): ")) if Change == "5" else PrintLog
        DeveloperMode = Bool(input("Set new value (Developer Mode): ")) if Change == "6" else DeveloperMode
        ReadOnly = Bool(input("Set new value (Read-Only): ")) if Change == "7" else ReadOnly

    elif Choose == "5":
        print("Closing PySafe...")
        quit()

    elif Choose == "6":
        if os.path.exists(f"{ScriptPath}\\Logs\\{PySafeRuntime[:10]}.txt"):
            os.system("cls")
            LogFile = open(f"{ScriptPath}\\Logs\\{PySafeRuntime[:10]}.txt", "r")
            line = 1
            for Line in LogFile:
                print(f"{line}| {Line.strip()}")
                line += 1
            LogFile.close()

print("PySafe started to scan the file(s). Press 'Control + C' to terminate the scan.\n")

#Caches for Files' Metadata
Cache1 = [] #FileSizeDictionary
Cache2 = [] #LastChangeTimeDictionary
Cache3 = [] #isFileDirectoryBooleans
Cache4 = [] #FileHashes
for File in os.listdir(Files):
    if Files[-1] != "\\":
        FilePath = Files + "\\" + File
    else:
        FilePath = Files + File

    if ReadOnly:
        os.chmod(FilePath, S_IREAD)

    print(f"FilePath: {FilePath}") if DeveloperMode else None
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
    else:
        Cache4.append(None)

if DeveloperMode:
    print(Colors.title + "[Cache1: Sizes]" + Colors.default)
    for index in range(len(Cache1)): print(f"{list(os.listdir(Files))[index]}: {Cache1[index]} Bytes")
    print()
    print(Colors.title + "[Cache2: Last Modifying Time]" + Colors.default)
    for index in range(len(Cache2)): print(f"{list(os.listdir(Files))[index]}: {Cache2[index]}")
    print()
    print(Colors.title + "[Cache3: Directories]" + Colors.default)
    for index in range(len(Cache3)): print(f"{list(os.listdir(Files))[index]}: {Cache3[index]}")
    print()
    print(Colors.title + "[Cache4: Hashes]" + Colors.default)
    for index in range(len(Cache4)): print(f"{list(os.listdir(Files))[index]}: {Cache4[index]}")
    print()

#The loop that checks the file's data for modification.
while True:
    print(Colors.warning + "[WARNING] File protection is not on. The files are not protected by PySafe!" + Colors.default) if ReadOnly == False else None

    for File in os.listdir(Files):
        if Files[len(Files) - 1] != "\\":
            FilePath = Files + "\\" + File
        else:
            FilePath = Files + File

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
                        print(Colors.title + f"[Time: {Time} | File checking number: {NumberOfChecks} | Lap number: {NumberOfLaps}] [Control + C to terminate]" + Colors.default)
                        print(f"Folder Changed!")
                        print(f"Old Size: {Cache1[DirFiles.index(File)]}")
                        print(f"Old Last Changed: {Cache2[DirFiles.index(File)]}")
                        print(f"New Size: {New_Size}")
                        print(f"New Last Changed: {New_Last_Change_Time}")
                        print(f"Folder: {File}")
                        print(f"Ram Available: {int(psutil.virtual_memory().available / 2 ** 20)} MB\n")

                    if WriteLog:
                        PySafeLog(f"[Time: {Time} | File checking number: {NumberOfChecks} | Lap number: {NumberOfLaps}]\n")
                        PySafeLog(f"Folder Changed!\n")
                        PySafeLog(f"Old Size: {Cache1[DirFiles.index(File)]}\n")
                        PySafeLog(f"Old Last Changed: {Cache2[DirFiles.index(File)]}\n")
                        PySafeLog(f"New Size: {New_Size}\n")
                        PySafeLog(f"New Last Changed: {New_Last_Change_Time}\n")
                        PySafeLog(f"Folder: {File}\n\n")

                else:
                    if PrintLog:
                        print(Colors.title + f"[Time: {Time} | File checking number: {NumberOfChecks} | Lap number: {NumberOfLaps}] [Control + C to terminate]" + Colors.default)
                        print(f"File Changed!")
                        print(f"Old Size: {Cache1[DirFiles.index(File)]}")
                        print(f"Old Last Changed: {Cache2[DirFiles.index(File)]}")
                        print(f"New Size: {New_Size}")
                        print(f"New Last Changed: {New_Last_Change_Time}")
                        print(f"Old Hash: {Cache4[DirFiles.index(File)]}")
                        print(f"New Hash: {NewFileHash}")
                        print(f"File: {File}")
                        print(f"Ram Available: {int(psutil.virtual_memory().available / 2 ** 20)} MB\n")

                    if WriteLog:
                        PySafeLog(f"[Time: {Time} | File checking number: {NumberOfChecks} | Lap number: {NumberOfLaps}]\n")
                        PySafeLog(f"File Changed!\n")
                        PySafeLog(f"WarningCode = {WarningCode}\n")
                        PySafeLog(f"Old Size: {Cache1[DirFiles.index(File)]}\n")
                        PySafeLog(f"Old Last Changed: {Cache2[DirFiles.index(File)]}\n")
                        PySafeLog(f"New Size: {New_Size}\n")
                        PySafeLog(f"New Last Changed: {New_Last_Change_Time}\n")
                        PySafeLog(f"Old Hash: {Cache4[DirFiles.index(File)]}")
                        PySafeLog(f"New Hash: {NewFileHash}")
                        PySafeLog(f"File: {File}\n\n")

                toaster.show_toast("PySafe Notification Service", "Protected file or folder changed!", duration=10) if NotifyWhenChanged else None

            else:
                if bool(Cache3[DirFiles.index(File)]):
                    if PrintLog:
                        print(Colors.title + f"[Time: {Time} | File checking number: {NumberOfChecks} | Lap number: {NumberOfLaps}] [Control + C to terminate]" + Colors.default)
                        print(f"Folder size: {New_Size}")
                        print(f"Last Changed: {New_Last_Change_Time}")
                        print(f"Folder: {File}")
                        print(f"Ram Available: {int(psutil.virtual_memory().available / 2 ** 20)} MB\n")

                    if WriteLog:
                        PySafeLog(f"[Time: {Time} | File checking number: {NumberOfChecks} | Lap number: {NumberOfLaps}]\n")
                        PySafeLog(f"Folder size: {New_Size}\n")
                        PySafeLog(f"Last Changed: {New_Last_Change_Time}\n")
                        PySafeLog(f"Folder: {File}\n\n")

                else:
                    if PrintLog:
                        print(Colors.title + f"[Time: {Time} | File checking number: {NumberOfChecks} | Lap number: {NumberOfLaps}] [Control + C to terminate]" + Colors.default)
                        print(f"File size: {New_Size}")
                        print(f"Last Changed: {New_Last_Change_Time}")
                        print(f"File SHA1: {NewFileHash}")
                        print(f"File: {File}")
                        print(f"Ram Available: {int(psutil.virtual_memory().available / 2 ** 20)} MB\n")

                    if WriteLog:
                        PySafeLog(f"[Time: {Time} | File checking number: {NumberOfChecks} | Lap number: {NumberOfLaps}]\n")
                        PySafeLog(f"File size: {New_Size}\n")
                        PySafeLog(f"Last Changed: {New_Last_Change_Time}\n")
                        PySafeLog(f"File SHA1: {NewFileHash}")
                        PySafeLog(f"File: {File}\n\n")

            time.sleep(InnerInterval)

        except Exception as Error:
            print(Colors.error + f"[Time: {Time}]" + Colors.default)
            print(f"[ERROR: {Error}] PySafe can't find the file or folder: {File}")
            PySafeLog(f"[Time: {Time}]\n") if WriteLog else None
            PySafeLog(f"[ERROR: {Error}] PySafe can't find the file or folder: {File}\n\n") if WriteLog else None

            toaster.show_toast("PySafe Notification Service", "PySafe encountered an error!", duration=8) if NotifyWhenChanged else None
            exit()

    NumberOfLaps += 1
    time.sleep(OuterInterval)
