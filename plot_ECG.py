import pandas as pd
import pyqtgraph as pg
import sys
import numpy as np

pd.options.mode.chained_assignment = None

def plot_data():
    """Plotter Function

    This function plots the 3 axis accelerometer data in the same diagram for easy visualization.
    """
    df = pd.read_csv(open("C:\\Users\\aashi\\Downloads\\2021-08-10_07-08-26_200830001604_EcgActivityGraphView.csv", 'rb'))
    plt = pg.plot()
    plt.showGrid(x = True, y = True)
    plt.addLegend()
    plt.setLabel('left', 'Acceleration')
    plt.setLabel('bottom', 'Time')
    plt.setWindowTitle('ECG')
    line1 = plt.plot(df['Timestamp'], df["Count"], pen ='g', name ='X')
if __name__ == "__main__":
    plot_data()
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()
    
