# PySafe: A file checking and protection script

PySafe is made to check specified files for changes and protects them if wanted.

# How To Use

![g1](https://user-images.githubusercontent.com/101973565/174833249-394aa45e-417c-4837-b517-bfa25d129d40.png)

Use of PySafe is very straightforward. You can either select your desktop or specify a path yourself to check.
When you specify a file, it should start scanning.

![g2](https://user-images.githubusercontent.com/101973565/174833298-53556cde-a6d4-475e-b1ef-aa7b9a0d3e26.png)

While scanning is on, you will get the file's properties and it's hash. When the file is changed, you will get a notification and a warning on the console.
When you start scanning, you only have to press "Control + C" to terminate the scan.

# Settings

![g3](https://user-images.githubusercontent.com/101973565/174833328-9522defc-ac4a-4ff1-9c53-866becbe7713.png)

You can either change the settings in source code or you can just modify the DefaultSettings.txt file. Also you have a chance to change the settings temporarily in the Main Menu.

Inner Interval is the amount of time that PySafe is going to wait between checking the files.
The Outer Interval is the amount of time that PySafe is going to wait when it finishes checking all files.
