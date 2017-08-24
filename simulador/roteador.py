# -*- coding: utf-8 -*-
"""
    File name: roteador.py
    Author: Ana Moraes, Daniela Pralon, Eduardo Andrews, João Paulo Reis Alvarenga, Manoel Stilpen, Patrick Rosa
    Date created: 08/23/2017
    Data last modified: 08/23/2017
    Python version: 3
    License: GPL
"""

from threading import Thread

import json
from time import sleep

from simulador import CamadaEnlace, CamadaFisica, CamadaTransporte


class Roteador(Thread):
    def __init__(self, porta):
        self.__enlace = CamadaEnlace(0.1, 0.01, 0.01, 32, (10, 20))
        self.__transporte = CamadaTransporte()
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
                conexao.enviar_msg('SEND', ack=True)
                # print('Esperando resposta')
                msg, cliente = conexao.receber()
                #print(msg)
                if msg != '':
                    checksum = self.__enlace.verifica_check_sum([int(i) for i in msg])
                    while not checksum:
                        print('error')
                        conexao.enviar_msg('SEND_AGAIN', ack=True)
                        msg, cliente = conexao.receber()
                        if msg == '':
                            break
                        checksum = self.__enlace.verifica_check_sum([int(i) for i in msg])
                    conexao.enviar_msg('OK')
                    try:
                        source, target, foo = self.__transporte.desenpacotar_mensagem(msg)
                        pacote = {'msg': msg, 'target': target}
                        self.__fila_pacotes.append(pacote)
                    except:
                        pass
            for pacote in self.__fila_pacotes:
                if pacote['target'] in self.__conexoes:
                    conexao = self.__conexoes[pacote['target']]
                    # print('Enviando recv')
                    conexao.enviar_msg('RECV', ack=True)
                    # print('Enviando msg')
                    conexao.enviar_msg(pacote['msg'])
            self.__fila_pacotes = []
            # sleep(1)
        print('morri router')


