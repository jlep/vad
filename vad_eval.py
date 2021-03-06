import csv
from subprocess import call
import librosa
import numpy as np
import math
import speech_processing as sp

try:
    try:
        import scikits.audiolab as al
    except ImportError:
        import audiolab as al
except ImportError:
    al = None
    print("Warning: scikits.audiolab not found! Using scipy.io.wavfile")
    from scipy.io import wavfile

def main(signalcsv, noisecsv, snrcsv, algorithmscsv, samplerate, tmppath, resultcsv):
    """
    combine signals and noises with all SNRs and write audio output to tmppath
    with given samplerate
    labels from signalcsv
    write to tmppath/signalname_noisename_+-SNR.flac
    call algorithm from algorithm.csv
    which writes to predictiondir/algoname_signalname_noisename_+-SNR.txt
    """
    signal_list = readcsv(signalcsv, True)
    noise_list = readcsv(noisecsv)
    snrlist = readcsv(snrcsv)
    try:
        snrlist = [float(x) for x in snrlist]
    except ValueError:
        print("Failed reading SNR definitions as float-values")
    algorithms = readcsv(algorithmcsv, True)
    combine(signal_list, noise_list, snrlist, soundpath)

def read_soundfile(filename):
        soundfile = al.Sndfile(filename, 'r')
        signal = soundfile.read_frames(soundfile.nframes)
        if soundfile.channels == 1:
            return signal, soundfile.samplerate
        else:
            return signal[:,0], soundfile.samplerate

""" Read vad csv-files """
def readcsv(filename, has_lists=False, delimiter=" "):
    res = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        for row in reader:
            if has_lists == False:
                res.append(row[0])
            else:
                res.append(row)
    return res

def predict(comb_files, labels, algos):
    #["matlab", "g279.m" "combined_list.txt", prediction_dir]
    for alg in algos:
        call(alg)

def evaluate(predicted_path, truthpath, resultpath):
    """ """

def g279(combined_files, prediction_dir):
    """" call matlab g279.m """
    """ store labels to csvfile"""
    pass

def txt2list(path):
    pass

def load_truths(paths=None):
    """ Returns combined truth values in a dictionary
    For example:
    {"s":[[voice-starttime, endtime],...],
     "g":[[voice-starttime, endtime],...]}"""
    if paths == None:
        paths = ['s/si.txt', 's/sj.txt', 'g/gi.txt', 'g/gj.txt']
    data = {}
    for fn in paths:
        segments = ad.read_segment_file(fn)
        identity = fn[2:4]
        scenario = identity[0]
        if scenario not in data: data[scenario] = {}
        data[scenario][identity] = segments
    for scene_id, scenario in data.iteritems():
        combined = []
        for segments in scenario.values():
            combined = combined+segments
        combined = sorted(combined)
        scenario['combined'] = combined
    return data

def segments_to_indexes(segments):
    indexes = []
    for s in segments:
        indexes.append([s[0], "start"])
        indexes.append([s[1], "end"])
    return sorted(indexes)

#if __name__ == "__main__":
#    if len(argv == n):
#        main(argv*)
