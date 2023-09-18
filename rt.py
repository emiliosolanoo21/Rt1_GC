from math import tan, pi
import numpy as np

class Raytracer(object):
    def __init__(self, screen):
        self.screen = screen
        _,_, self.width, self.height = screen.get_rect() #Recibe el rectangulo de la pantalla (_,_, -> x,y)
        
        self.scene = []
        self.lights = []
        
        self.camPosition = [0,0,0]
        
        self.rtViewport(0, 0, self.width, self.height)
        self.rtProyection()
        
        self.rtClearColor(0,0,0)
        self.rtColor(1,1,1)
        self.rtClear()
        
    
    def rtViewport(self,posX, posY, width, height):
        self.vpX = posX
        self.vpY = posY
        self.vpWidth = width
        self.vpHeight = height
    
    def rtProyection(self,fov=60,n=0.1):
        aspectRatio = self.vpWidth/self.vpHeight
        self.nearPlane = n
        self.topEdge = tan((fov*pi/180)/2)*self.nearPlane
        self.rightEdge = self.topEdge * aspectRatio
    
    #Color de fondo    
    def rtClearColor(self, r, g, b):
        #Recibe valores de 0 a 1
        self.clearColor = (r*255,g*255,b*255)
    
    def rtClear(self):
        #Pygame usa valores de colores de 0 a 255
        #Cada color es un Byte
        self.screen.fill((self.clearColor))
    
    #Color por default
    def rtColor(self,r,g,b):
        self.currentColor = (r*255,g*255,b*255)
    
    def rtPoint(self,x,y,color = None):
        y = self.height - y
        
        if (0<=x<self.width) and (0<=y<self.height):
            if color != None:
                color = (int(color[0]*255),
                         int(color[1]*255),
                         int(color[2]*255))
                
                self.screen.set_at((x,y), color)
            else:
                self.screen.set_at((x,y), self.currentColor)
    
    #Generador del rayo
    def rtCastRay(self,orig,dir,sceneObj = None):
        depth = float('inf')
        intercept = None
        hit = None
        
        for obj in self.scene:
            if sceneObj != obj:
                intercept = obj.ray_intersect(orig, dir)
                if intercept != None:
                        
                    if intercept.distance < depth:
                        hit = intercept
                        depth = intercept.distance
        return hit
    
    def rtRender(self):
        for x in range (self.vpX, self.vpX+self.vpWidth+1):
            for y in range (self.vpY, self.vpY+self.vpHeight+1):
                if (0<=x<self.width) and (0<=y<self.height):
                    #Pasar de coordenadas de ventana a coordenadas NDC (-1 a 1 (coords. normalizadas))
                    pX = ((x+0.5-self.vpX)/self.vpWidth)*2-1
                    pY = ((y+0.5-self.vpY)/self.vpHeight)*2-1
                    
                    pX*=self.rightEdge
                    pY*=self.topEdge
                    
                    #Crear un rayo
                    direction = (pX,pY,-self.nearPlane)
                    direction = direction/np.linalg.norm(direction)
                    
                    intercept = self.rtCastRay(self.camPosition, direction)
                    if intercept != None:
                        #Phong Reflection Model
                        #LightColor = AmbientIntensity + DiffuseIntensity + SpecularIntensity
                        #FinalColor = SurfaceColor * LightColor
                        
                        surfaceColor = intercept.obj.material.diffuse
                        ambientColor = [0,0,0]
                        diffuseColor = [0,0,0]
                        specularColor = [0,0,0]
                        
                        for light in self.lights:
                            if light.lightType == "Ambient":
                                ambientColor = [(ambientColor[i]+light.getLightColor()[i]) for i in range(3)]
                            
                            else:
                                lightDir = None
                                if light.lightType == "Directional":
                                    lightDir = [(i*-1) for i in light.direction]
                                elif light.lightType == "Point":
                                    lightDir = np.subtract(light.point, intercept.point)
                                    lightDir = lightDir / np.linalg.norm(lightDir)
                                    
                                shadowIntersect = self.rtCastRay(intercept.point, lightDir, intercept.obj)
                                
                                if shadowIntersect==None:
                                    diffuseColor = [(diffuseColor[i]+light.getDiffuseColor(intercept)[i]) for i in range(3)]
                                    specularColor = [(specularColor[i]+light.getSpecularColor(intercept, self.camPosition)[i]) for i in range(3)]
                                
                        lightColor = [(ambientColor[i]+diffuseColor[i]+specularColor[i]) for i in range(3)]  
                        
                        finalColor = [min(1,surfaceColor[i]*lightColor[i])for i in range(3)]
                        
                        self.rtPoint(x,y,finalColor)
                        