# -*- coding: utf-8 -*-
"""
    File name: camadatransporte.py
    Author: Ana Moraes, Daniela Pralon, Eduardo Andrews, João Paulo Reis Alvarenga, Manoel Stilpen, Patrick Rosa
    Date created: 8/09/2017
    Data last modified: 8/09/2017
    Python version: 2.7
    License: GPL
"""


class CamadaTransporte(object):
    """
    Simulacao da Camada de Transporte
    """

    def __init__(self):
        mensagem = []

    def enviar(self, pacote):
        """
        pacote["ip"]: string contendo ip
        pacote["porta"]: string contendo a porta
        pacote["mensagem"]: string contendo a mensagem a ser enviada
        :param pacote: Mensagem recebida da camada de aplicacao 
        :return: mensagem encapsulada para camada de rede
        """

        mensagem = []

        pacote['ip'] = pacote['ip'].split('.') # separa a string de acordo com o .
        mensagem += list(''.join(format(int(x), 'b').zfill(8) for x in pacote['ip'])) # converte string em binario

        mensagem += list(format(int(pacote['porta']), 'b').zfill(40)) # converte o numero da porta em binario

        if len(pacote['mensagem']) > 256:

        else:
            mensagem += list(''.join(format(ord(p), 'b').zfill(8) for p in pacote['mensagem']))

        print mensagem
