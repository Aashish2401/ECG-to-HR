import pandas as pd
import numpy as np
import easygui
import pyqtgraph as pg
import sys
from pyqtgraph import QtCore

FS = 200
N = int(FS / 10)

def read_from_csv():
    path = easygui.fileopenbox(msg="Choose a file", default="*.csv")
    ECG_df = pd.read_csv(open(path, 'rb'))
    return ECG_df

def QRS_detection(ECG_df):
    global FS, N
    low_pass = []
    high_pass = []
    derivative = []
    square = []
    integration = []
    for i in range(len(ECG_df) - 12):
        if len(low_pass) < 1:
            low_pass.append(ECG_df['Count'][i + 12] - (2 * ECG_df['Count'][i + 6]) + ECG_df['Count'][i])
        elif len(low_pass) < 2:
            low_pass.append((2 * low_pass[0]) + ECG_df['Count'][i + 12] - (2 * ECG_df['Count'][i + 6]) + ECG_df['Count'][i])
        else:
            low_pass.append((2 * low_pass[i - 1]) - low_pass[i - 2] + ECG_df['Count'][i + 12] - (2 * ECG_df['Count'][i + 6]) + ECG_df['Count'][i])
    for i in range(len(low_pass) - 32):
        if len(high_pass) < 1:
            high_pass.append((32 * low_pass[i + 16]) - (low_pass[i + 32] - low_pass[i]))
        else:
            high_pass.append((32 * low_pass[i + 16]) - (high_pass[i - 1] + low_pass[i + 32] - low_pass[i]))
    for i in range(2, len(high_pass) - 2):
        derivative.append((FS / 8) * (-high_pass[i - 2] - (2 * high_pass[i - 1]) +(2 * high_pass[i + 1]) + high_pass[i + 2]))
        square.append(derivative[i - 2] ** 2)
    integration.append(0)
    for i in range(N, len(square)):
        integration.append((1 / N) * (sum(square[i-N:i])))
    return low_pass, high_pass, derivative, square, integration

def plotter(line, line1, line2, line3, line4, line5):
    plt = pg.plot()
    plt.showGrid(x = True, y = True)
    plt.addLegend()
    plt.setLabel('left', 'Amplitude')
    plt.setLabel('bottom', 'Index')
    plt.setWindowTitle('ECG')
    plt.plot(line, pen ='g', name ='Amplitude')
    plt1 = pg.plot()
    plt1.showGrid(x = True, y = True)
    plt1.addLegend()
    plt1.setLabel('left', 'Amplitude')
    plt1.setLabel('bottom', 'Index')
    plt1.setWindowTitle('Low Pass')
    plt1.plot(line1, pen ='r', name ='Amplitude')
    plt2 = pg.plot()
    plt2.showGrid(x = True, y = True)
    plt2.addLegend()
    plt2.setLabel('left', 'Amplitude')
    plt2.setLabel('bottom', 'Index')
    plt2.setWindowTitle('Band Pass')
    plt2.plot(line2, pen ='y', name ='Amplitude')
    plt3 = pg.plot()
    plt3.showGrid(x = True, y = True)
    plt3.addLegend()
    plt3.setLabel('left', 'Amplitude')
    plt3.setLabel('bottom', 'Index')
    plt3.setWindowTitle('Derivative')
    plt3.plot(line3, pen ='b', name ='Amplitude')
    plt4 = pg.plot()
    plt4.showGrid(x = True, y = True)
    plt4.addLegend()
    plt4.setLabel('left', 'Amplitude')
    plt4.setLabel('bottom', 'Index')
    plt4.setWindowTitle('Square')
    plt4.plot(line4, pen ='w', name ='Amplitude')
    plt5 = pg.plot()
    plt5.showGrid(x = True, y = True)
    plt5.addLegend()
    plt5.setLabel('left', 'Amplitude')
    plt5.setLabel('bottom', 'Index')
    plt5.setWindowTitle('Integral')
    plt5.plot(line5, pen ='g', name ='Amplitude')

if __name__ == "__main__":
    df = read_from_csv()
    low_pass, high_pass, derivative, square, integral = QRS_detection(df)
    plotter(df['Count'], low_pass, high_pass, derivative, square, integral)
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()