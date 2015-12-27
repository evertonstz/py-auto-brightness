#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PIL, Pygame, os(xbacklight), numpy

import os,sys,configparser,subprocess,pygame,pygame.camera,numpy,time
from PIL import Image

ConfigDir="%s/.config/autobrighness" %(os.path.expanduser('~'))
ConfigFile="%s/config" %ConfigDir
Save="%s/.current.jpg" %ConfigDir
	
Configure = configparser.ConfigParser()
Configure.read(ConfigFile)

try:
	X=Configure["DoNotChange"]["X"]
	Y=Configure["DoNotChange"]["Y"]
	TransitionTime=int(Configure["CONFIG"]["Transition"])
	MODE=Configure["CONFIG"]["Mode"]
	NumberOfPictures=int(Configure["CONFIG"]["NumberOfPictures"])
	TimeBetweenPictures=int(Configure["CONFIG"]["TimeBetweenPictures"])
	Deviece=Configure["CONFIG"]["Deviece"]
except:
	pass

try:
	Brilho_MIN=int(Configure["CONFIG"]["Minimum_Brightness"])
	Brilho_MAX=int(Configure["CONFIG"]["Maximum_Brightness"])
except:
	pass


##from config

def TestIfConfExist():
	try:
		os.stat(ConfigDir)
		try:
			os.stat(ConfigFile)
		except:
			return(False)
		return(True)
	except:
		os.mkdir(ConfigDir) 
		return(False)

def TestIfMaxMinExist():
	try:
		Brilho_MIN=int(Configure["CONFIG"]["Minimum_Brightness"])
		Brilho_MAX=int(Configure["CONFIG"]["Maximum_Brightness"])
		return(True)
	except:
		return(False)

def CreateConfigFile():
		ConfCreate = open(ConfigFile, 'w')
		ConfCreate.write("[CONFIG]")
		ConfCreate.write("\n")
		ConfCreate.write("Deviece = /dev/video0")
		ConfCreate.write("\n")
		ConfCreate.write("Minimum_Brightness =")
		ConfCreate.write("\n")
		ConfCreate.write("Maximum_Brightness =")
		ConfCreate.write("\n")
		ConfCreate.write("Transition = 4000")
		ConfCreate.write("\n")
		ConfCreate.write("numberofpictures = 2")
		ConfCreate.write("\n")
		ConfCreate.write("timebetweenpictures = 1")
		ConfCreate.write("\n")
		ConfCreate.write("mode = precise")
		ConfCreate.write("\n")
		ConfCreate.write("\n")
		ConfCreate.write("[DoNotChange]")
		ConfCreate.write("\n")
		ConfCreate.write("x =")
		ConfCreate.write("\n")
		ConfCreate.write("y =")
		ConfCreate.write("\n")
		ConfCreate.close()

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

def GetBRInput( Txt ):
	var=float(subprocess.check_output("xbacklight -get", shell=True))
	while True:
		subprocess.call("clear")
		print(Txt)
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
			return(var)
		elif keypress == "n" or keypress == "q":
			subprocess.call("clear")
			print("Exiting without save...")
			exit(0)
		else:
			pass

def CreateMinMax():
	Configure.read(ConfigFile)
	Brilho_MIN=int(GetBRInput("Select the MINIMUM brightness PyAutoBrightness should use (use + and - keys, then press y to confirm or n to exit)"))
	Configure.set("CONFIG","Minimum_Brightness",str(Brilho_MIN))
	subprocess.call("clear")
	print("Saving Minimum Brightness...")
	time.sleep(1)
	subprocess.call("clear")
	Brilho_MAX=int(GetBRInput("Select the MAXIMUM brightness PyAutoBrightness should use (use + and - keys, then press y to confirm or n to exit)"))
	Configure.set("CONFIG","Maximum_Brightness",str(Brilho_MAX))
	with open(ConfigFile, 'w') as configfile:
			Configure.write(configfile)
	print("Saving Maximum Brightness...")
	time.sleep(1)
	
def CaptureImage( im_file ): #local de salvamento, retorna porcentagem de brilho
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
		import numpy
		for i in range(0,num_pic):
			value.append(CaptureImage(Save))
			print(value)
			time.sleep(Interval)
		if Mode == "precise":
			while numpy.array(value).std() > 2:
				if len(value) < (3+num_pic):
					value.append(CaptureImage(Save))
					time.sleep(Interval)
				else:
					break
		elif Mode == "normal":
			pass
		else:
			print("ERROR: invalid option for Mode, check your config file...")
			exit(1)
		if numpy.array(value).std() > 10:
			print("Error while calibrating, too much brightness variation in this ambient. Try again.")
			exit(1)
		else:
			return(numpy.median(numpy.array(value)))
	else:
		print("Must take at least one picture, check the config file")
		exit(1)
	
def RunFirstCalibration():
	subprocess.call("clear")
	Deviece=Configure["CONFIG"]["Deviece"]
	print("Cover your webcam and press y, so PyAutoBrightness can see the minimum brightness value your webcam can capture and add it to the equation")
	while True:
		test=getch()
		if test == "Y" or test == "y":
			break
	MinX=CaptureImage(Save)
	try:
		test=int(Brilho_MIN)
		MinY=Brilho_MIN
	except:
		Configure.read(ConfigFile)
		MinY=int(Configure["CONFIG"]["Minimum_Brightness"])
	time.sleep(2)
	print("You can uncover it now!")
	MaxY=GetBRInput("Now go to the brightest place you can, set the screen brightness as you please and press Y (don't worry if you can't reach the brightest place you use your PC, you can calibrate PyAutoBrightness after for other values:")
	MaxX= Captures( 3, 1, "precise")
	X="%s,%s" %(str(int(round(MinX,0))), str(int(round(MaxX,0))))
	print(X)
	Y="%s,%s" %(str(int(round(MinY,0))), str(int(round(MaxY,0))))
	Configure.set("DoNotChange","x", X) 
	Configure.set("DoNotChange","y", Y)
	with open(ConfigFile, 'w') as configfile:
			Configure.write(configfile)
	print("PyAutoBrightness sucessful calibrated! Try run pyautobrightness -c in various light conditions; the more you run it, the better PyAutoBrightness will get! Press any key to exit.")
	getch()

def ConvertIntoList( str ):
	LST= str.split(",")
	LSTFloat= []
	for i in LST:
		try:
			LSTFloat.append(float(i.strip()))
		except ValueError:
			print("""ERROR: no numbers in X Y, try to calibrate again.""")
			exit(1)
	return(LSTFloat)

#calibrate

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

def Calibrate():
	XList = ConvertIntoList(X)
	YList = ConvertIntoList(Y)
	var=float(subprocess.check_output("xbacklight -get", shell=True))
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
			Ycurrent=int(var)
			break
		elif keypress == "n" or keypress == "q":
			subprocess.call("clear")
			print("Exiting without save...")
			exit(0)
		else:
			pass
	Xcurrent=Captures(3, 1, "precise")
	ListSAVE= AddtoEquation( (Xcurrent,Ycurrent), (XList, YList))
	def SaveList( List, destvar, destfile ):
		File=""
		for i in List:
			File+=",%s" %int(i)
		print(File[1:])
		Configure.set("DoNotChange",destvar,File[1:])
		with open(destfile, 'w') as configfile:
			Configure.write(configfile)			
	SaveList(ListSAVE[0], "x", ConfigFile)
	SaveList(ListSAVE[1], "y", ConfigFile)
	exit(0)

def RUN():
	XList = ConvertIntoList(X)
	YList = ConvertIntoList(Y)
	def GetInterpolation( x, List):
		return(numpy.interp(x, List[0], List[1]))
	BrightValue=GetInterpolation(Captures( NumberOfPictures, TimeBetweenPictures, MODE), (XList, YList))
	if BrightValue > Brilho_MAX:
		BrightValue=Brilho_MAX
	elif BrightValue < Brilho_MIN:
		BrightValue=Brilho_MIN
	subprocess.call("xbacklight -time %s -steps %s -set %i" %(TransitionTime,TransitionTime,int(round(BrightValue,0))), shell=True)