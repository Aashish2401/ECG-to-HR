import pandas as pd
import pyqtgraph as pg
from pyqtgraph import QtCore
import sys
import easygui
import os

FILE_PATH = easygui.fileopenbox(msg="Choose a file", default="*.csv")

pd.options.mode.chained_assignment = None

peak_flag = False
trough_flag = False
false_beat = False
maxhr = 0
minhr = 300
avghr = 0
counter = 0
diff = 0
count = 0
fs = 128
age = 21
th_mhr = 210 - (0.65 * age)
fb1 = 0
beat1 = False
beat_plot = []
beat = False
true_beat = False
hr = 0
peak = 0
trough = 0
T1 = 0
T2 = 0

def HR_detector_v2(id, ecg_buff):
    global peak_flag, trough_flag, false_beat, maxhr, minhr, avghr, counter, diff, count, fb1, beat1, beat, true_beat, hr, peak, trough, T1, T2, beat_plot
    if not peak_flag:
        if ecg_buff[0] < ecg_buff[1] and ecg_buff[1] > ecg_buff[2]:
            peak_flag = True
            peak = ecg_buff[1]
    elif not trough_flag:
        if ecg_buff[0] > ecg_buff[1] and ecg_buff[1] < ecg_buff[2]:
            trough_flag = True
            trough = ecg_buff[1]
            diff = peak - trough
            beat = True
    elif beat:
        if diff > 1000 and diff < 8000:
              beat = False
              true_beat = True
              peak_flag = False
              peak = 0
              trough_flag = False
              trough = 0
        elif diff < 1000:
              hr = 0 # Belt removed
              rri = 0
              beat = False
              true_beat = False
              beat = False
              peak_flag = False
              peak = 0
              trough_flag = False
              trough = 0
        else:
            if false_beat:
                if (id - fb1) > 4:
                    hr = 1 # Belt contact issue
                    rri = 0
                    beat = False
                    true_beat = False
                    beat = False
                    peak_flag = False
                    peak = 0
                    trough_flag = False
                    trough = 0
                    false_beat = False
                else:
                    hr = 2 # Electrical interference
                    rri = 0
                    beat = False
                    true_beat = False
                    beat = False
                    peak_flag = False
                    peak = 0
                    trough_flag = False
                    trough = 0
                    false_beat = False
            else:
                fb1 = id
                beat = False
                true_beat = False
                beat = False
                peak_flag = False
                peak = 0
                trough_flag = False
                trough = 0
                false_beat = True
        if true_beat and not beat1:
            beat1 = True
            T1 = id
            true_beat = False
        elif beat1 and (id - T1) > (1.4 * fs):
            peak_flag = False
            trough_flag = False
            peak = 0
            trough = 0
            true_beat = False
            beat1 = False
        elif true_beat and beat1 and ((id - T1) > (0.3 * fs)):
            T2 = id
            rri = id - T1
            hr = ((rri * 60) / fs)
            if maxhr < hr:
                maxhr = hr
            if minhr > hr:
                minhr = hr
            if hr < 0.5 * th_mhr:
                zone = 1
            elif hr < 0.6 * th_mhr:
                zone = 2
            elif hr < 0.7 * th_mhr:
                zone = 3
            elif hr < 0.9 * th_mhr:
                zone = 4
            else:
                zone = 5
            avghr += hr
            counter += 1
            peak_flag = False
            trough_flag = False
            peak = 0
            trough = 0
            true_beat = False
            beat1 = False
            beat_plot.append(T1)
            beat_plot.append(T2)
        if true_beat and beat1 and ((id - T1) < (0.3 * fs)):
            peak_flag = False
            trough_flag = False
            peak = 0
            trough = 0
            true_beat = False
            beat1 = False
      
    return hr

def HR_detector(id, ecg_buff):
    global peak_flag, trough_flag, false_beat, maxhr, minhr, avghr, counter, diff, count, fb1, beat1, beat, true_beat, hr, peak, trough, T1, T2, beat_plot
    if not peak_flag:
        if ecg_buff[0] < ecg_buff[1] and ecg_buff[1] > ecg_buff[2]:
            peak_flag = True
            peak = ecg_buff[1]
    if peak_flag and not trough_flag:
        if ecg_buff[0] > ecg_buff[1] and ecg_buff[1] < ecg_buff[2]:
            trough_flag = True
            trough = ecg_buff[1]
            diff = peak - trough
            beat = True
    if diff > 1000 and diff < 8000 and beat:
        beat = False
        true_beat = True
        beat = False
        peak_flag = False
        peak = 0
        trough_flag = False
        trough = 0
    if diff < 1000 and beat:
        if count > 500:
            hr = 0 # Belt removed
            rri = 0
            count = 0
        else:
            count += 1
        beat = False
        true_beat = False
        beat = False
        peak_flag = False
        peak = 0
        trough_flag = False
        trough = 0
    if diff > 8000 and beat:
        if false_beat:
            if (id - fb1) > 4:
                hr = 1 # Belt contact issue
                rri = 0
                beat = False
                true_beat = False
                beat = False
                peak_flag = False
                peak = 0
                trough_flag = False
                trough = 0
                false_beat = False
            else:
                hr = 2 # Electrical interference
                rri = 0
                beat = False
                true_beat = False
                beat = False
                peak_flag = False
                peak = 0
                trough_flag = False
                trough = 0
                false_beat = False
        if not false_beat:
            fb1 = id
            beat = False
            true_beat = False
            beat = False
            peak_flag = False
            peak = 0
            trough_flag = False
            trough = 0
            false_beat = True
    if true_beat and not beat1:
        beat1 = True
        T1 = id
        true_beat = False
    if beat1 and (id - T1) > (1.4*fs):
        peak_flag = False
        trough_flag = False
        peak = 0
        trough = 0
        true_beat = False
        beat1 = False
    if true_beat and beat1 and ((id - T1) > (0.3 * fs)):
        T2 = id
        rri = id - T1
        hr = ((rri * 60) / fs)
        if maxhr < hr:
            maxhr = hr
        if minhr > hr:
            minhr = hr
        if hr < 0.5 * th_mhr:
            zone = 1
        elif hr < 0.6 * th_mhr:
            zone = 2
        elif hr < 0.7 * th_mhr:
            zone = 3
        elif hr < 0.9 * th_mhr:
            zone = 4
        else:
            zone = 5
        avghr += hr
        counter += 1
        peak_flag = False
        trough_flag = False
        peak = 0
        trough = 0
        true_beat = False
        beat1 = False
        beat_plot.append(T1)
        beat_plot.append(T2)
    if true_beat and beat1 and ((id - T1) < (0.3 * fs)):
        peak_flag = False
        trough_flag = False
        peak = 0
        trough = 0
        true_beat = False
        beat1 = False
    
    return hr
    

def plot_data():
    """Plotter Function

    This function plots the 3 axis accelerometer data in the same diagram for easy visualization.
    """
    global beat_plot
    df = pd.read_csv(open(FILE_PATH, 'rb'))
    index = []
    hr = []
    beat_plot = []
    for i in range(len(df) - 3):
        hr.append(HR_detector_v2(i, list(df['Count'][i:i+3])))
    hr_df = pd.DataFrame({'HR': hr})
    writer = pd.ExcelWriter(path = os.path.join(os.getcwd(), "output.xlsx"))
    hr_df.to_excel(writer)
    writer.save()
    plt = pg.plot()
    plt.showGrid(x = True, y = True)
    plt.addLegend()
    plt.setLabel('left', 'Acceleration')
    plt.setLabel('bottom', 'Time')
    plt.setWindowTitle('ECG')
    line1 = plt.plot(df['Timestamp'], df["Count"], pen ='g', name ='X')
    line2 = plt.plot([df['Timestamp'][i] for i in beat_plot], [0 for i in beat_plot], pen = None, symbol = 'o')

if __name__ == "__main__":
    plot_data()
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()
    
