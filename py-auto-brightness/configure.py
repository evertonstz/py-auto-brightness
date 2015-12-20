#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  configure.py
#  
#  Copyright 2015 evertonstz
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



def FirstRUN( ConfFile, MinMax, FirstCalibration ):
	import os,sys,configparser,subprocess,pygame,pygame.camera,numpy
	from PIL import Image
	ConfigDir="%s/.config/autobrighness" %(os.path.expanduser('~'))
	Save="%s/.current.jpg" %ConfigDir
	Conffile="%s/config" %ConfigDir
	Configure = configparser.ConfigParser()
	if ConfFile is True: #criar arquivo de configuração
		Deviece="/dev/video0"
		ConfCreate = open(Conffile, 'w')
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
	else:
		Configure.read(Conffile)
		Deviece=Configure["CONFIG"]["Deviece"]
		
	def GetBRInput( Txt ):
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
		print("kek")
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
				
	if MinMax is True:
		Configure.read(Conffile)
		Brilho_MIN=int(GetBRInput("Select the MINIMUM brightness PyAutoBrightness should use (use + and - keys, then press y to confirm or n to exit)"))
		Configure.set("CONFIG","Minimum_Brightness",str(Brilho_MIN))
		subprocess.call("clear")
		print("Saving Minimum Brightness...")
		time.sleep(1)
		subprocess.call("clear")
		Brilho_MAX=int(GetBRInput("Select the MAXIMUM brightness PyAutoBrightness should use (use + and - keys, then press y to confirm or n to exit)"))
		Configure.set("CONFIG","Maximum_Brightness",str(Brilho_MAX))
		with open(Conffile, 'w') as configfile:
				Configure.write(configfile)
		print("Saving Maximum Brightness...")
		time.sleep(1)
	
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
						print("kekeke")
						value.append(CaptureImage(Save))
						time.sleep(Interval)
					else:
						break
			elif Mode == "normal":
				pass
			else:
				print("ERROR: invalid option for Mode, check your config file...")
				exit(1)
			return(numpy.median(numpy.array(value)))
		else:
			print("Must take at least one picture, check the config file")
			exit(1)
	
	if 	FirstCalibration == True:
		subprocess.call("clear")
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
			Configure.read(Conffile)
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
		with open(Conffile, 'w') as configfile:
				Configure.write(configfile)
	print("PyAutoBrightness sucessful calibrated! Try run pyautobrightness -c in various light conditions; the more you run it, the better PyAutoBrightness will get! Press any key to exit.")
	test=getch()
	exit(1)	
