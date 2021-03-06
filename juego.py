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
ROJO = (183,28,28)
VERDE = (46,125,50)
GRIS = (69,90,100)
BLANCO2 = (224,224,224)

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
FUENTE = "font/Comfortaa-Regular.ttf"
font_peque = pygame.font.Font(FUENTE,25)
font_media = pygame.font.Font(FUENTE,50)
font_grande = pygame.font.Font(FUENTE,75)

#Serpiente
img = pygame.image.load("img/snake1.png") #Cargamos la foto para la cabeza de la serpiente
img_cuerpo = pygame.image.load("img/snake2.png") #Cargamos la foto para la cabeza de la serpiente
cabeza_x_cambio = 0
cabeza_y_cambio = 0
medida_bloque = 20
direccion = "derecha"

#Manzana
medida_manzana = 30
manzana = pygame.image.load("img/manzana.png")

#Musica y sonidos
pygame.mixer.init() 
pygame.mixer.music.load("sound/musica_fondo.mp3")
sonido = pygame.mixer.Sound("sound/sonido_manzana.wav")

# --------------------------------------------------------------------- 
# Clases

# ---------------------------------------------------------------------
# Funciones generales
# --------------------------------------------------------------------- 
def objetos_texto(msg,color, medida):
	#Evaluar el tamaño de la letra
	if medida == "peque":
		superficie_texto = font_peque.render(msg, True, color)
	elif medida == "media":
		superficie_texto = font_media.render(msg, True, color)
	elif medida == "grande":
		superficie_texto = font_grande.render(msg, True, color)
	
	return superficie_texto, superficie_texto.get_rect() 

def mensaje_por_pantalla(msg,color, desplazamiento_Y=0,medida="peque"): #Funcion para generar mensajes
	superficie_texto, rectangulo_texto = objetos_texto(msg,color,medida)
	rectangulo_texto.center = (ANCHURA_PANTALLA/2), (ALTURA_PANTALLA/2)+desplazamiento_Y #Con el desplazamiento_Y se mueve el mensaje hacia abajo o arriba
	pantalla.blit(superficie_texto, rectangulo_texto)

def perder_partida(salir, perder): #Salta cuando pierdes
	while perder == True:
		pantalla.fill(GRIS) 
		mensaje_por_pantalla("Has perdido",ROJO, -200, medida="grande")
		mensaje_por_pantalla("Volver a jugar --> R",BLANCO2,75, medida = "media")
		mensaje_por_pantalla("Salir --> Q",BLANCO2, 140, medida = "media")
		pygame.display.update()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					pygame.quit()
					quit()
				if event.key == pygame.K_r:
					main()
		
	return salir, perder

def pausar(): #Funcion del menu de pausa
	pausa = True
	pygame.mixer.music.stop()
	while pausa:
		#Imprimir texto de pausa
		pantalla.fill(GRIS) #Fondo del juego
		mensaje_por_pantalla("Menu de pausa: ", ROJO, -200, medida="grande")
		mensaje_por_pantalla("Salir --> Q ", BLANCO2, -10, medida="media")
		mensaje_por_pantalla("Reanudar --> E ", BLANCO2, 40,medida="media")
		mensaje_por_pantalla("Reiniciar partida --> R ", BLANCO2, 90, medida="media")
		pygame.display.update()
		
		#Mirar que ha clicado
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.key == pygame.K_q:
				pygame.quit()
				quit()
			if event.key == pygame.K_r:
				main()
			if event.key == pygame.K_e:
				return False


def pantalla_inicio():
	inicio = True
	pantalla.fill(GRIS)
	while inicio:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					main()
				elif event.key == pygame.K_q:
					pygame.quit()
					quit()
		
		mensaje_por_pantalla("Bienvenido", ROJO, -200, medida="grande")
		mensaje_por_pantalla("El juego consiste en comer las maximas", BLANCO2,-30)
		mensaje_por_pantalla("manzanas que puedas sin chocarte contigo", BLANCO2, 10)
		mensaje_por_pantalla("mismo o los limites del campo suerte!!", BLANCO2,50)
		mensaje_por_pantalla("Jugar --> P", BLANCO2, 180)
		mensaje_por_pantalla("Salir --> Q", BLANCO2, 240)
		
		pygame.display.update()
		reloj.tick(15)



# ---------------------------------------------------------------------
# Funciones del juego
# ---------------------------------------------------------------------
def puntos(puntos):
	texto = font_peque.render("Puntos: "+ str(puntos), True, BLANCO2)
	pantalla.blit(texto, [0,0])

def serpiente(medida_bloque, lista_serpiente):
	
	#Rotar la cabeza de la serpiente
	if direccion == "derecha":
		cabeza = pygame.transform.rotate(img, 270)
		cuerpo = pygame.transform.rotate(img_cuerpo, 270)
	
	if direccion == "izquierda":
		cabeza = pygame.transform.rotate(img, 90)
		cuerpo = pygame.transform.rotate(img_cuerpo, 90)
	
	if direccion == "arriba":
		cabeza = img
		cuerpo = img_cuerpo
	
	if direccion == "abajo":
		cabeza = pygame.transform.rotate(img, 180)
		cuerpo = pygame.transform.rotate(img_cuerpo, 180)
		
	
	pantalla.blit(cabeza, (lista_serpiente[-1][0], lista_serpiente[-1][1]))
	
	#Imprimir cuerpo serpiente
	for XY in lista_serpiente[:-1]:
		pantalla.blit(cuerpo, [XY[0], XY[1], medida_bloque, medida_bloque])
		

def generarSerpiente():
	#Generar la posicion manzana aleatoriamente teniendo en cuenta el tamaño del bloque
	manzana_x = round(random.randrange(0,ANCHURA_PANTALLA-medida_bloque))
	manzana_y = round(random.randrange(0,ALTURA_PANTALLA-medida_bloque))
	
	return manzana_x,manzana_y

def movimiento_serpiente():
	global cabeza_x_cambio
	global cabeza_y_cambio
	global direccion
	
	for event in pygame.event.get(): #Eventos que hay https://www.pygame.org/docs/ref/event.html
		if event.type == pygame.QUIT: #Salir cuando se le da al boton X de la pantalla
			pygame.quit()
			quit()
		if event.type == pygame.KEYDOWN: #Si se presiona una tecla
			if event.key == pygame.K_ESCAPE:
				salir = pausar()
			elif event.key == pygame.K_LEFT:
				direccion = "izquierda"
				cabeza_x_cambio -= medida_bloque
				cabeza_y_cambio = 0
			elif event.key == pygame.K_RIGHT:
				direccion = "derecha"
				cabeza_x_cambio = medida_bloque
				cabeza_y_cambio = 0
			elif event.key == pygame.K_UP:
				direccion = "arriba"
				cabeza_y_cambio -= medida_bloque
				cabeza_x_cambio = 0
			elif event.key == pygame.K_DOWN:
				direccion = "abajo"
				cabeza_y_cambio = medida_bloque
				cabeza_x_cambio = 0

# ---------------------------------------------------------------------
# Programa Principal
# ---------------------------------------------------------------------
def main():
	global direccion
	
	salir = False
	perder = False
	
	#Posicion inicial del jugador
	cabeza_x = ANCHURA_PANTALLA/2
	cabeza_y = ALTURA_PANTALLA/2
	
	lista_serpiente = []
	longitud_serpiente = 1

	manzana_x,manzana_y = generarSerpiente() 
	
	#Musica
	pygame.mixer.music.play(-1)
	
	while not salir:
		salir,perder = perder_partida(salir, perder)
		
		movimiento_serpiente()
		
		pantalla.fill(GRIS) #Color de fondo
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
		
		if len(lista_serpiente) > longitud_serpiente:
			del lista_serpiente[0]
		
		for segmento in lista_serpiente[:-1]: #Comprobar si la serpiente se choca con sigo misma pero excluyendo la propia cabeza
			if segmento == cabeza_serpiente:
				perder = True
		
		serpiente(medida_bloque, lista_serpiente)
		
		puntos(longitud_serpiente-1) #Coge el valor -1 de la longitud de la serpiente ya que cada manzana se suma 1 y le quitamos 1 porque empieza en 1
		
		#Mirar colisiones contra la manzana
		if cabeza_x + medida_bloque > manzana_x and cabeza_x < manzana_x + medida_manzana:
			if cabeza_y + medida_bloque > manzana_y and cabeza_y < manzana_y + medida_manzana:
				manzana_x,manzana_y = generarSerpiente()
				longitud_serpiente +=1
				sonido.play() #Efecto de sonido al comerse la manzana
			elif cabeza_y + medida_bloque > manzana_y and cabeza_y + medida_bloque < manzana_y + medida_manzana:
				manzana_x,manzana_y = generarSerpiente()
				longitud_serpiente +=1
				sonido.play()
		
		pygame.display.update() #Actualizar pantalla
		reloj.tick(FPS) #FPS para cambiar la velocidad del juego mejor no tocar FPS sino fuerzas que el bucle for se ejecute muchas veces por segundo y puede haber problema de rendimiento
	
	pygame.quit()
	quit()

if __name__ == '__main__':
	pygame.init() #Inicializar pygame
	pantalla_inicio()
