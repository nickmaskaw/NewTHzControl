import sys
import numpy as np
import pandas as pd
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from interface import MainWindow, InstrumentWidgets, LivePlot, ExperimentWidgets
from instruments import VISAInstrument, LockIn, KBD101, OttimeDelayline, Cernox
from experiment import Parameters

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    
    lockin = LockIn()
    cernox = Cernox()
    thz_dl = KBD101("THz delay-line")
    pmp_dl = OttimeDelayline("Pump delay-line")
    instrument_widgets = InstrumentWidgets(lockin, cernox, pmp_dl, thz_dl)
    
    live_plot = LivePlot()
    
    parameters = Parameters()
    experiment_widgets = ExperimentWidgets(parameters)
    
    main_window.setInstrumentWidgets(instrument_widgets)
    main_window.setExperimentWidgets(experiment_widgets)
    main_window.setLivePlot(live_plot) 
    
    main_window.show()
    
    sys.exit(app.exec())