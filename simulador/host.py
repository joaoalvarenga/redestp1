# -*- coding: utf-8 -*-
import json
from threading import Thread, Lock
from queue import Queue

from simulador import CamadaEnlace, CamadaFisica


class HostConsumer(Thread):
    def __init__(self, queue, porta):
        self.__lock = Lock()
        self.__queue = queue
        self.__fisica = CamadaFisica('UDP', '0.0.0.0', porta, False, 0)
        self.__fisica.servir()
        Thread.__init__(self)

        self.__killme = False
        self.__pacote = None

    def __get_shared_values(self):
        if not self.__queue.empty():
            values = self.__queue.get()
            self.__queue.task_done()
            self.__killme = values['killme']
            self.__pacote = values['pacote']

    def __set_shared_values(self, pacote):
        if not self.__queue.empty():
            self.__queue.put({'killme': self.__killme, 'pacote': pacote})

    def run(self):
        while not self.__killme:
            print('Esperando roteador')
            __msg, __cliente = self.__fisica.receber()
            self.__get_shared_values()
            # print(str(__msg))
            if __msg.decode('UTF-8') == 'SEND':  # pergunta ao host se ele tem algo para mandar
                print('Enviando mensagem com pacotes')
                self.__fisica.enviar_msg(self.__pacote, __cliente)
                self.__get_shared_values()
                self.__set_shared_values(b'')

            if __msg.decode('UTF-8') == 'RECV':  # pede ao host para que ele receba um pacote
                print("Recebendo pacote do roteador")
                msg, cliente = self.__fisica.receber()
                print('Pacote recebido {}'.format(msg.decode('utf-8')))


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
        Thread.__init__(self)
        self.__queue.put({'killme': False, 'pacote': b''})

    def get_porta(self):
        return self.__porta

    def send_message(self, target, msg):
        packet = {'target': target, 'msg': msg}
        self.__queue.put({'killme': False, 'pacote': json.dumps(packet)})

    def run(self):
        self.__thread.start()
        while not self.__killme:
            self.__op = None
            # self.__queue.put({'killme': self.__killme, 'pacote': '{"target": 1, "msg": "olá 1"}'.encode('utf-8')})
