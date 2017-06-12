# -*- coding: utf-8 -*-
'''
    File name: main.py
    Author: Daniela Pralon, Joao Paulo Reis Alvarenga, Manoel Stilpen, Marina Lima, Patrick Rosa
    Date created: 5/30/2017
    Data last modified: 5/30/2017
    Python version: 2.7
    License: GPL
'''

from simulador.camadafisica import CamadaFisica
from simulador.camadaenlace import CamadaEnlace

camada_fisica = CamadaFisica('UDP', '127.0.0.1', '666')
camada_enlace = CamadaEnlace(0.1, 0.01, 0.01, 32, (1,10))
print(camada_enlace.gerar_msg())