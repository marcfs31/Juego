#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import pygame
import time, random


# Constantes
#Tuplas con colores
BLANCO = (255,255,255)
NEGRO = (0,0,0)
ROJO = (255,0,0)
VERDE = (0,150,0)

ANCHURA_PANTALLA = 800
ALTURA_PANTALLA = 600

FPS = 30
FUENTE = "Comfortaa-Regular.ttf"

pantalla = pygame.display.set_mode((ANCHURA_PANTALLA,ALTURA_PANTALLA)) #Se crea el objeto pantalla con el tamaño en una tupla

pygame.display.set_caption("Juego de la serpiente") #Titulo del juego

# --------------------------------------------------------------------- 
# Clases

# ---------------------------------------------------------------------
# Funciones generales
def mensaje_por_pantalla(msg,color): #Funcion para generar mensajes
	pygame.font.init() #Iniciamos font
	font = pygame.font.SysFont(None , 25) #Creamos el objeto fuente con la fuente por defecto y el tamaño 25
	texto = font.render(msg, True, color)
	pantalla.blit(texto, [ANCHURA_PANTALLA/2, ALTURA_PANTALLA/2])

def perder_partida(salir, perder):
	while perder == True:
		pantalla.fill(BLANCO)
		mensaje_por_pantalla("Has perdido presiona R para jugar otra vez o Q para salir", NEGRO)
		pygame.display.update()
		
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					salir = True
					perder = False
				if event.key == pygame.K_r:
					main()
		
	return salir, perder

# ---------------------------------------------------------------------
# Funciones del juego
# ---------------------------------------------------------------------
def serpiente(medida_bloque, lista_serpiente):
	for XY in lista_serpiente:
		pygame.draw.rect(pantalla, VERDE, [XY[0],XY[1],medida_bloque,medida_bloque]) #Imprimir serpiente
# ---------------------------------------------------------------------
# Programa Principal
# ---------------------------------------------------------------------
def main(): 
	salir = False
	perder = False
	
	#Posicion inicial del jugador
	cabeza_x = ANCHURA_PANTALLA/2
	cabeza_y = ALTURA_PANTALLA/2
	
	cabeza_x_cambio = 0
	cabeza_y_cambio = 0
	
	medida_bloque = 10
	
	lista_serpiente = []
	longitud_serpiente = 1
	
	manzanaX = round(random.randrange(0,ANCHURA_PANTALLA-medida_bloque)/10.0)*10.0 #Generar la manzana aleatoriamente teniendo en cuenta el tamaño del bloque
	manzanaY = round(random.randrange(0,ALTURA_PANTALLA-medida_bloque)/10.0)*10.0 #Si se redondea para que sea multiplo de 10 se puede conseguir que la serpiente y la manzana se crucen bien
	
	reloj = pygame.time.Clock() #Objeto reloj para definir los FPS

	while not salir: #Mientras salir no sea True se ejecuta
		
		salir,perder = perder_partida(salir, perder)

		for event in pygame.event.get(): #Eventos que hay https://www.pygame.org/docs/ref/event.html
			if event.type == pygame.QUIT: #Salir cuando se le da al boton X de la pantalla
				salir = True
			if event.type == pygame.KEYDOWN: #Si se presiona una tecla
				if event.key == pygame.K_LEFT: #Si se presiona la flecha izquierda
					cabeza_x_cambio -= medida_bloque #La posición de la cabeza_x_cambio se reduce en 10
					cabeza_y_cambio = 0 #Evitar que al cambiar la x la y no
				elif event.key == pygame.K_RIGHT:
					cabeza_x_cambio += medida_bloque
					cabeza_y_cambio = 0
				elif event.key == pygame.K_UP:
					cabeza_y_cambio -= medida_bloque
					cabeza_x_cambio = 0
				elif event.key == pygame.K_DOWN:
					cabeza_y_cambio += medida_bloque
					cabeza_x_cambio = 0

			
			if cabeza_x >= ANCHURA_PANTALLA or cabeza_x < 0 or cabeza_y >= ALTURA_PANTALLA or cabeza_y < 0: #Si el cuadrado llega a alguno de los bordes se cierra el juego
				perder = True
	
		cabeza_x += cabeza_x_cambio #Cada vuelta al for sumara el cambio de posicion a cabeza_x asi se puede mantener la tecla pulsada y se mueve
		cabeza_y += cabeza_y_cambio
		
		medida_manzana = 30
		pantalla.fill(NEGRO) #Llena el fondo del color pasado
		pygame.draw.rect(pantalla, ROJO, [manzanaX, manzanaY, medida_manzana, medida_manzana]) #Imprimir manzana
		
		cabeza_serpiente = []
		cabeza_serpiente.append(cabeza_x)#Se mete en la lista la posicion de la cabeza x y la y
		cabeza_serpiente.append(cabeza_y)
		lista_serpiente.append(cabeza_serpiente) #Se pasan las coordenadas de la serpiente a otra lista que se usara para imprimir la serpiente en la funcion de arriba
		
		if len(lista_serpiente) > longitud_serpiente: #Si la longitud de 
			del lista_serpiente[0]
		
		for segmento in lista_serpiente[:-1]: #Comprobar si la serpiente se choca con sigo misma pero excluyendo la propia cabeza
			if segmento == cabeza_serpiente:
				perder = True

		serpiente(medida_bloque, lista_serpiente)
		#pygame.draw.rect(pantalla, BLANCO, [400,100,10,10]) #Dibujar un rectangulo en la pantalla y se pone la posicion en los 2 primeros y la altura y anchura en los siguientes
		#pantalla.fill(BLANCO, rect=[200,200,50,50]) #Hace lo mismo que el anterior 
		pygame.display.update() #Actualizar pantalla
		
		if cabeza_x == manzanaX and cabeza_y == manzanaY: #Comprobar si se ha comido la manzana
			manzanaX = round(random.randrange(0,ANCHURA_PANTALLA-medida_bloque)/10.0)*10.0
			manzanaY = round(random.randrange(0,ALTURA_PANTALLA-medida_bloque)/10.0)*10.0
			longitud_serpiente += 1

		reloj.tick(FPS) #FPS para cambiar la velocidad del juego mejor no tocar FPS sino fuerzas que el bucle for se ejecute muchas veces por segundo y puede haber problema de rendimiento
	
	pygame.quit()
	quit()

if __name__ == '__main__':
	pygame.init() #Inicializar pygame
	main()
