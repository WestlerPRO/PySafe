# PySafe: A file checking and protection script

PySafe is made to check specified files for changes and protects them if wanted.

# How To Use

![g1](https://user-images.githubusercontent.com/101973565/174833249-394aa45e-417c-4837-b517-bfa25d129d40.png)

Use of PySafe is very straightforward. You can either select your desktop or specify a path yourself to check.
When you specify a path, it should start scanning.

![g3](https://user-images.githubusercontent.com/101973565/174833328-9522defc-ac4a-4ff1-9c53-866becbe7713.png)

While scanning is on, you will get the file's properties and it's hash. When the file is changed, you will get a notification and a warning on the console.
When PySafe starts scanning, you only have to press "Control + C" to terminate the scan.

# Settings

![g4](https://user-images.githubusercontent.com/101973565/174835563-e7073b44-8f6a-4277-ab30-db3766bedbad.png)

You can either change the settings in source code or you can just modify the DefaultSettings.txt file. Also you have a chance to change the settings temporarily in the Main Menu.

Inner Interval: Integer value for durations between file checking.
Outer Interval: Integer value for durations between laps.
Notify When Changed: Boolean value for notifications. When set to True, it will notify the user when a file is changed.
Write Log: Boolean value for PySafe Logs. When set to True, it will log all file actions.
Print Log: Boolean value for console prints. When set to True, it will print descriptions when it checks a file.
Developer Mode: Boolean value for advanced data printing. When set to True, it will print all the data every variable has on the console.
Read-Only: Boolean value for file protection. When set to True, all files will be set to read only.
Duration: Integer value for notification duration.
