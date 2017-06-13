#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    File name: main.py
    Author: Daniela Pralon, Eduardo Andrews, João Paulo Reis Alvarenga, Manoel Stilpen, Marina Lima, Patrick Rosa
    Date created: 5/30/2017
    Data last modified: 6/12/2017
    Python version: 2.7
    License: GPL
"""

from simulador import CamadaFisica
from simulador import CamadaEnlace

from threading import Thread
from time import sleep


class Servidor(Thread):
    """
    Thread para simular um servidor
    """
    def __init__(self, tipo, porta):
        Thread.__init__(self)
        self.__camadafisica = CamadaFisica(tipo, '127.0.0.1', porta)

    def run(self):
        self.__camadafisica.servir()


class Cliente(Thread):
    """
    Thread para simular um cliente
    """
    def __init__(self, tipo, endereco, porta):
        Thread.__init__(self)
        self.__camadafisica = CamadaFisica(tipo, endereco, porta)
        self.__camadaenlace = CamadaEnlace(0.1, 0.01, 0.01, 32, (10, 20))

    def run(self):
        while True:
            frame = self.__camadaenlace.gerar_frame()
            frame = self.__camadaenlace.aplicar_ruido(frame)
            msg = ''.join([str(bit) for bit in frame])
            self.__camadafisica.enviar_msg(msg)
            sleep(0.5)


if __name__ == '__main__':
    thread_servidor = Servidor('UDP', 6666)
    thread_cliente = Cliente('UDP', '127.0.0.1', 6666)

    thread_servidor.start()
    thread_cliente.start()

    thread_cliente.join()
    thread_servidor.join()
