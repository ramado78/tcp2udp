#!/usr/bin/python

"""
************************ TCP 2 UDP FIREWALL BYPASSING ***********************

Descripcion: Evasion de cortafuegos a traves del protocolo UDP
Dependencias: packit socat (aptitude install packit socat)
Version: Version inicial 0.1 Beta
Comentarios: El cliente ha de ser lanzado primero y esperar conexion del servidor. Testeado en entorno Debian 5.0
*****************************************************************************
"""

__autor__ = 'Roberto Amado, S2 Grupo'
__version__ = '0.1 Beta'
__fecha__ = '10 de Enero de 2011'

import socket
import sys
import thread
import os
import signal
from time import sleep

#Variables de configuracion ###############
puerto_control = 50000 #puerto por donde se recibira la informacion de servicios al cliente, debe ser el mismo que en la parte servidor
IPServidor = '172.17.1.37'

###########################################

def muestraInfo(datos):
	
	global puerto_control
	IPproceso = datos.rsplit("@")
	print "Mapeo de servicios remotos en local total: %i puertos remotos\n" % (int(len(IPproceso)) - 1)
	print "Socket Remoto        Proceso Remoto    Socket local en localhost"
	print "-------------        ---------------   -------------------------"
	for i in range(len(IPproceso)):
		if (i != 0):
			info = IPproceso[i].rsplit("#")
			print ("%s\t-->\t%s\t\t%s\n") % (info[0], info[1], "127.0.0.1:" + str(puerto_control + i) + "/TCP")
		
def lanzaProcesos(datos):
	
	global IPServidor
	IPproceso = datos.rsplit("@")
	for i in range(len(IPproceso)):
		if (i != 0):		
			socat = "socat tcp4-listen:" + str(puerto_control + i) + ",reuseaddr,fork,bind=127.0.0.1 UDP:" + IPServidor + ":" + str(puerto_control + i) + ",sourceport=" + str(puerto_control + i)
			thread.start_new_thread(lanzaSocat,(socat,))
	

def lanzaSocat(socat):
	
	os.popen(socat).read()	

def FinPrograma(signum, frame):
		
	print "Fin programa\n"
	

print "Esperando conexion maquina remota....\n"
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
	s.bind(('', puerto_control))
except socket.error, err:
	print "No puede levantars el puerto UDP %d : %s" % (server_port, err)
	raise SystemExit


datagrama = s.recv(5000)
s.close()

muestraInfo(datagrama)
sleep (2)
lanzaProcesos(datagrama)


signal.signal(signal.SIGTERM, FinPrograma)
signal.pause()
