"""
Taylor Seale & Iheanyi Ekechukwu
Programming Paradigms
Final Project - Audite

Music Streaming App using PyQt and CherryPy
"""

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Form(QDialog):
	def __init__(self, parent=None):
		super(Form, self).__init__(parent)

		# create all the widget objects
		self.menubar = QMenuBar() 
		
		# set the widgets into the layout
		mainlayout = QVBoxLayout()

		# create the layout
		self.setLayout(mainlayout)
		self.setWindowTitle("Audite")

# show and execute the gui application
app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()