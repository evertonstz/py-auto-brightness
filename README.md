# pyautobrightness
Pyautobrightness is a very simple "Calise like" program, wrote in python, designed to change the screen brightness using the webcam as a pseudo light sensor.

### Installation

Pyautobrightness primally requires [python 2.7.x](https://www.python.org/download/releases/2.7/) to run.

ArchLinux: you can download the package from [AUR](https://aur.archlinux.org/packages/pyautobrightness/), or install with yaourt:

```sh
$ yaourt pyautobrightness
```
Windows (tested only on Windows 10 64bits): install [OpenCV (3.1.0)](http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv) and [PyWin32 for py 2.7](https://sourceforge.net/projects/pywin32/files/pywin32/). Install pyautobrightness itself with [pip](http://docs.python-guide.org/en/latest/starting/install/win/). When pip is up and running, just run the following on cmd:
```sh
> pip install pyautobrightness
```
Other Distros: not tested, but pip is suposed to work:
```sh
$ pip install pyautobrightness
```

### Dependences

Pyautobrightness currently depends on the following tech:

* Pygame (linux only)
* Numpy
* Pillow
* Xorg Xbacklight (linux only)
* pywin32 (windows only)
* WMI (windows only)
* OpenCV (windows only)

### Version
0.3

### Comented Conf file
In this section I'll try to explain each aspect from the conf file:

>Minimum_Brightness = 10

Possible values are positive numbers between 0 and 100. The software will never set the brightness for less than the stated in this option;


>Maximum_Brightness = 90

Possible values are positive numbers between 0 and 100. The software will never set the brightness for more than the stated in this option;

>Transition = 4000

Linux only. Possible values are positive numbers. This set the transition time in xbacklight, 1000 is one second, try to not set it for more than 5 seconds;

>NumberOfPictures = 2

Possible values are positive numbers. This option set how many pictures the software will take to measure the brightness, the more the better and slower. NumberOfPictures= 2 with Mode=precise is the best combination;

>TimeBetweenPictures = 1

Possible values are positible numbers only (0 is possible, but not recommended). This is the time between the pictures in seconds, if NumberOfPictures=1 this option is ignored.

>Mode = precise

Possible values are "precise" and "normal". In precise mode pyautobrightness will try to get the better brightness by taking more pictures (if necessary) and giving it a statistical treatment. For security reasons, the Precise method will run up to 3 MORE times than the value set by the user in NumberOfPictures if it didn't met the estatistical requirements. In Normal mode it'll only take the number of pictures set by the user in NumberOfPictures.

>x = 5,65\
>y = 55,98

Those are the the numbers that are stored when the user run this program with the --calibrate argument, they are used to interpolate an equation in the script with Numpy's help. The more, the better. Try to not change it manually, unless you know what you're doing. If the software is setting strange brightness you can run "pyautobrightness --calibrate reset" to clean all your calibrations

### Changelog

>0.2 - windows support (tested on windows 10 64bits only), migrated from python 3 to python 2 due to library problems, cleaned some code\
>0.2 - added help and some arguments. Also some changes to add the package into pypi.\
>0.1 - the first version is a mess, but It works. My only focus in this version was to get the math to work, and it does quite well 


### Todos

 - add the "odd" option to fix odd values in the stored calibrations

License
----

GPL
