#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    File name: main.py
    Author: Ana Moraes, Daniela Pralon, Eduardo Andrews, João Paulo Reis Alvarenga, Manoel Stilpen, Patrick Rosa
    Date created: 5/30/2017
    Data last modified: 6/12/2017
    Python version: 2.7
    License: GPL
"""

from simulador import CamadaFisica
from simulador import CamadaEnlace
from simulador import Configuration
from simulador import HostConsumer, Roteador

from threading import Thread
from time import sleep


# class Servidor(Thread):
#     """
#     Thread para simular um servidor
#     """
#     def __init__(self, tipo, porta):
#         Thread.__init__(self)
#         self.__camadafisica = CamadaFisica(tipo, '127.0.0.1', porta, False, 0.01)
#
#     def run(self):
#         self.__camadafisica.servir()
#
#
# class Cliente(Thread):
#     """
#     Thread para simular um cliente
#     """
#     def __init__(self, tipo, endereco, porta):
#         Thread.__init__(self)
#         self.__camadafisica = CamadaFisica(tipo, endereco, porta, False, 0.01)
#         self.__camadaenlace = CamadaEnlace(0.1, 0.01, 0.01, 32, (10, 20))
#
#     def run(self):
#         while True:
#             frame = self.__camadaenlace.gerar_frame()
#             frame = self.__camadaenlace.aplicar_ruido(frame)
#             frame = self.__camadaenlace.gera_check_sum(frame)
#             msg = ''.join([str(bit) for bit in frame])
#             self.__camadafisica.enviar_msg(msg)
#             sleep(0.5)
#
#
# if __name__ == '__main__':
#     thread_servidor = Servidor('UDP', 6666)
#     thread_cliente = Cliente('UDP', '127.0.0.1', 6666)
#
#     thread_servidor.start()
#     thread_cliente.start()
#
#     thread_cliente.join()
#     thread_servidor.join()




class Manager(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.__hosts = {}
        self.__routers = []
        self.__enlace = CamadaEnlace(0.1, 0.01, 0.01, 32, (10, 20))

        self.__messages = [
            {'source': 1, 'target': 0, 'msg': ''.join(map(str,self.__enlace.gera_check_sum([int(i) for i in ''.join(['{0:08b}'.format(c) for c in map(ord, 'Olá')])])))},
            {'source': 0, 'target': 1, 'msg': ''.join(map(str,self.__enlace.gera_check_sum([int(i) for i in ''.join(['{0:08b}'.format(c) for c in map(ord, 'Olá, como vai?')])])))},
            {'source': 1, 'target': 0, 'msg': ''.join(map(str,self.__enlace.gera_check_sum([int(i) for i in ''.join(['{0:08b}'.format(c) for c in map(ord, 'Vou bem e você?')])])))},
            {'source': 0, 'target': 1, 'msg': ''.join(map(str,self.__enlace.gera_check_sum([int(i) for i in ''.join(['{0:08b}'.format(c) for c in map(ord, 'Bem também')])])))}
        ]

        self.load_network()

    def load_network(self):
        network = Configuration.options.get_network()
        for host in network['hosts']:
            self.__hosts[host['name']] = {
                'port': host['port'],
                'address': host['address'],
                'thread': HostConsumer(host['port'])
            }
            self.__hosts[host['name']]['thread'].start()

        for router in network['routers']:
            r = Roteador(router['port'])
            for connection in router['connections']:
                r.adicionar_conexao('127.0.0.1', self.__hosts[connection]['port'])
            r.start()
            self.__routers.append(r)

    def run(self):
        for msg in self.__messages:
            for host_name in self.__hosts:
                if self.__hosts[host_name]['address'] == msg['source']:
                    self.__hosts[host_name]['thread'].send_message(msg['target'], msg['msg'])
                    for host_name_2 in self.__hosts:
                        if self.__hosts[host_name_2]['address'] == msg['target']:
                            p = self.__hosts[host_name_2]['thread'].collect_packets()
                            while len(p) == 0:
                                p = self.__hosts[host_name_2]['thread'].collect_packets()
                            # print(p)
                            print(self.__enlace.verifica_check_sum([int(i) for i in p[0].split(' - ')[1]]))

        print('morri')
        for router in self.__routers:
            router.killme()
            router.join()

        for host_name in self.__hosts:
            self.__hosts[host_name]['thread'].killme()
            self.__hosts[host_name]['thread'].join()


if __name__ == '__main__':
    manager = Manager()
    manager.start()

    manager.join()
