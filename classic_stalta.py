import obspy
from obspy.signal.trigger import classic_sta_lta, plot_trigger, trigger_onset
import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('Im connected')
    sio.emit('event', 'Hola desde python')

@sio.event
def connect_error(data):
    print('Error')

@sio.on('new-event')
def new_data(data):
    print('hanshake')
    cft = classic_sta_lta(data['data'], int(1 * data['sampling_rate']), int(7 * data['sampling_rate']))
    on_of = trigger_onset(cft, 1.15, 0.5)
    print(on_of)
    f = plt.Figure(figsize=(16, 8))
    a = f.add_subplot(211)
    #ax = a.subplot(211)
    a.plot(data['data'], 'k')
    ymin, ymax = a.get_ylim()
    #a.set_xticklabels(segundos+a.get_xticks()/64)
    a.vlines(on_of[:, 0], ymin, ymax, color='r', linewidth=2)
    a.vlines(on_of[:, 1], ymin, ymax, color='b', linewidth=2)
    #x1=p_pick+segundos
    #x2=s_pick+segundos
    a.set_xlabel('Segundos [s]')

sio.connect('http://192.168.0.115:3000')



#st = obspy.read("200428000000-CH0.mseed")[0]

#t = st.stats.starttime
#t1 = t + 3600 * 13
#t1 = t
#t2 = t + 3600 * 13
#t2 = st.stats.endtime
#trace = st.trim(t1,t2)
#trace = st
#print(trace.data)
#trace.data = trace.data/6553.6
#print(trace.data)
#trace.filter('bandpass', freqmin = 5, freqmax = 20)
#df = trace.stats.sampling_rate

#cft = classic_sta_lta(trace.data, int(10 * df), int(70 * df))
#on_of = trigger_onset(cft, 1.15, 0.5)
#print(trace.stats)
#print(trace.data)
#print(on_of)
#np.savetxt("eventosp10.txt", on_of)
#plot_trigger(trace, cft, 1.15, 0.5)