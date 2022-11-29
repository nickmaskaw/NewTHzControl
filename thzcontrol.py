import sys
import numpy as np
import pandas as pd
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from interface import MainWindow, LeftDockWidget, ConnectionContainer, ControlContainer, LivePlot
from instruments import VISAInstrument, KBD101, OttimeDelayline

def update():
    global liveplot, timer, i, t, X
    i += 1
    liveplot.data_line.setData(x=t[:i], y=X[:i])
    if i == len(t): timer.stop()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    lockin = VISAInstrument("Lock-in")
    cernox = VISAInstrument("Cernox")
    pmp_dl = OttimeDelayline("Pump delay-line")
    thz_dl = KBD101("THz delay-line")
    
    main_window = MainWindow()
    
    connection_widget = LeftDockWidget("Connection", main_window, ConnectionContainer(lockin, cernox, pmp_dl, thz_dl))
    control_widget    = LeftDockWidget("Manual Control", main_window, ControlContainer(pmp_dl, thz_dl))
    
    liveplot = LivePlot(main_window)
    
    data = pd.read_table("sample_signal.dat")
    t = data['t'].values
    X = data['X'].values
    
    i = 0
    
    timer = QTimer()
    timer.setInterval(50)
    timer.timeout.connect(update)
    timer.start()
    
    
    
    main_window.show()
    
    sys.exit(app.exec())