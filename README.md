tcp2udp
=======

Tool for convert tcp traffic to udp. Firewall bypassing



************************ TCP 2 UDP FIREWALL BYPASSING ***********************

Descripcion: Evasion de cortafuegos a traves del protocolo UDP
Dependencias: packit socat (aptitude install packit socat)
Version: Version inicial 0.1 Beta 10 de Enero de 2011
Comentarios: Testeado en entorno Debian 5.0
Autor: Roberto Amado, S2 Grupo
*****************************************************************************

Configuración
-------------

1º Satisfacer dependencias mediante: 
	aptitude install packit socat

2º Editar el archivo tcp2udpClient.py y modificar la variable IPServidor con la dirección de la IP del Cortafuegos que estará haciendo NAT al servidor comprometido

	Ej. IPServidor = '172.17.22.1'

3º Editar el archivo tcp2udpServer.py y modificar la variable ip_cliente con la dirección de la IP del equipo atacante, así como modificar el interfaz de red utilizado

 	Ej. ip_cliente = '192.168.1.23'
	Ej. interfaz  = "eth0"

4º Modificar si se desea el puerto de control por donde se intercambiará el cliente y el servidor la información. Este pueto se utiliza además como base para los mapeos de puertos de la víctima, de forma local en el atacante.
	Ej. puerto_control = 50000


Instalación
-----------

1º Ejecutar tcp2udpClient.py en el entorno atacante y esperar a la conexión del servidor (víctima) (como root).

	Ej. python tcp2udpClient.py

2º Ejecutar tcp2udpServer.py en el entorno víctima (como root).

	Ej. python tcp2udpServer.py

En ese momento el la victima remitirá por el puerto de control la información de sus sericios al atacante. Cada puerto  TCP de la víctima se le asigna un puerto UDP mapeado en todas las interfaces, incluidos los servicios que escuchan tan solo en localhost. El tráfico TCP es transformado a UDP y remitido al atacante. Este último para conectar con uno de esos servicios tan solo tendrá que realizar una conexión TCP en su interfaz localhost.

Ejemplo de salida por pantalla del atacante:



Socket Remoto        Proceso Remoto    Socket local en localhost
-------------        ---------------   -------------------------
0.0.0.0:389     -->     slapd           127.0.0.1:50001/TCP

0.0.0.0:57574   -->     rpc.statd       127.0.0.1:50002/TCP

0.0.0.0:8010    -->     python          127.0.0.1:50003/TCP

127.0.0.1:587   -->     sendmail:MTA:   127.0.0.1:50004/TCP

0.0.0.0:111     -->     portmap         127.0.0.1:50005/TCP

0.0.0.0:81      -->     nginx           127.0.0.1:50006/TCP

0.0.0.0:113     -->     inetd           127.0.0.1:50007/TCP

127.0.0.1:818   -->     famd            127.0.0.1:50008/TCP

0.0.0.0:22      -->     sshd            127.0.0.1:50009/TCP

0.0.0.0:23      -->     inetd           127.0.0.1:50010/TCP

127.0.0.1:631   -->     cupsd           127.0.0.1:50011/TCP

127.0.0.1:25    -->     sendmail:MTA:   127.0.0.1:50012/TCP


En es momento si el atacante desea conectarse al puerto de telnet de la victima realizaría lo siguiente:

telnet localhost 50010


Happy hacking ;)!



Fallos Conocidos
----------------

* Dependiendo del servicio mapeado este puede no responder correctamente, como por ejemplo el servicio de ssh. Servicios como telnet, http, SMTP, https suele funcionar muy bien.

* No funciona en Windows (todavía)

* Tanto cliente como servidor han de ejecutarse como root

TODO
----------------

* Versión para Windows
* Aunar la comuniación UDP en un solo puerto demultiplexando los paquetes a la llegada al cliente y al servidor.
