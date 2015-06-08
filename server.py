#!/usr/bin/python2
# -*- coding: utf-8 -*-

# Grado de Ingeniería Informática
# Asignatura Sistemas Distribuidos
# Fecha: 08/06/2015
# Autores:
#   José Carlos Solís Lojo
#   Alejandro Rosado Pérez
#   Alexandra Morón Méndez
#   Juan Manuel Hidalgo Navarro
# Descripción:
#   Servidor de una aplicación de transferencia de archivos.
#   La aplicación permite listar, borrar, enviar y recivir archivos de
#   una máquina que esta ejecutando la parte servidor del código.
#   El servidor ejecutará un método u otro en función del parámetro
#   que le envie el cliente.

import zmq
import os

# Set up the zeromq context and REP socket
context = zmq.Context(1)
sock = context.socket(zmq.REP)
sock.bind('tcp://*:4545')

# Envia un archivo solicitado por el cliente
def enviar(path):
    # Comprobamos que el fichero existe
    if os.path.exists("./files/"+path):
        sock.send('si') # El archivo existe
        sock.recv()
        fn = open("./files/"+path, 'rb')
        stream = True
        # Start reading in the file
        while stream:
            # Read the file bit by bit
            stream = fn.read(128)
            if stream:
                # If the stream has more to send then send more
                sock.send(stream, zmq.SNDMORE)
            else:
                # Finish it off
                sock.send(stream)
        print "Archivo enviado al cliente con éxito."
    else:
        sock.send('no')

# Almacena un arvhivo enviado por el cliente
def recibir(archivo):
    sock.send('')
    
    # Creamos el archivo en la carpeta indicada en la ruta
    dest = open('./files/'+archivo, 'w+')
    
    while True:
        # Start grabing data
        data = sock.recv()
        # Write the chunk to the file
        dest.write(data)
        if not sock.getsockopt(zmq.RCVMORE):
            # If there is not more data to send, then break
            break
    print "Archivo almacenado en el servidor con éxito."
    sock.send('')

# Envia al cliente el contenido de la carpeta files
def listar():
    os.system("ls ./files > listado.txt") # hacemos ls y guardamos la salida en un fichero
    fichero = open('listado.txt', 'r')
    listado = fichero.read() # leemos el contenido del fichero para enviarlo
    sock.send(listado)
    os.system("rm listado.txt") # eliminamos el fichero

# Borrar un archivo si existe
def borrar(archivo):
    if os.path.exists("./files/"+archivo):
        os.system("rm ./files/"+archivo)
        sock.send('Archivo borrado con éxito.')
    else:
        sock.send('El archivo no existe.') 


# Fución principal del servidor
def server():
    print "Servidor a la espera..."
    # Start the server loop
    while True:
        # Recibimos un mensaje del cliente
        msg = sock.recv()
        
        # Dependiendo del mensaje, se ejecuta un método u otro
        if msg == 'get':
             sock.send('') # conexión establecida
             path = sock.recv()
             enviar(path)
        elif msg == 'send':
             sock.send('') # conexión establecida
             path = sock.recv()
             recibir(path)
        elif msg == 'list':
             listar()
        elif msg == 'del':
             sock.send('') # conexión establecida
             path = sock.recv()
             borrar(path)



if __name__ == '__main__':
    server()
