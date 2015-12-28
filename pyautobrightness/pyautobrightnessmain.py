#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse, sys, os

from pyautobrightness.pyautobrightness import *


if TestIfConfExist() is False:
	CreateConfigFile()

if TestIfMaxMinExist() is False:
	CreateMinMax()

def TestFirstRun():
	try:
		if X is "" or Y is "":
			raise()
	except:
		RunFirstCalibration()
TestFirstRun()


def main():
	parser = argparse.ArgumentParser(description='PyAutoBrighyness is a very simple "Calise like" program, wrote in python 3 and designed to change the screen brightness using the webcam as a "light sensor".')
	
	parser.add_argument('--calibrate', '-c', metavar="N", nargs='?', help='Run this argument to calibrate PyAutoBrighyness. Try to run it in multiple light conditions, the more you run it, the better the software will perform;: "--calibrate rm" to remove all stored calibrations and start a new one "--calibrate odd" to try to fix odd values automatically "--calibrate mm" to reenter minimum and maximum brightness')

	args = parser.parse_args()

	#>>>testar se há config file

	if len(sys.argv) > 1:
		if args.calibrate is None:
			###rodar função de calibração
			Calibrate()
			exit(0)
		elif args.calibrate == "rm":
			RunFirstCalibration()
			exit(0)
		elif args.calibrate == "odd":
			print("run odd values function") #TODO
			exit(0)
			#run odd values function#
		elif args.calibrate == "mm":
			CreateMinMax()
		else:
			print("ERROR: invalid argument for -c")
			exit(1)
	else: #acertar o brilho
		RUN()
	
if __name__ == '__main__':
    import sys
    sys.exit(main())