#!/usr/bin/env python

from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import sys
import scipy
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):

    def __init__(self):
        """
        This function initializes the figure.
        """
        self.fig = Figure()
        self.picture = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)

class matplotlibWidget(QtGui.QWidget):

    def __init__(self, parent = None):
        """
        This function initializes the place where the figure will be display.
        """
        QtGui.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)