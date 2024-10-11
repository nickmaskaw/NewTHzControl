import sys
import numpy as np
import pandas as pd
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QThreadPool, QRunnable, pyqtSlot
from interface import MainWindow, InstrumentWidget, ParametersWidget, LivePlot
from instruments import VISAInstrument, LockIn, KBD101, OttimeDelayline_foo, Cernox
from experiment import Parameters, Measurement


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # tools:
    lockin      = LockIn()
    cernox      = Cernox()
    thz_dl      = KBD101("THz delay-line")
    pmp_dl      = OttimeDelayline_foo("Pump delay-line")
    parameters  = Parameters(lockin, cernox)
    measurement = Measurement(parameters, lockin, cernox, thz_dl, pmp_dl)
    thread_pool = QThreadPool()
    
    # widgets:
    liveplot_widget   = LivePlot()
    instrument_widget = InstrumentWidget(lockin, cernox, thz_dl, pmp_dl)
    parameters_widget = ParametersWidget(parameters)
    
    # connect slots:
    parameters_widget.set_button.toggled.connect(lambda state: instrument_widget.setPagesEnabled(not state))
    parameters_widget.start_button.clicked.connect(lambda: measurement.run())
    parameters_widget.stop_button.clicked.connect(lambda: measurement.setBreak(True))
    measurement.signals.updated.connect(lambda x, y: liveplot_widget.update(x, y))
    measurement.signals.finished.connect(lambda: parameters_widget.set_button.setChecked(False))
    
    # main window:
    main_window = MainWindow()
    main_window.setLivePlot(liveplot_widget) 
    main_window.setInstrumentWidget(instrument_widget)
    main_window.setParametersWidget(parameters_widget)
    
    main_window.show()
    
    sys.exit(app.exec())