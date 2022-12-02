import sys
import numpy as np
import pandas as pd
from PyQt6.QtWidgets import QApplication
from interface import MainWindow, InstrumentWidget, ParametersWidget, LivePlot
from instruments import VISAInstrument, LockIn, KBD101, OttimeDelayline, Cernox
from experiment import Parameters

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # tools:
    lockin     = LockIn()
    cernox     = Cernox()
    thz_dl     = KBD101("THz delay-line")
    pmp_dl     = OttimeDelayline("Pump delay-line")
    parameters = Parameters()
    
    # widgets:
    live_plot         = LivePlot()
    instrument_widget = InstrumentWidget(lockin, cernox, thz_dl, pmp_dl)
    parameters_widget = ParametersWidget(parameters)
    
    # some slots configurations:
    parameters_widget.control_page.set_button.toggled.connect(lambda state: instrument_widget.setEnabled(not state))
    
    # main window:
    main_window = MainWindow()
    main_window.setLivePlot(live_plot) 
    main_window.setInstrumentWidget(instrument_widget)
    main_window.setParametersWidget(parameters_widget)
    
    main_window.show()
    
    sys.exit(app.exec())