# SistemasDistribuidos_ZMQ
Repositorio donde se aloja el proyecto de la asignatura de Sistemas Distribuidos en ZeroMQ.
--------------------------------------------------------------------------------------------

# Creadores:
  + Juan Manuel Hidalgo Navarro (https://github.com/JuanmaHidalgoNavarro)
  + Alexandra Morón Méndez (https://github.com/almome)
  + Alejandro Rosado Pérez (https://github.com/ARosadoPerez)
  + Jose Carlos Solís Lojo (https://github.com/jocasolo)

En nuestro proyecto con ZeroMQ vamos a llevar a cabo un sistema de transferencia de ficheros de forma remota, en el cual tendremos un cliente y un servidor, donde el servidor dará varias opciones al cliente y el cliente podra enviar
o recibir ficheros entre muchas otras cosas.

# Idea del Proyecto
El proyecto podrá realizar un envio de ficheros entre cliente y servidor. El servidor estará a la espera de cualquier peticion de un cliente, ya sea de almacenar un fichero, recibir un listado de los ficheros almacenados, obtener un fichero del servidor o incluso borrarlo.

# Funcionamiento
Para ejecutar el proyecto es necesario ejecutar el servidor en una maquina con "python server.py". Cuando un cliente quiera realizar una acción con el servidor ejecutará el cliente con "python client.py" y opcionalmente introducir la IP del servidor como argumento.
Una vez ejecutado el cliente podrá hacer uso de las ordenes a continuación listadas:
- list (Listar archivos alojador en el servidor).
- del {archivo} (Borra un archivo del servidor)
- send {ruta_archivo} (Enviaa un archivo al servidor)
- get {archivo} [destino] (Obtiene un archivo del servidor y lo almacena en destino)
- exit (Cierra la aplicación)
