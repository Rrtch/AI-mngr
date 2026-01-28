import time

#Funciones de tiempo

def wait(X):        #esperar X segundos
    timeout_start = time.time()
    while  time.time()< timeout_start + X:
        time.sleep(0)

def Tpss(T):            #Tiempo pasad a partir de T (en formato .time)
    return(time.time()-T)

def tomarmomento():     #marcar el momento actual (en formato segundos pasados a partir de la hora 0 del dia actual)
    a=(time.localtime()[3]*60*60)
    b=(time.localtime()[4]*60)
    c=(time.localtime()[5])
    return (a+b+c)