from pyqtgraph import PlotWidget, plot


class LivePlot(PlotWidget):
    def __init__(self):
        super().__init__()
        
        self._data_line = self.plot()
        
    @property
    def data_line(self): return self._data_line
        
    def update(self, x, y):
        self.data_line.setData(x=x, y=y)