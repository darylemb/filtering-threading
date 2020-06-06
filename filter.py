from matplotlib import pyplot
import numpy
from scipy import signal

def LPfir (Q,cutoff_hz,nyq_rate_hz):
    Oc = numpy.pi*cutoff_hz/nyq_rate_hz
    m = numpy.linspace(0,Q,Q+1)-Q/2
    m = m+(numpy.equal(m,0)+0)*1e-16
    return (1/numpy.pi)*(1.0/m)*numpy.sin(Oc*m)

fs= 8000
fNyquist = fs/2
bLP = LPfir(32,3400,fNyquist)

f=numpy.arange(0,fNyquist,10)
w,h = signal.freqz(bLP,[1],numpy.pi*f/fNyquist)
abs = numpy.absolute(h)

noise = numpy.max(abs)

print("Desviación promedio:")
print(noise-1)
print("Desviación promedio en dBv")
print(20*numpy.log10(noise-1))
pyplot.subplot(2,1,1)
pyplot.plot(f,numpy.absolute(h))
pyplot.show()