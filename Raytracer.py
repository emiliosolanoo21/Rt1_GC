import pygame
from pygame.locals import * 
from rt import Raytracer
from figures import *
from lights import *
from materials import *

width = 256
height = 256

pygame.init()

screen = pygame.display.set_mode((width,height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

raytracer = Raytracer(screen)
raytracer.rtClearColor(0.25,0.45,0.95)

coal = Material(diffuse=(0.25,0.25,0.25), spec = 256,  ks = 0.1)
carrot = Material(diffuse=(0.93,0.57,0.13), spec = 50,  ks = 0.3)
snow = Material(diffuse=(0.91,0.93,0.90), spec = 5, ks = 0.02)
stone = Material(diffuse=(0.60,0.60,0.60), spec = 20, ks = 0.01)
sclera = Material(diffuse=(0.86,0.88,0.85), spec = 20, ks = 0.01)

#Nieve
raytracer.scene.append(Sphere(position=(0,-1.2,-5), radius = 1.2, material = snow))
raytracer.scene.append(Sphere(position=(0,0.55,-5), radius = 0.95, material = snow))
raytracer.scene.append(Sphere(position=(0,1.94,-5), radius = 0.7, material = snow))

#Carbon
raytracer.scene.append(Sphere(position=(0,-0.8,-4), radius = 0.35, material = coal))
raytracer.scene.append(Sphere(position=(0,0.15,-4), radius = 0.25, material = coal))
raytracer.scene.append(Sphere(position=(0,1,-4), radius = 0.15, material = coal))

#iluminacion minima del ambiente
raytracer.lights.append(AmbientLight(intensity=0.1))
raytracer.lights.append(DirectionalLight(direction=(1,-1,-2), intensity=0.95))
raytracer.lights.append(PointLight(point=(2.5,0,-5), intensity=1, color= (1,1,1)))


isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning=False
    
    raytracer.rtClear()
    raytracer.rtRender()
    pygame.display.flip()
                
pygame.quit()           