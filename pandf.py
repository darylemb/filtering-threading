import threading 
import alsaaudio
import queue
import numpy
from scipy import signal
import struct

N=170


#Datos

def LPfir(Q,cutoff_hz,nyq_rate_hz):
	Oc=numpy.pi*cutoff_hz/nyq_rate_hz
	m=numpy.linspace(0,Q,Q+1)-Q/2
	m=m+(numpy.equal(m,0)+0)*1e-16
	return (1/numpy.pi)*(1.0/m)*numpy.sin(Oc*m)

pilaEntrada=queue.Queue()
pilaSalida=queue.Queue()
fs=8000
fNyquist=fs/2
#edo=numpy.zeros(32)
#Designing filter
bLP=LPfir(32, 3400,fNyquist)
#Frquency behavior
f=numpy.arange(0,fNyquist,10)
w,h=signal.freqz(bLP,[1],numpy.pi*f/fNyquist)

#Grabadora de audio
#recorder=alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL,device='default') #en mi laptop 
recorder=alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL,device='sysdefault:CARD=1') # En su laptop
recorder.setchannels(1)
recorder.setrate(fs)
recorder.setformat(alsaaudio.PCM_FORMAT_S16_LE)
recorder.setperiodsize(N)

#Reproductor de audio
#player=alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, alsaaudio.PCM_NORMAL,device='default') #en mi laptop
player=alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, alsaaudio.PCM_NORMAL,device='sysdefault:CARD=1') # en su laptop
player.setchannels(1)
player.setrate(fs)
player.setformat(alsaaudio.PCM_FORMAT_S16_LE)
player.setperiodsize(N)

def Filtrado():
	edo=numpy.zeros(32)
	while pilaEntrada.qsize()<3:
		pass
	while True:
		
		strBuff= pilaEntrada.get()
		#buff=numpy.array(struct.unpack(N*'h',strBuff[3:]))
		buff=numpy.array(struct.unpack(N*'h',strBuff))
		audioFltr,edo=signal.lfilter(bLP,[1],buff,zi=edo) 
		audioFltr=audioFltr.astype(numpy.int16)		
		#strAudioFltr = 'pkg'+struct.pack(N*'h',*audioFltr)
		strAudioFltr = struct.pack(N*'h',*audioFltr)
		pilaSalida.put(strAudioFltr)			

def  Reproductor():
	while pilaSalida.qsize()<3:
		pass 
	while True:
		audio=pilaSalida.get()
		player.write(audio)

fifo1=threading.Thread(target=Reproductor)
fifo2=threading.Thread(target=Filtrado)
fifo1.start()
fifo2.start()

print ("Grabando...")
for k in range(1000):
	length,strBuff=recorder.read()
	pilaEntrada.put(strBuff)
print ("fin de grabacion")







