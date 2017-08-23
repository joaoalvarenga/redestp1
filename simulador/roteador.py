# -*- coding: utf-8 -*-
from threading import Thread

import json
from time import sleep

from simulador import CamadaEnlace, CamadaFisica


class Roteador(Thread):
    def __init__(self, porta):
        self.__enlace = CamadaEnlace(0.1, 0.01, 0.01, 32, (10, 20))
        # self.__conexoes = [CamadaFisica('UDP', '127.0.0.1', 6666, False, 0), CamadaFisica('UDP', '127.0.0.1', 6667, False, 0)]
        self.__conexoes = []

        self.__fila_pacotes = []

        self.__killme = False

        Thread.__init__(self)

    def adicionar_conexao(self, conexao_ip, conexao_porta):
        self.__conexoes.append(CamadaFisica('UDP', conexao_ip, conexao_porta, False, 0))

    def run(self):
        while not self.__killme:
            for i, conexao in enumerate(self.__conexoes):
                print('Enviando send')
                conexao.enviar_msg(b'SEND')
                print('Esperando resposta')
                msg, cliente = conexao.receber()
                #print(msg)
                try:
                    msg = json.loads(msg.decode('utf-8'))
                    if type(msg) == dict:
                        msg['source'] = i
                        self.__fila_pacotes.append(msg)
                except:
                    pass
            for pacote in self.__fila_pacotes:
                conexao = self.__conexoes[pacote['target']]
                print('Enviando recv')
                conexao.enviar_msg(b'RECV')
                print('Enviando msg')
                conexao.enviar_msg('{} - {}'.format(pacote['source'], pacote['msg']).encode('utf-8'))
            self.__fila_pacotes = []
            sleep(1)



