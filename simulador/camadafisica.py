# -*- coding: utf-8 -*-
"""
    File name: camadafisica.py
    Author: Daniela Pralon, Eduardo Andrews, João Paulo Reis Alvarenga, Manoel Stilpen, Marina Lima, Patrick Rosa
    Date created: 5/30/2017
    Data last modified: 6/30/2017
    Python version: 2.7
    License: GPL
"""

import socket
from threading import Thread
from datetime import datetime


class CamadaFisica(object):
    """
    Simulação da camada física, responsável por controlar as mensagens
    """

    def __init__(self, transporte, host, porta):
        """
        Função init da classe
        :param transporte(string): Tipo da camada TCP ou UDP
        :param host(string): Endereço de IP para subir ou conectar ao servidor 
        :param porta(int): Porta 
        :return None
        """
        self.__transporte = transporte
        self.__host = host
        self.__porta = porta
        tipo_socket = {'UDP': socket.SOCK_DGRAM, 'TCP': socket.SOCK_STREAM}
        self.__socket = socket.socket(socket.AF_INET, tipo_socket[transporte])

    def servir(self):
        """
        Mantem a camada servindo, funcionando como um servidor
        :return: None
        """
        self.__socket.bind((self.__host, self.__porta))

        if self.__transporte == 'TCP':
            self.__socket.listen(1)
            return self.__servir_tcp()

        return self.__servir_udp()

    def __receber_msg_tcp(self, conexao, cliente):
        """
        Trata mensagens recebidas através do protocolo TCP
        :param conexao(Connection): Objeto da conexao
        :param cliente(tuple): Identificação do cliente 
        :return: None
        """
        while True:
            msg = conexao.recv(1024)
            if not msg:
                break
            print("[{}] {} - {}".format(datetime.now(), cliente, msg))
        conexao.close()

    def __servir_tcp(self):
        """
        Trata os clientes TCPs conectados ao servidor, instanciando uma thread pra cada cliente
        :return: None
        """
        threads = []
        while True:
            conexao, cliente = self.__socket.accept()
            thread = Thread(target=self.__receber_msg_tcp, args=(conexao, cliente))
            thread.start()
            threads.append(thread)

    def __servir_udp(self):
        """
        Trata os clientes UDPs conectados ao servidor
        :return: None
        """
        while True:
            self.__receber_msg_udp()

    def __receber_msg_udp(self):
        """
        Trata a mensagem enviado por um cliente UDP
        :return: None
        """
        msg, cliente = self.__socket.recvfrom(1024)
        print("[{}] {} - {}".format(datetime.now(), cliente, msg))

    def __enviar_tcp(self, msg):
        """
        Envia uma mensagem utilizando o protocolo TCP
        :param msg(string): Mensagem para ser enviada
        :return: None
        """
        self.__socket.send(msg)

    def __enviar_udp(self, msg):
        """
        Envia uma mensagem utilizando o protocolo UDP
        :param msg(string): Mensagem para ser enviado 
        :return: None
        """
        self.__socket.sendto(msg, (self.__host, self.__porta))

    def enviar_msg(self, msg):
        """
        Trata uma mensagem a ser enviada, direcionando ao protocolo certo
        :param msg: Mensagem a ser enviada
        :return: None
        """
        if self.__transporte == 'TCP':
            return self.__enviar_tcp(msg)

        return self.__enviar_udp(msg)
