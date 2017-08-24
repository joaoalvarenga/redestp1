# -*- coding: utf-8 -*-
"""
    File name: camadatransporte.py
    Author: Ana Moraes, Daniela Pralon, Eduardo Andrews, João Paulo Reis Alvarenga, Manoel Stilpen, Patrick Rosa
    Date created: 08/23/2017
    Data last modified: 08/23/2017
    Python version: 2.7
    License: GPL
"""
from threading import Thread

from simulador import HostConsumer, CamadaEnlace, CamadaTransporte


class CamadaAplicacao(Thread):
    """
    Simulacao da Camada de Aplicacao
    """

    def __init__(self, nome, endereco, porta, messages):
        self.__nome = nome
        self.__endereco = endereco
        self.__porta = porta
        self.__host = HostConsumer(porta)
        self.__enlace = CamadaEnlace(0.1, 0.01, 0.01, 32, (10, 20))
        self.__transporte = CamadaTransporte()
        self.__messages = messages
        # messages = [{'action': 'recv'}, {'action': 'send', 'target': 0, 'msg': 'Olá, como vai?'}]
        Thread.__init__(self)

        self.__host.start()

    def get_porta(self):
        return self.__porta

    def get_endereco(self):
        return self.__endereco

    def run(self):
        for message in self.__messages:
            if message['action'] == 'recv':
                pacotes = self.__host.collect_packets()
                while len(pacotes) == 0:
                    pacotes = self.__host.collect_packets()
                print('{} - {}'.format(self.__nome, self.__transporte.desenpacotar_mensagem(pacotes[0])))
            if message['action'] == 'send':
                pacote = self.__transporte.gerar_pacote(message['target'], message['msg'])
                pacote = ''.join(map(str, self.__enlace.gera_check_sum([int(i) for i in pacote])))
                self.__host.send_message(pacote)
