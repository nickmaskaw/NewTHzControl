from pyqtgraph import PlotWidget, plot
from PyQt6.QtCore import pyqtSlot


class LivePlot(PlotWidget):
    def __init__(self):
        super().__init__()
        
        self.data_line = self.plot()

    @pyqtSlot()
    def update(self, x, y):
        self.data_line.setData(x=x, y=y)