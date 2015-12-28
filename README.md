# py-auto-brightness
PyAutoBrighyness is a very simple "Calise like" program, wrote in python 3, designed to change the screen brightness using the webcam as "light sensor".

# Installation
 ```
pip install pyautobrightnes
```
#Version
0.2 - added help and some arguments. Also some changes to add the package into pypi.  

0.1 - the first version is a mess, but It works. My only focus in this version was to get the math to work, and it does quite well 
##dependences##
  * Python Pygame 
  ```
  python-pygame-hg on Arch's AUR
  ```
   - it's used only oontrol the webcam.
   
  * Python Numpy 
  ```
  #pacman -S python-numpy on Arch's Extra
  ```
   - it's used to make statistical treatments to get a good and trusty result from various pictures values (the average brigtness of the pictures). It's also used to interpolate an equation based on the data the user recover from runing pyautobrightness --calibrate
   
  * Xorg Xbacklight 
  ```
  #pacman -S xorg-xbacklight on Arch's Extra
  ```
   - it's used to actually change the screen brightness.
   
#Instalation
- By the time being the instalation has to be manual. Copy configure.py to the folder /home/$USER/.config/autobrighness/. After that, run "py-auto-brightness.py" manually.
- In the first run you'll have to calibrate and enter some options, after this just run py-auto-brightness.py with no argument and the program will automatically set your brightmess (YEAH, CRONTAP IT BRO!)
- TIP: run py-auto-brightness.py --calibrate in various light conditions, the more you run it, the more data the program will have to better select a confy brightness value.

#Commented conf file

```python
[CONFIG]
Minimum_Brightness = 10
```
Possible values are positive numbers between 0 and 100. The software will never set the brightness for less than the stated in this option

```python
Maximum_Brightness = 90
```
Possible values are positive numbers between 0 and 100. The software will never set the brightness for more than the stated in this option

```python
Transition = 4000
```
Possible values are positive numbers. This set the transition time in xbacklight, 1000 is one second, try to not set it for more than 5 seconds


```python
NumberOfPictures= 2
```
Possible values are positive numbers. This option set how many pictures the software will take to measure the brightness, the more, the better, but less efficient. NumberOfPictures= 2 with Mode=precise is the better combination I tested

```python
TimeBetweenPictures= 1
```
Possible values are positible numbers only (0 is possible, but not recommended). This is the time between the pictures in seconds, if NumberOfPictures=1 this option is ignored.

```python
Mode= precise
```
Possible values are "precise and "normal". In precise mode pyautobrightness will try to get the better brightness by taking more pictures (if necessary) and giving it a statistical treatment. For security reasons, the Precise method will run up to 3 MORE times than the value set by the user in this file if it did met the estatistical requirements. In Normal mode it'll only take the number of pictures set by the user in NumberOfPictures.

```python
[DoNotChange]
x = 8.0,64.0
y = 55.0,98.0
```
Those are the the numbers that are stored when the user run this program with the --calibrate argument, they are used to interpolate an equation in the script with Numpy's help. The more, the better. Try to not change it manually, unless you know what you're doing. If the software is setting strange brightness you can run "pyautobrightness --calibrate reset" to clean all your calibrations

#TODO
-add the "odd" option to fix odd values in the stored calibrations
