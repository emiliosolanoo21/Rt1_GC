import numpy as np

class Intercept(object):
    def __init__(self, distance, point, normal, obj):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.obj = obj

class Shape(object):
    def __init__(self,position,material):
        self.position = position
        self.material = material

    def ray_intersect(self,orig,dir):
        return None

class Sphere(Shape):
    def __init__(self,position,radius,material):
        self.radius = radius
        super().__init__(position,material)
        
    def ray_intersect(self, orig, dir):
        l = np.subtract(self.position, orig)
        lengthL = np.linalg.norm(l)
        tca = np.dot(l,dir)
        
        #if radius < d: no hay contacto (False)
        #if radius > d: si hay contacto (True)
        d = (lengthL**2 - tca**2)**0.5
        if d > self.radius:
            return None
        
        thc = (self.radius**2 - d**2)**0.5
        t0 = tca - thc
        t1 = tca + thc
        
        if t0<0:
            t0 = t1
        if t0<0:
            return None
        
        #P = O+D*t0
        p = np.add(orig,t0*np.array(dir))
        normal = np.subtract(p,self.position)
        normal = normal/np.linalg.norm(normal)
        
        return Intercept(distance = t0,
                         point = p,
                         normal = normal,
                         obj = self)
        