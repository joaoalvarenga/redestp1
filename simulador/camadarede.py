# -*- coding: utf-8 -*-
"""
    File name: camadarede.py
    Author: Ana Moraes, Daniela Pralon, Eduardo Andrews, João Paulo Reis Alvarenga, Manoel Stilpen, Patrick Rosa
    Date created: 8/03/2017
    Data last modified: 8/03/2017
    Python version: 2.7
    License: GPL
"""

from collections import defaultdict

class CamadaRede(object):
    """
    Simulacao da Camada de Rede
    """

    def __init__(self, nome_arquivo):
        self.__nome_arquivo = nome_arquivo
        self.__nconexoes = 0
        self.__nhosts = 0
        self.__connections = defaultdict(list)  # edges

        self.__read_graph()

    def __read_graph(self):
        with open(self.__nome_arquivo) as file:
            self.__nhosts, self.__nedges = file.readline().split()

            for _ in range(int(self.__nconexoes)):
                src, dest = file.readline().split()
                self.__connections[src].append(dest)
                self.__connections[dest].append(src)