from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import obspy
#import matplotlib
from obspy.signal.trigger import classic_sta_lta, plot_trigger, trigger_onset
import numpy as np
import socketio
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import multiprocessing
import time
import random
#from Tkinter import *

def conectarEvento():
    #se conecta al socket
    global f, a, b, line
    f = plt.Figure(figsize=(16, 8))
    a = f.add_subplot(211)
    dataFormat = [0]
    a.plot(dataFormat, 'k')
    #a.plot([1, 2 , 3], 'k')
    ymin, ymax = a.get_ylim()
    a.set_xlabel('Segundos [s]')
    b = f.add_subplot(212)
    dataFormat2 = [0]
    b.plot(dataFormat2, 'k')
    b.set_xlabel('Segundos [s]')
    b.axis('tight')
    plot()
    try:
        triggerOn   = triggerOnText.get()
        triggerOff  = triggerOffText.get()
        factorConversion = factorConversionText.get()
        nsta             = nstaText.get()
        nlta             = nltaText.get()
        if nsta=="" or nlta=="" or triggerOn=="" or triggerOff=="" or factorConversion=="":
            mb.showinfo("Información", "Debe ingresar los parámetros necesarios antes de Graficar")
        else:
            sio.connect('http://192.168.0.115:3000')

    except Exception:
            mb.showerror("Error", 'No se pudo conectar al servidor')

    

def desconectarEvento():
    #se conecta al socket
    try:
        sio.disconnect()
    except Exception:
            mb.showerror("Error", 'No se pudo desconectar del servidor')
            
def graficar(f):
    global canvas
    global toolbar
    #se intenta borrar la grafica en caso de que ya este dibujada en la interfaz
    #try:
        #canvas.get_tk_widget().pack_forget() # use the delete method here
        #toolbar.pack_forget()
    #except:
    #    pass
    
    
    canvas = FigureCanvasTkAgg(f, top_frame)
    
    canvas.get_tk_widget().pack(side="left", fill="both")
    canvas.draw()
    #raiz.after(500, graficar, f)

    toolbar = NavigationToolbar2Tk(canvas, bottom_frame)
    toolbar.update()
    canvas._tkcanvas.pack(side="left", fill="both")
    
def plot():
    global f,a,b,canvas, dataFormat
    canvas = FigureCanvasTkAgg(f, top_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side="left", fill="both")
    canvas._tkcanvas.pack(side="left", fill="both")

def updateplot():
    canvas.draw()
    
    
    
    

sio = socketio.Client()
global q
q = multiprocessing.Queue()

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
    #se obtienen los parametros ingresadors por el usuario
    triggerOn   = triggerOnText.get()
    triggerOff  = triggerOffText.get()
    factorConversion = factorConversionText.get()
    nsta             = nstaText.get()
    nlta             = nltaText.get()
    
    data_list = data['data']
    dataFormat = np.array(data_list)
    dataFormat = dataFormat/float(factorConversion)
    
    
    cft = classic_sta_lta(dataFormat, int(float(nsta) * data['sampling_rate']), int(float(nlta) * data['sampling_rate']))
    global line
    try:
        on_of = trigger_onset(cft, float(triggerOn), float(triggerOff))
        print(on_of)
        
        #plot()
        #raiz.after(500, updateplot, cft, on_of, dataFormat)
        #graficar(f)
        global a, b, f
        #f = plt.Figure(figsize=(16, 8))
        #a = f.add_subplot(211)
        a.clear()
        a.plot(dataFormat, 'k')
        ymin, ymax = a.get_ylim()
        a.vlines(on_of[:, 0], ymin, ymax, color='r', linewidth=2)
        a.vlines(on_of[:, 1], ymin, ymax, color='b', linewidth=2)
        #a.set_xlabel('Segundos [s]')
        #b = f.add_subplot(212)
        b.clear()
        b.plot(cft, 'k')
        b.hlines([float(triggerOn), float(triggerOff)], 0, len(cft), color=['r', 'b'], linestyle='--')
        #b.set_xlabel('Segundos [s]')
        #b.axis('tight')
        
        
        #raiz.after(500, graficar, f)
        
        raiz.after(500, updateplot)
        
    except Exception:
        print("Error")
        
    



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




#-----------------------------Titulos----------------------
## Titulo de la lista desplegable
Label(miFrame, text="Algoritmo de Detección", font=(20)).grid(row=1, column=1, padx=10, pady=10)

## Titulo de parametros
parametrosTitle=Label(miFrame, text="Parámetros del Algoritmo", font=(20))

#canalTitle=Label(miFrame, text="Canal:", font=(18))

nstaTitle=Label(miFrame, text="NSTA:", font=(18))
## Titulo de NLTA
nltaTitle=Label(miFrame, text="NLTA:", font=(18))
## Titulo de Triger On
triggerOnTitle=Label(miFrame, text="TRIGGER_ON:", font=(18))
## Titulo de Triger Off
triggerOffTitle=Label(miFrame, text="TRIGGER_OFF:", font=(18))
## Titulo de Ingresar hora inicio
#hInicioTitle=Label(miFrame, text="Hora Inicio:", font=(18))
## Titulo de Ingresar hora fin
#hFinTitle=Label(miFrame, text="Hora Fin:", font=(18))

## Titulo de factor de conversion
factorCTitle=Label(miFrame, text="Factor de conversión:", font=(18))

# ---------------Inputs-----------------------------

#input del canal
#canal=Entry(miFrame, width=10)


## data del archivo seleccionado
data=Label(miFrame, text="", font=(12))
data.grid(row=6, column=3, columnspan=7)

#global nstaText, nltaText, triggerOnText, triggerOffText, horaInicio, horaFin

nstaText=Entry(miFrame, width=10)
#nstaText.grid(row=2, column=3)

#NLTA input
nltaText=Entry(miFrame, width=10)
#nltaText.grid(row=2, column=5)

#Trigger On
triggerOnText=Entry(miFrame, width=10)
#triggerOnText.grid(row=3, column=3)

#Trigger Off
triggerOffText=Entry(miFrame, width=10)
#triggerOffText.grid(row=3, column=5)

#Hora Inicio
#horaInicio=Entry(miFrame, width=10)
#horaInicio.grid(row=2, column=7)

#Hora Fin
#horaFin=Entry(miFrame, width=10)
#horaFin.grid(row=3, column=7)

factorConversionText=Entry(miFrame, width=10)

#========================== Para emtros iniciales
nstaText.insert(0,'1')
nltaText.insert(0,'2')
triggerOnText.insert(0,'1.15')
triggerOffText.insert(0,'0.85')

#--------------------Botones----------------

# Boton para Seleccionar Archivo
conectarBtn = Button(miFrame, text="Conectar", command=conectarEvento, bg='#0D225F', fg="white", activebackground='#163aa2', activeforeground='white')
# Boton Graficar Eventos seleccionarArchivo
#graficarEventosBtn=Button(miFrame, text="Graficar Eventos", command=graficarEvento, bg='#0D225F', fg="white", activebackground='#163aa2', activeforeground='white')

# Boton Obtener Eventos
desconectarBtn=Button(miFrame, text="Desconectar", command=desconectarEvento, bg='#0D225F', fg="white", activebackground='#163aa2', activeforeground='white')

# Boton para extraer archivo miniSeed
#obtenerMiniSeedBtn=Button(miFrame, text="Obtener miniSeed", command=guardarMiniSeed , bg='#0D225F', fg="white", activebackground='#163aa2', activeforeground='white')


parametrosTitle.grid(row=1, column=2, padx=10, pady=10, columnspan=5)
        
## Titulo de NSTA
nstaTitle.grid(row=2, column=2, padx=10, pady=10)
## Titulo de NLTA
nltaTitle.grid(row=2, column=4, padx=10, pady=10)
## Titulo de Triger On
triggerOnTitle.grid(row=3, column=2, padx=10, pady=10)
## Titulo de Triger Off
triggerOffTitle.grid(row=3, column=4, padx=10, pady=10)
## Titulo de Ingresar hora inicio
#hInicioTitle.grid(row=2, column=8, padx=10, pady=10)
## Titulo de Ingresar hora fin
#hFinTitle.grid(row=3, column=8, padx=10, pady=10)

factorCTitle.grid(row=5, column=1, padx=10, pady=10)
factorConversionText.grid(row=5, column=2, padx=10, pady=10)



#NSTA input
#nstaText=Entry(miFrame)
nstaText.grid(row=2, column=3)

#NLTA input
#nltaText=Entry(miFrame)
nltaText.grid(row=2, column=5)

#Trigger On
#triggerOnText=Entry(miFrame)
triggerOnText.grid(row=3, column=3)

#Trigger Off
#triggerOffText=Entry(miFrame)
triggerOffText.grid(row=3, column=5)

#Hora Inicio
#horaInicio=Entry(miFrame)
#horaInicio.grid(row=2, column=9)

#Hora Fin
#horaFin=Entry(miFrame)
#horaFin.grid(row=3, column=9)

#canal
#canalTitle.grid(row=5, column=6)
#canal.grid(row=5, column=7)

#--------------------Botones----------------

# Boton para Seleccionar Archivo
conectarBtn.grid(row=4, column=1, padx=50, pady=10)
# Boton Graficar Eventos seleccionarArchivo
desconectarBtn.grid(row=4, column=3, padx=50, pady=10)

# Boton Obtener Eventos
#obtenerEventosBtn.grid(row=5, column=4, padx=50, pady=10)

# Boton para extraer archivo miniSeed
#obtenerMiniSeedBtn.grid(row=5, column=5, padx=50, pady=10)

#-------------------------Imagenes--------------------------------------------

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