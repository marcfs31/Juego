#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import pygame
import random


# Constantes
# --------------------------------------------------------------------- 

##Colores
BLANCO = (255,255,255)
NEGRO = (0,0,0)
ROJO = (255,0,0)
VERDE = (0,150,0)

##Tamaño pantalla
ANCHURA_PANTALLA = 800
ALTURA_PANTALLA = 600
pantalla = pygame.display.set_mode((ANCHURA_PANTALLA,ALTURA_PANTALLA)) #Se crea el objeto pantalla con el tamaño en una tupla

#Titulo del juego
pygame.display.set_caption("Juego de la serpiente")

#Reloj
reloj = pygame.time.Clock() #Objeto reloj para definir los FPS
FPS = 15

#Fuente
pygame.font.init()
FUENTE = "Comfortaa-Regular.ttf"
font = pygame.font.Font(FUENTE,25)

#Serpiente
img = pygame.image.load("snake1.png") #Cargamos la foto para la cabeza de la serpiente
cabeza_x_cambio = 10
cabeza_y_cambio = 0
medida_bloque = 20
direccion = "derecha"

#Manzana
medida_manzana = 30
manzana = pygame.image.load("manzana.png")

# --------------------------------------------------------------------- 
# Clases

# ---------------------------------------------------------------------
# Funciones generales
# --------------------------------------------------------------------- 
def objetos_texto(msg,color):
	superficie_texto = font.render(msg, True, color)
	return superficie_texto, superficie_texto.get_rect() 

def mensaje_por_pantalla(msg,color): #Funcion para generar mensajes
	superficie_texto, rectangulo_texto = objetos_texto(msg,color)
	rectangulo_texto.center = (ANCHURA_PANTALLA/2), (ALTURA_PANTALLA/2)
	pantalla.blit(superficie_texto, rectangulo_texto)

def perder_partida(salir, perder):
	while perder == True:
		pantalla.fill(BLANCO)
		mensaje_por_pantalla("Has perdido presiona R para jugar otra vez o Q para salir", NEGRO)
		pygame.display.update()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				salir = True
				perder = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					salir = True
					perder = False
				if event.key == pygame.K_r:
					main()
		
	return salir, perder

def pausar(pausa):
	while pausa == True:
		pantalla.fill(BLANCO)
		mensaje_por_pantalla("Menú de pausa: ", NEGRO)
		mensaje_por_pantalla("Salir --> Q ", NEGRO)
		mensaje_por_pantalla("Reanudar --> E ", NEGRO)
		mensaje_por_pantalla("Reiniciar partida --> R ", NEGRO)
		pygame.display.update()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				salir = True
				perder = False
			if event.key == pygame.K_q:
				salir = True
				perder = False
			if event.key == pygame.K_r:
				main()
			if event.key == pygame.K_e:
				pausa = False
# ---------------------------------------------------------------------
# Funciones del juego
# ---------------------------------------------------------------------
def serpiente(medida_bloque, lista_serpiente):
	
	#Rotar la cabeza de la serpiente
	if direccion == "derecha":
		cabeza = pygame.transform.rotate(img, 270)
		
	if direccion == "izquierda":
		cabeza = pygame.transform.rotate(img, 90)
		
	if direccion == "abajo":
		cabeza = pygame.transform.rotate(img, 180)
		
	if direccion == "arriba":
		cabeza = img
	
	pantalla.blit(cabeza, (lista_serpiente[-1][0], lista_serpiente[-1][1]))
	
	for XY in lista_serpiente[:-1]:
		pygame.draw.rect(pantalla, VERDE, [XY[0],XY[1],medida_bloque,medida_bloque]) #Imprimir serpiente
		

def movimiento_serpiente():
	global cabeza_x_cambio
	global cabeza_y_cambio
	#Problema que al reiniciar partida la serpiente se auto mueve es algo del cabeza_xy_cambio que no se reinicia
	
	for event in pygame.event.get(): #Eventos que hay https://www.pygame.org/docs/ref/event.html
		if event.type == pygame.QUIT: #Salir cuando se le da al boton X de la pantalla
			salir = True
		
		if event.type == pygame.K_ESCAPE:
			pausar(pausa = True)
			
		if event.type == pygame.KEYDOWN: #Si se presiona una tecla
			if event.key == pygame.K_LEFT: #Si se presiona la flecha izquierda
				direccion == "izquierda"
				cabeza_x_cambio -= medida_bloque #La posición de la cabeza_x_cambio se reduce en 10
				cabeza_y_cambio = 0 #Evitar que al cambiar la x la y no
			elif event.key == pygame.K_RIGHT:
				direccion == "derecha"
				cabeza_x_cambio += medida_bloque
				cabeza_y_cambio = 0
			elif event.key == pygame.K_UP:
				direccion == "arriba"
				cabeza_y_cambio -= medida_bloque
				cabeza_x_cambio = 0
			elif event.key == pygame.K_DOWN:
				direccion == "abajo"
				cabeza_y_cambio += medida_bloque
				cabeza_x_cambio = 0
			

# ---------------------------------------------------------------------
# Programa Principal
# ---------------------------------------------------------------------
def main(): 
	global direccion
	
	salir = False
	perder = False
	pausa = False
	
	#Posicion inicial del jugador
	cabeza_x = ANCHURA_PANTALLA/2
	cabeza_y = ALTURA_PANTALLA/2
	
	lista_serpiente = []
	longitud_serpiente = 1

	manzana_x = round(random.randrange(0,ANCHURA_PANTALLA-medida_bloque)) #Generar la manzana aleatoriamente teniendo en cuenta el tamaño del bloque
	manzana_y = round(random.randrange(0,ALTURA_PANTALLA-medida_bloque)) #Si se redondea para que sea multiplo de 10 se puede conseguir que la serpiente y la manzana se crucen bien

	while not salir:
		salir,perder = perder_partida(salir, perder)
		
		movimiento_serpiente()
		
		pausar(pausa) #No va
		
		pantalla.fill(NEGRO) #Llena el fondo del color pasado
		pantalla.blit(manzana,(manzana_x, manzana_y)) #Imprimrir imagen de manzana
		#pygame.draw.rect(pantalla, ROJO, [, medida_manzana, medida_manzana]) #Imprimir manzana
		
		if cabeza_x >= ANCHURA_PANTALLA or cabeza_x < 0 or cabeza_y >= ALTURA_PANTALLA or cabeza_y < 0: #Si el cuadrado llega a alguno de los bordes pierdes
			perder = True
	
		cabeza_x += cabeza_x_cambio #Cada vuelta al for sumara el cambio de posicion a cabeza_x asi se puede mantener la tecla pulsada y se mueve
		cabeza_y += cabeza_y_cambio
		
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
		
		#Mirar colisiones contra la manzana
		if cabeza_x + medida_bloque > manzana_x and cabeza_x < manzana_x + medida_manzana:
			if cabeza_y + medida_bloque > manzana_y and cabeza_y < manzana_y + medida_manzana:
				manzana_x = round(random.randrange(0,ANCHURA_PANTALLA-medida_bloque))
				manzana_y = round(random.randrange(0,ALTURA_PANTALLA-medida_bloque))
				longitud_serpiente +=1
				
		pygame.display.update() #Actualizar pantalla
		reloj.tick(FPS) #FPS para cambiar la velocidad del juego mejor no tocar FPS sino fuerzas que el bucle for se ejecute muchas veces por segundo y puede haber problema de rendimiento
	
	pygame.quit()
	quit()

if __name__ == '__main__':
	pygame.init() #Inicializar pygame
	main()
