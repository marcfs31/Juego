#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import pygame


# Constantes
#Tuplas con colores
WHITE = (255,255,255)
NEGRO = (0,0,0)

pygame.init() #Inicializar pygame

pantalla = pygame.display.set_mode((800,600)) #Se crea el objeto pantalla con el tamaño en una tupla
pygame.display.set_caption("Mi juego") #Titulo del juego

pygame.display.update() #Actualiza toda la pantalla si no le pasas parametros sino actualiza lo que le pases

salir = False

while not salir: #Mientras salir no sea True se ejecuta
	for event in pygame.event.get(): #Eventos que hay https://www.pygame.org/docs/ref/event.html
		if event.type == pygame.QUIT: #Salir cuando se le da al boton X de la pantalla
			salir = True

pygame.quit()
quit()
