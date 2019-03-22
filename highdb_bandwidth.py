# -----------------------------------------------------------
# highdb_bandwidth.py
# Author: Matthew Sumpter
#
# Scans a .csv created by rtlsdr_scanner(https: // github.com/EarToEarOak/RTLSDR-Scanner)
#
# Records bandwidth of any signal spikes above specified range
#
# Requires two CL arguments - the start and end point of the scan.
# i.e. python highdb_bandwidth.py 90 95
# (to run script on a range from 90MHz to 95 MHz)
# -------------------------------------------------------------

import csv
import sys

filename = "rtlsdr_scan.csv"

# hold begin point and end point of full scan
scan_begin = float(sys.argv[1])
scan_end = float(sys.argv[2])

'''
These lists will hold information on any detected signal. i.e. for the first detected signal -> Signal detected from
start_freq[0] - end_freq[0], with the peak of the signal at peak_signal[0]
'''
start_freq = []   # each element will hold the first frequency where a signal was detected
end_freq = []     # each element will hold the last frequency where a signal was detected
peak_signal = []  # each element will hold the frequency at which the signal was the strongest

#### Calculate Signal Detection Threshold ####
total, count, max_sig = 0, 0, 0

with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    # collects data from .csv to determine limits of data
    for row in csv_reader:

        # skip first line, contains headers rather than information
        if count == 0:
            count += 1
            continue

        # assign first value as maximum signal (as a baseline)
        # max_sig will keep track of the maximum decibel power detected in the full scan
        if count == 1:
            max_sig = float(row[2])

        if max_sig < float(row[2]):
            max_sig = float(row[2])  # tracks most powerful signal detected

        # tracks the sum of every decibel reading in scan (later, used for averaging)
        total += float(row[2])
        count += 1

# determines "noise floor" by finding average of all data points
avg_noise = total / (count - 1)

# if maximum signal is greater than the average, assign threshold (at which we can say a signal was detected) to be 1/4 the difference
# between the max signal and the noise floor
# NOTE: would like to improve this by finding stastical significance of max_sig
if max_sig > avg_noise:
    threshold = avg_noise - ((avg_noise - max_sig) / 4)
else:
    threshold = 0

#### Detect signals in .csv, record start of signal, end of signal, maximum peak of signal ####
with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    # flag for signal detection. True when in a power spike, false when outside of power spike
    signal_detected = False
    # max_peak tracks FREQUENCY, max_peak_power tracks DB LEVEL @ max_peak
    max_peak, max_peak_power = 0, 0

    for row in csv_reader:

        # skip first line - contains headers
        if line_count == 0:
            line_count += 1
            continue

        frequency = float(row[1])
        signal_power = float(row[2])

        # records first frequency where signal power spikes
        if signal_power > threshold and not signal_detected:
            start_freq.append(frequency)
            max_peak = frequency
            max_peak_power = signal_power
            signal_detected = True

        # records frequency where signal spike ends
        if signal_power < threshold and signal_detected:
            end_freq.append(frequency)
            peak_signal.append(max_peak)
            signal_detected = False

        # keep track of frequency with highest power in signal
        if signal_detected and signal_power > max_peak_power:
            max_peak = frequency
            max_peak_power = signal_power

        line_count += 1


num_detected = 0  # tracks number of signals detected

### print results of scan ###
print('\n')

# print information for each signal detected
for freq in range(len(start_freq)):
    if (end_freq[freq] - start_freq[freq]) < .1:  # disregard random power spikes
        continue
    else:
        num_detected += 1
        print("Signal detected: " +
              str(start_freq[freq]) + '-' + str(end_freq[freq]) + "MHz")
        print("Signal peak: " + str(peak_signal[freq]))
        print("Bandwidth: ", (end_freq[freq] - start_freq[freq]) * 100, " kHz")
        print('\n')


# if no signals detected
if num_detected == 0:
    print("No signal detected in range " +
          str(scan_begin) + '-' + str(scan_end) + "MHz")
