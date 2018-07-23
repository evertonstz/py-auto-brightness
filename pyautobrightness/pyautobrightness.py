#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PIL, Pygame, os(xbacklight), numpy

#ARRUMAR ONDE TIRA FOTO E CONVERTE DEPOIS ARRUMAR O PRIMEIRA CONFIGURAÇÃO

import os,sys,subprocess,numpy,time,ConfigParser

if os.name == "nt":
	sClean = "cls"
else:
	sClean = "clear"
	import pygame, pygame.camera #don't think I need this

Configure = ConfigParser.ConfigParser()

ConfigDirRoot = "%s/.config/" %(os.path.expanduser('~'))
ConfigDir="%s/.config/autobrighness" %(os.path.expanduser('~'))
ConfigFile="%s/config" %ConfigDir
Save="%s/.current.jpg" %ConfigDir
	
Configure.read(ConfigFile)

try:
	X=Configure.get("DoNotChange","X")
	Y=Configure.get("DoNotChange","Y")
	if os.name != "nt":
		TransitionTime=int(Configure.get("CONFIG","Transition"))
	MODE=Configure.get("CONFIG","Mode")
	NumberOfPictures=int(Configure.get("CONFIG","NumberOfPictures"))
	TimeBetweenPictures=int(Configure.get("CONFIG","TimeBetweenPictures"))
	Deviece=Configure.get("CONFIG","Deviece")
except:
	pass

try:
	Brilho_MIN=int(Configure.get("CONFIG","Minimum_Brightness"))
	Brilho_MAX=int(Configure.get("CONFIG","Maximum_Brightness"))
except:
	pass

##from config

def TestIfConfExist():
	if os.path.isdir(ConfigDirRoot) is False:
		os.mkdir(ConfigDirRoot)
	if os.path.isdir(ConfigDir) is False:
		os.mkdir(ConfigDir)
		return(False)
	if os.path.isfile(ConfigFile) is False:
		return(False)
	return(True)

def TestIfMaxMinExist():
	try:
		Brilho_MIN=int(Configure.get("CONFIG","Minimum_Brightness"))
		Brilho_MAX=int(Configure.get("CONFIG","Maximum_Brightness"))
		return(True)
	except:
		return(False)

def CreateConfigFile():
		ConfCreate = open(ConfigFile, 'w')
		ConfCreate.write("[CONFIG]")
		ConfCreate.write("\n")
		if os.name == "nt":
			ConfCreate.write("Deviece = 0")
		else:
			ConfCreate.write("Deviece = /dev/video0")
		ConfCreate.write("\n")
		ConfCreate.write("Minimum_Brightness =")
		ConfCreate.write("\n")
		ConfCreate.write("Maximum_Brightness =")
		ConfCreate.write("\n")
		if os.name != "nt":
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
		print("Configuration created, run the program again to calibrate.")
		exit(0)

try:
	from msvcrt import getch
except ImportError:
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

def fWinReturnScreenBrightness():
	import wmi
	oC = wmi.WMI(namespace='wmi')
	oScreen = oC.WmiMonitorBrightness()[0]
	oScreen
	return(float(oScreen.CurrentBrightness))

def fWinIncDecScreenBright(A, Mod):
	if Mod == "Set":
		import wmi
		oC = wmi.WMI(namespace='wmi')
		oScreen = oC.WmiMonitorBrightnessMethods()[0]
		oScreen.WmiSetBrightness(A, 0)
	elif Mod == "Sub":
		import wmi
		oC = wmi.WMI(namespace='wmi')
		oScreen = oC.WmiMonitorBrightnessMethods()[0]
		fNewBright = fWinReturnScreenBrightness()+A
		if fNewBright >= 0 and fNewBright <=100:
			oScreen.WmiSetBrightness(fNewBright, 0)
		
def iRoundNumber(Num):
	Dec=int(Num/10)*10
	Unit = Num-Dec
	if Unit >= 0 and Unit <= 3:
		return(Dec+0)
	elif Unit > 3 and Unit < 7:
		return(Dec+5)
	else:
		return(Dec+10)

def sGetBrightnessInput( Txt ):
	if os.name == "nt":
		fVar=fWinReturnScreenBrightness()
	else:
		fVar=float(subprocess.check_output("xbacklight -get", shell=True))
	while True:
		os.system(sClean)
		print(Txt)
		Now="#"*int(fVar)
		Then="-"*(100-int(fVar))
		Perc="%.1f" %fVar
		print("["+Now+Then+"] ["+Perc+"%]")
		
		keypress=getch()

		if keypress == "+" or ord(keypress) == 43:
			if os.name == "nt":
				fWinIncDecScreenBright(10, "Sub")
				fVar = fWinReturnScreenBrightness()
			else:
				subprocess.call("xbacklight -time 0 -inc 1", shell=True)
				fVar=float(subprocess.check_output("xbacklight -get", shell=True))
		elif keypress == "-" or ord(keypress) == 45:
			if os.name == "nt":
				fWinIncDecScreenBright(-10, "Sub")
				fVar = fWinReturnScreenBrightness()
			else:
				subprocess.call("xbacklight -time 0 -dec 1", shell=True)
				fVar=float(subprocess.check_output("xbacklight -get", shell=True))
		elif keypress == "y" or ord(keypress) == 121:
			return(fVar)
		elif keypress == "n" or keypress == "q" or ord(keypress) == 110 or ord(keypress) == 113 or ord(keypress) == 27:
			os.system(sClean)
			print("Exiting without save...")
			exit(0)
		else:
			pass

def CreateMinMax():
	# Configure.read(ConfigFile)
	Brilho_MIN=int(sGetBrightnessInput("Select the MINIMUM brightness PyAutoBrightness should use (use + and - keys, then press y to confirm or n to exit)"))
	Configure.set("CONFIG","Minimum_Brightness",str(Brilho_MIN))
	os.system(sClean)
	print("Saving Minimum Brightness...")
	time.sleep(1)
	os.system(sClean)
	Brilho_MAX=int(sGetBrightnessInput("Select the MAXIMUM brightness PyAutoBrightness should use (use + and - keys, then press y to confirm or n to exit)"))
	Configure.set("CONFIG","Maximum_Brightness",str(Brilho_MAX))
	with open(ConfigFile, 'w') as configfile:
			Configure.write(configfile)
	print("Saving Maximum Brightness...")
	time.sleep(1)
	
def CaptureImage( im_file ): #local de salvamento, retorna porcentagem de brilho
	# try:
	# 	Deviece=Configure.get("CONFIG","Deviece")
	# except:
	# 	pass
	if os.name == "nt":
		import cv2
		from PIL import Image
		from PIL import ImageStat
		#take the pic from webcam
		cam = cv2.VideoCapture(int(Deviece))
		_,image = cam.read()
		image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
		image = Image.fromarray(image)
		#get the brightness
		stat = ImageStat.Stat(image)
		perc = int(stat.mean[0]*100/255)
		cam.release()
		perc = iRoundNumber(perc)
		return(perc)
	else:
		import pygame
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
		perc = iRoundNumber(perc)
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
		print("Must take at least one picture, check the configuration file.")
		exit(1)
	
def RunFirstCalibration():
	os.system(sClean)
	# Deviece=Configure.get("CONFIG","Deviece")
	print("Cover your webcam and press y, so PyAutoBrightness can see the minimum brightness value your webcam can capture and add it to the equation")
	while True:
		test=getch()
		if test == "Y" or test == "y" or ord(test) == 121 or test == 89:
			break
	MinX=CaptureImage(Save)
	try:
		test=int(Brilho_MIN)
		MinY=Brilho_MIN
	except:
		Configure.read(ConfigFile)
		MinY=float(Configure.get("CONFIG","Minimum_Brightness"))
	time.sleep(1)
	print("You can uncover it now!")
	MaxY=sGetBrightnessInput("Now go to the brightest place you can, set the screen brightness as you please and press Y (don't worry if you can't reach the brightest place you use your PC, you can calibrate PyAutoBrightness after for other values:")
	MaxX= Captures( 3, 1, "precise")
	print(MaxX,MaxY)
	X="%s,%s" %(str(int(round(MinX,0))), str(int(round(MaxX,0))))
	print(X)
	Y="%s,%s" %(str(int(round(MinY,0))), str(int(round(MaxY,0))))
	Configure.set("DoNotChange","x", X) 
	Configure.set("DoNotChange","y", Y)
	with open(ConfigFile, 'w') as configfile:
			Configure.write(configfile)
	print("PyAutoBrightness sucessful calibrated! Try run pyautobrightness -c in Various light conditions; the more you run it, the better PyAutoBrightness will get! Press any key to exit.")
	getch()

def ConvertIntoList( str ):
	LST= str.split(",")
	LSTFloat= []
	for i in LST:
		try:
			LSTFloat.append(int(i.strip()))
		except ValueError:
			print("""ERROR: no numbers in X Y, try to calibrate again.""")
			exit(1)
	return(LSTFloat)

def AddtoEquation( new_coord, list_coord ):
	"""this function takes new coordinates (x,y), and fit them inside the already current
	coordinates, that are saved in the config file. 
	RETURNS A LIST OF LISTS"""
	ListX = list_coord[0]
	ListY = list_coord[1]

	for i in range(0, len(ListX)):
		if ListX[i]%5 != 0:
			ListX[i] = iRoundNumber(ListX[i])
			
	x= iRoundNumber(float(new_coord[0]))
	y= float(new_coord[1])

	if x not in ListX:
		ListX.append(int(x))
		ListX.sort()
		SlotY = ListX.index(x)
		ListY.insert(SlotY, int(y))
	else:
		SlotY = ListX.index(x)
		OldY = ListY[SlotY]
		NewY = float((OldY+y)/2)
		ListY[SlotY] = int(NewY)
	return([ListX, ListY])

def Calibrate():
	XList = ConvertIntoList(X)
	YList = ConvertIntoList(Y)
	if os.name == "nt":
		fVar=fWinReturnScreenBrightness()
	else:
		fVar=float(subprocess.check_output("xbacklight -get", shell=True))
	while True:
		os.system(sClean)
		print("Select a good brightness for the current light in your room (use + and - keys, then press y to confirm or n to exit)")
		Now="#"*int(fVar)
		Then="-"*(100-int(fVar))
		Perc="%.1f" %fVar
		print("["+Now+Then+"] ["+Perc+"%]")
		keypress=getch()
		if keypress == "+" or ord(keypress) == 43:
			if os.name == "nt":
				fWinIncDecScreenBright(10, "Sub")
				fVar = fWinReturnScreenBrightness()
			else:
				subprocess.call("xbacklight -time 0 -inc 1", shell=True)
				fVar=float(subprocess.check_output("xbacklight -get", shell=True))
		elif keypress == "-" or ord(keypress) == 45:
			if os.name == "nt":
				fWinIncDecScreenBright(-10, "Sub")
				fVar = fWinReturnScreenBrightness()
			else:
				subprocess.call("xbacklight -time 0 -dec 1", shell=True)
				fVar=float(subprocess.check_output("xbacklight -get", shell=True))
		elif keypress == "y" or ord(keypress) == 121:
			Ycurrent=int(fVar)
			break
		elif keypress == "n" or keypress == "q" or ord(keypress) == 110 or ord(keypress) == 113:
			os.system(sClean)
			print("Exiting without save...")
			exit(0)
		else:
			pass
	Xcurrent=Captures(3, 1, "precise")
	ListSAVE= AddtoEquation( (Xcurrent,Ycurrent), (XList, YList))
	def SaveList( List, destfVar, destfile ):
		File=""
		for i in List:
			File+=",%s" %int(i)
		print(File[1:])
		Configure.set("DoNotChange",destfVar,File[1:])
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
	print(BrightValue)
	if os.name == "nt":
		fWinIncDecScreenBright(int(round(BrightValue,0)), "Set")
	else:
		subprocess.call("xbacklight -time %s -steps %s -set %i" %(TransitionTime,TransitionTime,int(round(BrightValue,0))), shell=True)