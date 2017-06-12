# -*- coding: utf-8 -*-
'''
    File name: main.py
	Author: Daniela Pralon, João Paulo Reis Alvarenga, Manoel Stilpen, Marina Lima, Patrick Rosa, Eduardo Andrews
    Date created: 5/30/2017
    Data last modified: 5/30/2017
    Python version: 2.7
    License: GPL
'''

from simulador.camadafisica import CamadaFisica
from simulador.camadaenlace import CamadaEnlace

from threading import Thread
from time import sleep

class Servidor(Thread):
    def __init__(self, tipo, porta):
        Thread.__init__(self)
        self.__camadafisica = CamadaFisica(tipo, '127.0.0.1', porta)

    def run(self):
        self.__camadafisica.servir()

class Cliente(Thread):
    def __init__(self, tipo, endereco, porta):
        Thread.__init__(self)
        self.__camadafisica = CamadaFisica(tipo, endereco, porta)
        self.__camadaenlace =  CamadaEnlace(0.1, 0.01, 0.01, 32, (1,10))

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