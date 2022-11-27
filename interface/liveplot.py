from pyqtgraph import PlotWidget, plot

class LivePlot(PlotWidget):
    def __init__(self, main_window):
        super().__init__()
        
        main_window.setCentralWidget(self)
        self.data_line = self.plot()