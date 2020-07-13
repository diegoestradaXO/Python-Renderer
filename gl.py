#Escritor de Imagenes BMP
#Author: Diego Estrada

# Errores comunes:
# "index out of range" puede suceder cuando el vertex esta fuera del viewport

import struct

def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(c):
    return struct.pack('=h', c)

def dword(c):
    return struct.pack('=l', c)

def color(r, g, b):
    return bytes([b,g,r])

class Render(object):
    def __init__(self):
        self.clear_color = color(0,0,0)
        self.draw_color = color(255,0,0)
    
    def glClear(self):
        self.framebuffer = [
            [self.clear_color for x in range(self.width)]
            for y in range(self.height)
        ]

    def glCreateWindow(self, width, height): #el width y height del window es el del Render()
        self.width = width
        self.height = height
        self.framebuffer = []
        self.glClear()
    
    def point(self, x,y):
        self.framebuffer[y][x] = self.draw_color

    def glInit(self):
        pass

    def glViewPort(self, x, y, width, height):
        self.x_VP = x
        self.y_VP = y
        self.width_VP = width
        self.height_VP = height

    def glClearColor(self, r, g, b):
        self.clear_color = color(int(round(r*255)),int(round(g*255)),int(round(b*255)))

    def glColor(self, r,g,b):
        self.draw_color = color(int(round(r*255)),int(round(g*255)),int(round(b*255)))

    def glVertex(self, x, y):
        xPixel = self.x_VP + int(round( self.width_VP/2 + x * self.width_VP/2))
        yPixel = self.y_VP + int(round( self.height_VP/2 + y * self.height_VP/2))
        self.point(round(xPixel),round(yPixel))

    def glFinish(self, filename):
        f = open(filename, 'bw')

        #file header
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        #image header
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))   
        f.write(dword(0))
        f.write(dword(24))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0)) 
        f.write(dword(0))

        # pixel data

        for x in range(self.width):
            for y in range(self.height):
                f.write(self.framebuffer[y][x])
        
        f.close()

r = Render()
r.glClearColor(1,0,1)
r.glColor(1,1,0)
r.glCreateWindow(100,200)
r.glViewPort(1,1,80,80)
r.glVertex(1,0)
r.glVertex(1,1)
r.glVertex(0,1)
r.glVertex(0,0)
r.glVertex(-1,-1)
r.glVertex(-1,0)
r.glVertex(0,-1)
r.glVertex(-1,1)
r.glVertex(1,-1)
r.glFinish('output.bmp')

