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

coal = Material(diffuse=(0.15,0.15,0.15), spec = 5, ks = 0.02)
carrot = Material(diffuse=(0.93,0.57,0.13), spec = 5, ks = 0.02)
snow = Material(diffuse=(0.91,0.93,0.90), spec = 5, ks = 0.02)
stone = Material(diffuse=(0.60,0.60,0.60), spec = 5, ks = 0.02)
sclera = Material(diffuse=(0.86,0.88,0.85), spec = 5, ks = 0.02)

#Nieve
raytracer.scene.append(Sphere(position=(0,-1.2,-5), radius = 1.2, material = snow))
raytracer.scene.append(Sphere(position=(0,0.55,-5), radius = 0.95, material = snow))
raytracer.scene.append(Sphere(position=(0,1.94,-5), radius = 0.7, material = snow))

#Carbon
raytracer.scene.append(Sphere(position=(0,-0.8,-4), radius = 0.35, material = coal))
raytracer.scene.append(Sphere(position=(0,0.15,-4), radius = 0.25, material = coal))
raytracer.scene.append(Sphere(position=(0,1,-4), radius = 0.15, material = coal))

#Zanahoria
raytracer.scene.append(Sphere(position=(0,1.75,-4), radius = 0.20, material = carrot))

#Boca
raytracer.scene.append(Sphere(position=(-0.35,1.54,-4.15), radius = 0.075, material = stone))
raytracer.scene.append(Sphere(position=(-0.13,1.49,-4.15), radius = 0.075, material = stone))
raytracer.scene.append(Sphere(position=(0.12,1.51,-4.15), radius = 0.075, material = stone))
raytracer.scene.append(Sphere(position=(0.35,1.55,-4.15), radius = 0.075, material = stone))

#Ojos
raytracer.scene.append(Sphere(position=(0.145,2.04,-4.1), radius = 0.05, material = sclera))
raytracer.scene.append(Sphere(position=(-0.145,2.04,-4.1), radius = 0.05, material = sclera))
raytracer.scene.append(Sphere(position=(-0.145,1.95,-3.95), radius = 0.025, material = coal))
raytracer.scene.append(Sphere(position=(0.145,1.95,-3.95), radius = 0.025, material = coal))

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