# -*- coding: utf-8 -*-
'''
    File name: camadafisica.py
    Author: Daniela Pralon, João Paulo Reis Alvarenga, Manoel Stilpen, Marina Lima, Patrick Rosa, Eduardo Andrews
    Date created: 5/30/2017
    Data last modified: 5/30/2017
    Python version: 2.7
    License: GPL
'''

import socket
from threading import Thread

from datetime import datetime

class CamadaFisica(object):

    def __init__(self, transporte, host, port):
        self.__transporte = transporte
        self.__host = host
        self.__port = port
        tipo_socket = {'UDP': socket.SOCK_DGRAM, 'TCP': socket.SOCK_STREAM}
        self.__socket = socket.socket(socket.AF_INET, tipo_socket[transporte])

    def servir(self):
        self.__socket.bind((self.__host,self.__port))

        if self.__transporte == 'TCP':
            self.__socket.listen(1)
            return self.__servir_tcp()

        return self.__servir_udp()

    def __receber_msg_tcp(self, conexao, cliente):
        while True:
            msg = conexao.recv(1024)
            if not msg:
                break
            print("[{}] {} - {}".format(datetime.now(), cliente, msg))
        conexao.close()

    def __servir_tcp(self):
        threads = []
        while True:
            conexao, cliente = self.__socket.accept()
            thread = Thread(target=self.__receber_msg_tcp, args=(conexao, cliente))
            thread.start()
            threads.append(thread)

    def __servir_udp(self):
        while True:
            self.__receber_msg_udp()

    def __receber_msg_udp(self):
        msg, cliente = self.__socket.recvfrom(1024)
        print("[{}] {} - {}".format(datetime.now(), cliente, msg))

    def __enviar_tcp(self, msg):
        self.__socket.send(msg)

    def __enviar_udp(self, msg):
        self.__socket.sendto(msg, (self.__host, self.__port))

    def enviar_msg(self, msg):
        if self.__transporte == 'TCP':
            return self.__enviar_tcp(msg)

        return self.__enviar_udp(msg)

