import obspy
from obspy.signal.trigger import classic_sta_lta, plot_trigger, trigger_onset
import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import socketio
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import filedialog as fd
from tkinter import messagebox as mb

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

#---------------------#Interfaz------------------------------------------------
raiz=Tk()

raiz.title("RSADE-RT")
raiz.attributes('-zoomed', True)



#Se crea el frame
miFrame=Frame()

#se empaueta el frame y este se acomoda al tamano de la ventana
miFrame.pack(fill="both", expand="True")

top_frame = Frame(raiz)
top_frame.pack(side="top", fill="both", expand=True)
bottom_frame = Frame(raiz)
bottom_frame.pack(side="top", fill="both", expand=True)

#variable del nombre del archivo seleccionado
miArchivo=StringVar()



#-----------------------------Titulos----------------------
## Titulo de la lista desplegable
Label(miFrame, text="Algoritmo de Detección", font=(20)).grid(row=1, column=1, padx=10, pady=10)

## Titulo de parametros
parametrosTitle=Label(miFrame, text="Parámetros del Algoritmo", font=(20))

canalTitle=Label(miFrame, text="Canal:", font=(18))

nstaTitle=Label(miFrame, text="NSTA:", font=(18))
## Titulo de NLTA
nltaTitle=Label(miFrame, text="NLTA:", font=(18))
## Titulo de Triger On
triggerOnTitle=Label(miFrame, text="TRIGGER_ON:", font=(18))
## Titulo de Triger Off
triggerOffTitle=Label(miFrame, text="TRIGGER_OFF:", font=(18))
## Titulo de Ingresar hora inicio
hInicioTitle=Label(miFrame, text="Hora Inicio:", font=(18))
## Titulo de Ingresar hora fin
hFinTitle=Label(miFrame, text="Hora Fin:", font=(18))

## Titulo de factor de conversion
factorCTitle=Label(miFrame, text="Factor de conversión:", font=(18))

#-------------------------Imagenes--------------------------------------------
# Eventos
#miImagen = PhotoImage(file="p7.png")
#Label(miFrame, image=miImagen).grid(row=5, column=0, columnspan=7)

miImagen = PhotoImage(file="ucuenca.png")
imagen_sub = miImagen.subsample(4)
miImagen = imagen_sub
Label(miFrame, image=miImagen).grid(row=1, column=10, rowspan=4, padx=10, pady=50)


raiz.mainloop()



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