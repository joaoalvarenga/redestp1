# -*- coding: utf-8 -*-
from threading import Thread

import json
from time import sleep

from simulador import CamadaEnlace, CamadaFisica


class Roteador(Thread):
    def __init__(self, porta):
        self.__enlace = CamadaEnlace(0.1, 0.01, 0.01, 32, (10, 20))
        # self.__conexoes = [CamadaFisica('UDP', '127.0.0.1', 6666, False, 0), CamadaFisica('UDP', '127.0.0.1', 6667, False, 0)]
        self.__conexoes = {}

        self.__fila_pacotes = []

        self.__killme = False

        Thread.__init__(self)

    def adicionar_conexao(self, conexao_ip, conexao_porta, endereco):
        self.__conexoes[endereco] = CamadaFisica('UDP', conexao_ip, conexao_porta, False, 0)

    def killme(self):
        self.__killme = True

    def run(self):
        while not self.__killme:
            for conexao in self.__conexoes.values():
                # print('Enviando send')
                conexao.enviar_msg('SEND')
                # print('Esperando resposta')
                msg, cliente = conexao.receber()
                ## print(msg)
                try:
                    pacote = {'msg': msg.decode('utf-8'), 'target': int(msg[:8], 2)}
                    self.__fila_pacotes.append(pacote)
                except:
                    pass
            for pacote in self.__fila_pacotes:
                conexao = self.__conexoes[pacote['target']]
                # print('Enviando recv')
                conexao.enviar_msg('RECV')
                # print('Enviando msg')
                conexao.enviar_msg(pacote['msg'])
            self.__fila_pacotes = []
            # sleep(1)
        print('morri router')


