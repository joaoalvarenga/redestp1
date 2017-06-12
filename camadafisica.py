# -*- coding: utf-8 -*-
'''
    File name: camadafisica.py
    Author: Daniela Pralon, Joao Paulo Reis Alvarenga, Manoel Stilpen, Marina Lima, Patrick Rosa
    Date created: 5/30/2017
    Data last modified: 5/30/2017
    Python version: 2.7
    License: GPL
'''

import socket

class CamadaFisica(object):
    def __init__(self, transporte, host, port):
        if transporte == 'UDP':
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # incializa o socket usando UDP na camada de transporte
        else:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # inicializa o socket usandp TCP na camada de transporte

    def servir(host, port):
        self.__socket.bind((host,port))

    def receber_msg():
        msg, client = self.__socket.recvfrom(1024)
        print cliente, msg

    def enviar_msg(msg):
        pass
