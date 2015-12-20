#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  pyautobright.py
#  
#  Copyright 2015 Unknown <everton@localhost.localdomain>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
# PIL, Pygame, os(xbacklight), 
import os,sys,configparser,subprocess,pygame,pygame.camera,numpy
from PIL import Image

ConfigDir="%s/.config/autobrighness" %(os.path.expanduser('~'))
print(ConfigDir)
Conffile="%s/config" %ConfigDir


CONFFILEGEN=False
try:
	os.stat(ConfigDir)
	try:
		os.stat(Conffile)
	except:
		CONFFILEGEN=True
except:
	os.mkdir(ConfigDir) 
	CONFFILEGEN=True
		
try:
	os.stat(Save)
	os.remove(Save)
except:
	pass
	
Configure = configparser.ConfigParser()
Configure.read(Conffile)

print(CONFFILEGEN)

try:
	Brilho_MIN=int(Configure["CONFIG"]["Minimum_Brightness"])
	Brilho_MAX=int(Configure["CONFIG"]["Maximum_Brightness"])
	MINMAXGEN=False
except:
	MINMAXGEN=True
	
def ConvertIntoList( str ):
	LST= str.split(",")
	LSTFloat= []
	for i in LST:
		LSTFloat.append(float(i.strip()))
	return(LSTFloat)
try:
	X=Configure["DoNotChange"]["X"]
	test=int(X[0]) #teste
	Y=Configure["DoNotChange"]["Y"]
	XList = ConvertIntoList(X)
	YList = ConvertIntoList(Y)
	CALIBRATIONGEN=False
except:
	CALIBRATIONGEN=True

if CALIBRATIONGEN is False and MINMAXGEN is False and CONFFILEGEN is False:
	pass
else:
	sys.path.insert(0, "%s" %ConfigDir)
	from configure import FirstRUN
	FirstRUN(CONFFILEGEN, MINMAXGEN, CALIBRATIONGEN)


TransitionTime=int(Configure["CONFIG"]["Transition"])
MODE=Configure["CONFIG"]["Mode"]
NumberOfPictures=int(Configure["CONFIG"]["NumberOfPictures"])
TimeBetweenPictures=int(Configure["CONFIG"]["TimeBetweenPictures"])
Deviece=Configure["CONFIG"]["Deviece"]

Save="%s/.current.jpg" %ConfigDir

#definir brilho minimo#




def CaptureImage( im_file ): #local da imagem, retorna porcentagem de brilho
	pygame.init()
	pygame.camera.init()
	cam = pygame.camera.Camera(Deviece, (640,480))
	cam.start()
	image = cam.get_image()
	cam.stop()
	pygame.image.save(image, im_file)
	from PIL import ImageStat
	im = Image.open(im_file).convert('L')
	stat = ImageStat.Stat(im)
	perc=int(stat.mean[0]*100/255)
	os.remove(im_file)
	return(perc)
	
def Captures( num_pic, Interval, Mode ):
	if num_pic == 1:
		return(CaptureImage(Save))
	elif num_pic > 1:
		import time
		value=[]
		for i in range(0,num_pic):
			value.append(CaptureImage(Save))
			print(value)
			time.sleep(Interval)
		if Mode == "precise":
			while numpy.array(value).std() > 2:
				if len(value) < (3+num_pic):
					print("kekeke")
					value.append(CaptureImage(Save))
					time.sleep(Interval)
				else:
					break
		return(numpy.median(numpy.array(value)))
	else:
		print("Must take at least one picture, check the config file")
		exit(1)

if len(sys.argv) == 2:
	if sys.argv[1] == "-c" or sys.argv[1] == "--calibrate":
		def AddtoEquation( new_coord, list_coord ):
			x= int(new_coord[0])
			y= int(new_coord[1])
			ListX = list_coord[0]
			ListY = list_coord[1]
			if x not in ListX:
				ListX.append(float(x))
				ListX.sort()
				SlotY= ListX.index(x)
				ListY.insert(SlotY, float(y))
			else:
				SlotY= ListX.index(x)
				OldY=ListY[SlotY]
				NewY=(OldY+y)/2
				ListY.pop(SlotY)
				ListY.insert(SlotY, float(NewY))
			return([ListX, ListY])		
			
		def getch():
			import tty, termios
			fd = sys.stdin.fileno()
			old_settings = termios.tcgetattr(fd)
			try:
				tty.setraw(fd)
				ch = sys.stdin.read(1)
			finally:
				termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
			return ch
		var=float(subprocess.check_output("xbacklight -get", shell=True))
		BKP=int(var)
		while True:
			subprocess.call("clear")
			print("Select a good brightness for the current light in your room (use + and - keys, then press y to confirm or n to exit)")
			Now="#"*int(var)
			Then="-"*(100-int(var))
			Perc="%.1f" %var
			print("["+Now+Then+"] ["+Perc+"%]")
		
			keypress=getch()
			if keypress == "+":
				subprocess.call("xbacklight -time 0 -inc 1", shell=True)
				var=float(subprocess.check_output("xbacklight -get", shell=True))
			elif keypress == "-":
				subprocess.call("xbacklight -time 0 -dec 1", shell=True)
				var=float(subprocess.check_output("xbacklight -get", shell=True))
			elif keypress == "y":
				break
			elif keypress == "n" or keypress == "q":
				subprocess.call("clear")
				print("Exiting without save")
				exit(0)
			else:
				pass
		Ycurrent=int(var)
		Xcurrent=Captures(3, 1, "precise")
		subprocess.check_output("xbacklight -set %i" %BKP, shell=True)
		ListSAVE= AddtoEquation( (Xcurrent,Ycurrent), (XList, YList))
		def SaveList( List, destvar, destfile ):
			File=""
			for i in List:
				File+=",%s" %int(i)
			print(File[1:])
			Configure.set("DoNotChange",destvar,File[1:])
			with open(destfile, 'w') as configfile:
				Configure.write(configfile)			
		SaveList(ListSAVE[0], "x", Conffile)
		SaveList(ListSAVE[1], "y", Conffile)
		exit(0)
			

def GetInterpolation( x, List):
	return(numpy.interp(x, List[0], List[1]))

BrightValue=GetInterpolation(Captures( NumberOfPictures, TimeBetweenPictures, MODE), (XList, YList))
print(BrightValue)

if BrightValue > Brilho_MAX:
	BrightValue=Brilho_MAX
elif BrightValue < Brilho_MIN:
	BrightValue=Brilho_MIN
subprocess.call("xbacklight -time %s -steps %s -set %i" %(TransitionTime,TransitionTime,int(round(BrightValue,0))), shell=True)
