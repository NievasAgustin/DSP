import pylab as plt
import numpy as np
import scipy
import scipy.signal as signal
from synthesizer import Synthesizer


def freq_phase(b, a = 1, comment = ''):
    # Create the data points for a transfer function with coefficients b, a
    w, h = signal.freqz(b, a)

    h_dB = 20 * np.log10(abs(h))

    plt.subplot(211)
    plt.plot(w/max(w),h_dB)
    plt.ylim(-120, 10)
    plt.ylabel('Magnitude (db)')
    plt.xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
    plt.title(r'Frequency response ' + comment)

    plt.subplot(212)
    h_Phase = plt.unwrap(np.arctan2(np.imag(h), np.real(h)))
    plt.plot(w/max(w),h_Phase)
    plt.ylabel('Phase (radians)')
    plt.xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
    plt.title(r'Phase response ' + comment)
    plt.subplots_adjust(hspace=0.5)
    plt.show()


def step_impulse(b, a = 1):
    l = len(b)
    impulse = [1.0] + [0] * (l - 1)
    x = np.arange(0, l)
    response = signal.lfilter(b, a, impulse)

    plt.subplot(211)
    plt.stem(x, response, use_line_collection = True)
    plt.ylabel('Amplitude')
    plt.xlabel(r'n (samples)')
    plt.title(r'Impulse response')

    plt.subplot(212)
    step = np.cumsum(response)
    plt.stem(x, step, use_line_collection = True)
    plt.ylabel('Amplitude')
    plt.xlabel(r'n (samples)')
    plt.title(r'Step response')
    plt.subplots_adjust(hspace=0.5)

    plt.show()


def coeff(a):
    total = sum(a)
    plt.plot(a)
    plt.title("Coefficients (sum = {:.6f})".format(total))
    plt.xlabel("number")
    plt.ylabel("value")
    plt.show()


def test_simple_transfer():
    freq_phase(1, 1)


def fir_highpass():
    n_coef = 99
    
    fs = 160000
    f_nyq = fs/2
    #cutoff = 1500/f_nyq = 0.1875
    #width = 800/f_nyq = 0.1
    #filtro pasa alto con fcorte en 1500 con banda de transición hasta 2300[Hz]
    window = "hamming" #("kaiser", 14)
    a = signal.firwin(n_coef, pass_zero = False, cutoff = (0.1875), width = (0.1) , window = window)
    print ("cutoff = 1500[Hz] =",1500/f_nyq,"F_nyquist")
    print ("width = 800[Hz]",800/f_nyq,"F_nyquist")
    print ("fsampling =", fs)
    print ("fnyquist =", f_nyq)
    cof = coeff(a)
    #Grafico coeficientes, respuesta en frecuencia de magnitud y de fase
    freq_phase(a, comment = "(window: {}))".format(window))
    #Grafico de respuesta al impulso  y al escalon
    step_impulse (a)
    print (a)
    
    
    coeffile = open("coeficientes.txt", "w")
    #x = ','.join(str(a))
    x = (str(a))
    coeffile.write (x)
    coeffile.close()
            
   
def main(args):
    #test_simple_transfer ()
    fir_highpass ()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
