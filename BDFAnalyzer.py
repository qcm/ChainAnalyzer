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

#--------------
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from array import array
import numpy as np

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

win = pg.GraphicsWindow(title="Chain Analyzer: chain 0 (RED) chain 1 (GREEN)")
win.resize(1000,600)
def backup_calibration(fin):
	for index in range(len(fullpwr_tag_list)):
		fin.write(fullpwr_tag_list[index])
		fin.write(" ")
		fin.write(fullpwr_val_list[index])
		fin.write(",")
		fin.write(fullpdadc_val_list[index])
		fin.write("\n")

def plot_render(band, channel):
	index_lower = 0
	index_upper = 0
	X = []
	Y = []
	if band == "G": # 2.4G
		index_lower = channel * 20
		index_upper = (channel+1) * 20 
	elif band == "A": # 5G
		index_lower = 280 + channel * 20
		index_upper = 280 + (channel+1) * 20 
	else:
		print "Plot render error\n"
	
	for i in range(index_lower, index_upper):
		X.append(int(fullpwr_val_list[i], 10))
		Y.append(int(fullpdadc_val_list[i], 10))

	title_description = "Channel " + str(channel)
	pp = win.addPlot(title = title_description)
	pp.plot(X[0:10],Y[0:10], title="Chain 0", pen=(255,0,0)) # chain 0 as red line
	pp.plot(X[10:20],Y[10:20], title="Chain 1", pen=(0,255,0)) # chain 1 as green line
	pp.showGrid(x=True, y=True)
		

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
	# draw plot
	plot_render('A', 7)
	plot_render('A', 8)
	win.nextRow()
	plot_render('A', 9)
	plot_render('A', 10)
	if __name__ == '__main__':
		import sys
		if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
			QtGui.QApplication.exec_()

main()
