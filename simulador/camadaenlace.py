# -*- coding: utf-8 -*-
"""
    File name: camadaenlace.py
    Author: Daniela Pralon, Eduardo Andrews, João Paulo Reis Alvarenga, Manoel Stilpen, Marina Lima, Patrick Rosa, Eduardo Andrews
    Date created: 5/30/2017
    Data last modified: 6/12/2017
    Python version: 2.7
    License: GPL
"""
from random import random, randint, choice


class CamadaEnlace(object):
    """
    Simulação da Camada de Enlace, responsável por gerar os quadros e gerar os ruídos nas mensagens
    """

    def __init__(self, prob_inversao, prob_adicao, prob_rajada, tamanho_frame, intervalo_rajada):
        """
        Função de Init da classe
        :param prob_inversao(float): Probabilidade de inverter um bit
        :param prob_adicao(float): Probabilidade de adicionar um bit para cada bit do frame
        :param prob_rajada(float): Probabilidade de adicionar uma rajada
        :param tamanho_frame(int): Tamanho do frame
        :param invervalo_rajada(tuple(int,int)): Invervalo de tamanhos da rajada
        :return: None
        """
        self.__prob_inversao = prob_inversao  # probabilidade de inverter um bit
        self.__prob_adicao = prob_adicao  # probabilidade de adicionar um bit
        self.__prob_rajada = prob_rajada  # probabilidade da rajada
        self.__tamanho_frame = tamanho_frame  # tamanho do quadro
        self.__intervalo_rajada = intervalo_rajada

    def __inverter_bit(self, bit):  # inversor de bit
        """
        Inverte o bit caso caia no caso probabilístico
        :param bit(int): Bit a ser invertido 
        :return(int): bit invertido ou não
        """
        if random() <= self.__prob_inversao:
            return int(not bit)
        return bit

    def __adicionar_bit(self, bit):
        """
        Adiciona um bit logo após caso caia no caso probabilístico
        :param bit(int): Bit a ser invertido 
        :return(list[int]): Array contendo o somente o bit original, ou o bit original mais um bit
        """
        if random() <= self.__prob_adicao:
            return [bit, randint(0, 1)]
        return [bit]

    def __aplicar_rajada(self, frame):
        """
        Adiciona uma rajada em uma posição aleatória do frame
        :param frame(list[int]): Quadro o qual será adicionada a rajada
        :return(list[int]): Quadro contendo a rajada ou não 
        """
        if random() <= self.__prob_rajada:
            tamanho_rajada = choice(self.__intervalo_rajada)  # escolhe um tamanho aleatório para a rajada
            rajada = [randint(0, 1) for i in range(tamanho_rajada)]  # gera o conteúdo da rajada
            posicao_insercao = randint(0,
                                       self.__tamanho_frame - 1)  # escolhe aleatóriamente um lugar para inserir a rajada
            frame_final = frame[:posicao_insercao] + rajada + frame[
                                                              posicao_insercao:]  # concatena a rajada junto ao frame
            return frame_final

        return frame

    def gerar_frame(self):
        """
        Gera a mensagem original
        :return(list[int]): Retorna a mensagem original 
        """
        frame = [randint(0, 1) for i in range(self.__tamanho_frame)]  # gera a mensagem original
        return frame

    def aplicar_ruido(self, frame):
        """
        Aplica os ruídos no frame original de dados
        :param frame(list[int]): Quadro original sem ruídos 
        :return(list[int]): Quadro final com ruídos 
        """
        frame_prob_inversao = [self.__inverter_bit(bit) for bit in frame]  # aplica ruido de inversão
        frame_prob_adiconar = []
        for bit in frame_prob_inversao:
            frame_prob_adiconar += self.__adicionar_bit(bit)  # aplica ruido de adição

        frame_final = self.__aplicar_rajada(frame_prob_adiconar)
        return frame_final
