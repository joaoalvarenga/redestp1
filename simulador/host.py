# -*- coding: utf-8 -*-
import json, logging
from threading import Thread, Lock
from queue import Queue

from simulador import CamadaEnlace, CamadaFisica


class HostConsumer(Thread):
    def __init__(self, porta):
        self.__lock = Lock()
        self.__fisica = CamadaFisica('UDP', '0.0.0.0', porta, False, 0)
        self.__fisica.servir()
        Thread.__init__(self)

        self.__killme = False
        self.__pacote = None

        self.__pacotes_recebidos = []
        self.__pacotes_enviar = []

    def killme(self):
        self.__killme = True

    def send_message(self, packet):
        self.__pacotes_enviar.append(packet)

    def collect_packets(self):
        packets = self.__pacotes_recebidos
        self.__pacotes_recebidos = []
        return packets

    def run(self):
        while not self.__killme:
            # print('Esperando roteador')
            __msg, __cliente = self.__fisica.receber()
            # self.__get_shared_values()
            # # print(str(__msg))
            if __msg is None:
                continue
            if __msg.decode('UTF-8') == 'SEND':  # pergunta ao host se ele tem algo para mandar
                print('Enviando mensagem com pacotes')
                if len(self.__pacotes_enviar) > 0:
                    self.__fisica.enviar_msg(self.__pacotes_enviar.pop(), __cliente)
                else:
                    self.__fisica.enviar_msg('', __cliente)
                # self.__get_shared_values()
                # self.__set_shared_values('')

            if __msg.decode('UTF-8') == 'RECV':  # pede ao host para que ele receba um pacote
                # print("Recebendo pacote do roteador")
                msg, cliente = self.__fisica.receber()
                self.__pacotes_recebidos.append(msg.decode('utf-8'))
                msg = msg.decode('utf-8')
                msg_sender = msg.split(' - ')[0]
                msg = msg.split(' - ')[1]
                msg = msg[8:-6]
                msg = ''.join([chr(int(msg[i:i+8], 2))for i in range(0, len(msg), 8)])

                print('Pacote recebido {} - {}'.format(msg_sender, msg))
        print('morri host')


class Host(Thread):
    def __init__(self, porta):
        """
        Inicia o host como servidor que espera o roteador coletar suas mensagens
        :param porta:
        """
        self.__queue = Queue(1)
        self.__pacote = None
        self.__killme = False  # flag para matar host
        self.__thread = HostConsumer(self.__queue, porta)  # Thread para escutar roteador
        self.__porta = porta
        self.__last_message = None
        Thread.__init__(self)
        self.__queue.put({'killme': False, 'pacote': ''})

    def killme(self):
        self.__killme = True

    def get_porta(self):
        return self.__porta

    def send_message(self, target, msg):
        packet = {'target': target, 'msg': msg}
        self.__queue.put({'killme': self.__killme, 'pacote': json.dumps(packet)})

    def run(self):
        self.__thread.start()
        while not self.__killme:
            self.__op = None
            # self.__queue.put({'killme': self.__killme, 'pacote': '{"target": 1, "msg": "olá 1"}'.encode('utf-8')})
