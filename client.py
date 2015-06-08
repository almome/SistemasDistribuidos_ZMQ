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
#   Cliente de una aplicación de transferencia de archivos.
#   La aplicación permite listar, borrar, enviar y recivir archivos de
#   una máquina que esta ejecutando la parte servidor del código.
#   Se debe pasar un argumento con la dirección del servidor
#   al ejecutar este archivo.

import zmq 
import os
import sys

# Set up the zeromq context and socket
context = zmq.Context()
socket = context.socket(zmq.REQ)
if len(sys.argv) == 2: # Si hemos introducido la IP como argumento
    socket.connect('tcp://'+sys.argv[1]+':4545')
else:
    socket.connect('tcp://127.0.0.1:4545')


# Muesta las órdenes disponibles
def ayuda():
    print ""
    print "Las ordenes disponibles son:"
    print "\tlist\t\t\tListar archivos alojados en el servidor."
    print "\tdel [archivo]\t\tBorra un archivo del servidor."
    print "\tsend [ruta_archivo]\tEnvia un archivo al servidor."
    print "\tget [archivo] [destino]\tObtiene un archivo del servidor."
    print "\texit\t\t\tCierra la aplicación." 
    print ""


# Recibe un archivo del servidor en la ruta indicada
def recibir(archivo, path):    
    socket.send("get") # Le decimos al servidor que queremos obtener un archivo
    socket.recv()
    socket.send(archivo) # Indicamos el archivo que queremos obtener

    if socket.recv() == 'si':
        # Creamos el archivo en la carpeta indicada en la ruta
        dest = open(path+archivo, 'w+')
        socket.send('')
        # Código para recibir el fichero
        while True:
            # Start grabing data
            data = socket.recv()
            # Write the chunk to the file
            dest.write(data)
            if not socket.getsockopt(zmq.RCVMORE):
                # If there is not more data to send, then break
                break
        print "Archivo recibido con éxito."
    else:
        print "El archivo solicitado no existe. Compruebe el nombre del archivo."


# Enviar un archivo a la carpeta del servidor
def enviar(path):
    if os.path.exists(path):
        socket.send('send') # Le decimos al servidor que queremos enviar un archivo
        socket.recv()
        archivo = path.split('/')
        socket.send(archivo[len(archivo)-1]) # Le enviamos solo el nombre del archivo, no la
        socket.recv()

        # Open the file for reading
        fn = open(path, 'rb')
        stream = True
        # Start reading in the file
        while stream:
            # Read the file bit by bit
            stream = fn.read(128)
            if stream:
                # If the stream has more to send then send more
                socket.send(stream, zmq.SNDMORE)
            else:
                # Finish it off
                socket.send(stream)
        socket.recv()
        print 'Archivo enviado con éxito.'
    else:
        print 'El archivo que desea enviar no existe. Revise la ruta.'

# Pide al servidor un listado con sus archivos
def listar():
    socket.send("list")
    listado = socket.recv()
    print '\nLista de archivos alojados en el servidor:'
    print listado

# Borrar un archivo alojado en el servidor
def borrar(archivo):
    socket.send('del')
    socket.recv()
    socket.send(archivo)
    print socket.recv()

# Función principal
def main():
    orden = ""
    print "Introduzca '?' para obtener ayuda."
    
    while orden != "exit":
        orden = raw_input('Orden: ') # Leemos la orden de teclado
        orden_str = orden.split(" ") # Separamos la orden por espacios
        
        # Segun la orden introducida se hará una cosa u otra
        if orden_str[0] == "?":
            ayuda()
        elif orden_str[0] == "list":
            listar()
        elif orden_str[0] == "send":
            if len(orden_str) == 2: # Esta orden necesita 1 parámetros
                enviar(orden_str[1])
            else:
                print "Formato de orden incorrecto."
        elif orden_str[0] == "get":
            if len(orden_str) == 3: # Esta orden necesita 2 parámetros
                recibir(orden_str[1], orden_str[2])
            else:
                print "Formato de orden incorrecto."
        elif orden_str[0] == "del":
            if len(orden_str) == 2: # Esta orden necesita 1 parámetro
                borrar(orden_str[1])
            else:
                print "Formato de orden incorrecto."
        elif orden_str[0] == "exit":
            print "Cerrando aplicación."
        else:
            print "No se reconoce la orden."


if __name__ == '__main__':
    main()
