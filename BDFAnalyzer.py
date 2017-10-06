#!/usr/bin/python
#===============================================================================
#
# Board Data File Analyzer
#
# Copyright (c) 2017 by QUALCOMM Atheros, Incorporated.
# All Rights Reserved
# QUALCOMM Atheros Confidential and Proprietary
#
# Notifications and licenses are retained for attribution purposes only
#===============================================================================


Description = """
[Description]:
Read WLAN board data file and generate graph per chain.
             1 2 3 4
fullmeas_pwr_0_G_0_0
fullmeas_pwr_0_A_0_0

1. Index/Step: a iteration takes 10 steps
2. Band: 'G' is 2.4G and 'A' is 5G.
3. Channel: 14 channels for 2.4G and 32 channels for 5G.
4. Chain: Either chain0 or chain1.

[Input]:
BIN/wlan_proc/wlan/halphy_tools/host/bdfUtil/qca61x0/bdf
[Usage]:
BDFAnalyzer.py input.txt
"""


fullpdadc_val_list = [] # y-axis
fullpwr_val_list = [] # x-axis
fullpwr_tag_list = [] 

def backup_calibration(fin):
	print "fullpwr_tag: "
	print len(fullpwr_tag_list)
	print "fullpwr_val: "
	print len(fullpwr_val_list)
	print "fullpdadc_val: "
	print len(fullpdadc_val_list)
	for index in range(len(fullpwr_tag_list)):
		fin.write(fullpwr_tag_list[index])
		fin.write(" ")
		fin.write(fullpwr_val_list[index])
		fin.write(",")
		fin.write(fullpdadc_val_list[index])
		fin.write("\n")


def main():
	global fullpwr_tag_list, fullpwr_val_list, fullpdadc_val_list
	clpc = open("files/calibration.txt","w")
	bdf = open("files/bdwlan30.txt",'r')
	# read data
	for line in bdf:
		if "fullpdadc" in line:
			tmp = line.split()
			fullpdadc_val_list.append(tmp[1])
		if "fullmeas_pwr" in line:
			tmp = line.split()
			fullpwr_tag_list.append(tmp[0])
			fullpwr_val_list.append(tmp[1])

	# write calibration backup file
	backup_calibration(clpc)
	bdf.close()
	clpc.close()

main()
#import numpy as np1
#import pyqtgraph as pg1
#
#data = np1.random.normal(size=1000)
#pg1.plot(data, title="Simplest possible plotting example")
#
#data = np1.random.normal(size=(500,500))
#pg1.image(data, title="Simplest possible image example")
#
#
### Start Qt event loop unless running in interactive mode or using pyside.
#if __name__ == '__main__':
#    import sys
#    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
#        pg1.QtGui.QApplication.exec_()
