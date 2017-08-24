# -*- coding: utf-8 -*-
"""
    File name: camadatransporte.py
    Author: Ana Moraes, Daniela Pralon, Eduardo Andrews, João Paulo Reis Alvarenga, Manoel Stilpen, Patrick Rosa
    Date created: 08/23/2017
    Data last modified: 08/23/2017
    Python version: 2.7
    License: GPL
"""

import json

# mensagem['porta'], mensagem['ip'], mensagem['mensagem']

class CamadaAplicacao(object):
    """
    Simulacao da Camada de Aplicacao
    """

    def __init__(self):
        #self.__config_file = 'config.json'
        #self.__config = json.load(open(self.__config_file))
        self.__messages = [{'ip':'192.168.1.117', 'porta':'22', 'msg':'eai, td bem?'},
                            {'ip':'192.168.1.17', 'porta':'22','msg':'eai, bora fechar?'}]

    def enviar(self):
        """
        Realiza leitura das mensagens no arquivo 
        :return: dict com informacoes parseadas
        """

        if len(self.__messages) > 0:
            ip = self.__messages[0]['ip']
            port = self.__messages[0]['porta']
            msg = self.__messages[0]['msg']

            self.__messages.pop(0)

            return {'ip':ip, 'porta':port, 'mensagem':msg}

        return {}
        