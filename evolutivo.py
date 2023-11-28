import random as rm
import math as mt
import tkinter as tk>
from tkinter import font

#formulas fisicas
def polar (r,direction):
    y = r*mt.sin(mt.radians(direction))
    x = r*mt.cos(mt.radians(direction))
    return x, y    

def time(angle, speed):
    time =  ((2*speed)/9.81)*mt.sin(mt.radians(angle*2))
    return abs(time)

def distance(x1, y1, x2, y2):
    de = mt.sqrt((mt.pow((x2-x1), 2)) + (mt.pow((y2-y1), 2)))
    return de

#formulas de bitsu.,.p,.p
def binario(binario):
    posicion = 0
    decimal = 0
    binario = binario[::-1]
    for digito in binario:
        multiplicador = 2**posicion
        decimal += int(digito) * multiplicador
        posicion += 1
    return decimal

def generar_cadena_binaria(longitud):
    cadena = []
    for _ in range(longitud):
        bit = rm.choice([0, 1])
        cadena.append(bit)
    return cadena

#objetos
class target:
     def __init__(this, positionx, positiony):
        this.positionx = positionx
        this.positiony = positiony
    
class tank:
    def __init__(this, positionx, positiony):
        this.chain = 0
        this.positionx = positionx
        this.positiony = positiony
        this.positionz = 0
        this.angle = 0
        this.aimx = 0
        this.aimy = 0
        this.time = 0
        this.direction = 0
        this.speed = 0
        
    def shoot(self, angle, speed, direction):
        speed = speed + 10
        xmax =  ((speed*speed)*mt.sin(mt.radians(angle*2)))/9.81
        x, y = polar(xmax, direction)
        x += self.positionx 
        y += self.positiony 
        self.time = time(angle, speed)
        self.aimx = x
        self.aimy = y
        self.direction = direction
        self.angle = angle
        self.speed = speed   
        

#generacion de individuos
def single():
    bc = generar_cadena_binaria(43)
    a = binario(bc[:9])
    b = binario(bc[10:19])
    c = binario(bc[20:28])
    d = binario(bc[29:37])
    e = binario(bc[38:])
    if(bc[19] == 0):
        c *= -1 
    if(bc[28] == 0):
        d *= -1
    guy = tank(c, d)
    guy.shoot(a, e, b)
    guy.chain = bc
    return guy 
def individual(bc):
    a = binario(bc[:9])
    b = binario(bc[10:19])
    c = binario(bc[20:28])
    d = binario(bc[29:37])
    e = binario(bc[38:])
    if(bc[19] == 0):
        c *= -1 
    if(bc[28] == 0):
        d *= -1
    guy = tank(c, d)
    guy.shoot(a, e, b)
    guy.chain = bc
    return guy 
def population(size):
    guy = []
    for i in range(size):
        guy.append(single())
    return guy

def targetmaker():
    targetA =  target(rm.randint(0,264),rm.randint(0,264))
    return targetA


#evaluacion
def assess(population, target):
    distances = []
    for i in range(len(population)):
        distances.append(distance(population[i].aimx, population[i].aimy, target.positionx,target.positiony))     
        distances[i] = 1/(distances[i]+1)
    return distances

def fit(assess):
    p =  []
    total = 0
    for i in range(len(assess)):
        total += assess[i]
    for i in range(len(assess)):
        p.append(assess[i]/total)
    return p

#seleccion de los mejores
def select(population, fit):
    sub2, sub = 0,0 
    total_fitness = sum(fit)
    probabilities = [f / total_fitness for f in fit]
    sub = rm.choices(population, probabilities)[0]
    while True:
        sub2 = rm.choices(population, probabilities)[0]
        if sub2 != sub:
            break
    return sub, sub2
    
#modificacion
def cross(ind, ind2):
    n = len(ind.chain)
    point = rm.randint(0,n)
    desc1 = individual(ind.chain[0:point] + ind2.chain[point:])
    desc2 = individual(ind2.chain[0:point] + ind.chain[point:])
    return desc1, desc2

def mutation(ind):
    point = rm.randint(0,len(ind.chain) - 1)
    des = ind.chain
    if(des[point] == 0):
        des[point] = 1
    else:
        des[point] = 0
    indn = individual(des)
    return indn



def _AE(size, cicles):
    global resultado
    global trgtx
    global trgty
    trgt = targetmaker()
    trgtx = "El blanco está en: " + str(trgt.positionx)
    trgty =  str(trgt.positiony)
    pption = population(size)
    check = False
    print("El objetivo esta en x:", trgt.positionx, " y:", trgt.positiony, sep = "")
    for i in range(cicles):
        ev = assess(pption, trgt)
        ft = fit(ev)
        npopulation = []
        for j in range(int(size/2)):
            ind, ind2 = select(pption, ft)
            ind, ind2 = cross(ind, ind2)
            ind2 = mutation(ind2)
            npopulation.append(ind)
            npopulation.append(ind2)
        pption = npopulation
        pption = npopulation  
    for i in range(size):
        if (ev[i] > .9 ):
                definitive = npopulation[i]
                check = True
                break
    if(check == True):
        resultado = "El tanque de la posición x:" + str(definitive.positionx)[:4] + " y:" + str(definitive.positiony)[:4] +  "\nDispara en dirección " + str(definitive.direction) + " con un ángulo de " + str(definitive.angle) + " a una velocidad de " + str(definitive.speed)[:4] + " m/s^2 \nAcertando a los " + str(definitive.time)[:4]  + " segundos en x:" + str(definitive.aimx)[:4]  + " y:" + str(definitive.aimy)[:4]  + "\n KAAAABOOOOOOOOOM"
        
    else:   
        resultado = "No se han encontrado un tanque, pruebe aumentar los ciclos o la poblacion"
    salidaFinal.config(text=resultado)
    blanco.config(text=trgtx + " " + trgty)



#interfaz grafica

    #ventana
ventana = tk.Tk()
ventana.title("Guerra de tanques")
ventana.geometry("1080x540")

    #salida
resultado = "------"
trgtx = ""
trgty = ""


    #etiqueta
label = tk.Label(ventana, text="Al presionar el boton el programa generara una punto al que se tiene que disparar, \n luego de esto generara de forma automatica tanques al azar, \n evaluara los tanques que se acerquen más al punto, los reproducira y generaran descendencia, \n al final devolvera algún tanque que haya acertado",
                 width=100, height=10, 
                 font=font.Font(family="Arial", size=12))

    #escritura
etiqueta = tk.Label(ventana, text="Ingrese la poblacion deseada")
campo_entrada = tk.Entry(ventana)
etiqueta2 = tk.Label(ventana, text="Ingrese los ciclos deseados")
campo_entrada2 = tk.Entry(ventana)

    #boton
boton = tk.Button(ventana, text="Generar la población", 
                  font=font.Font(family="Arial", size=12, weight="bold"), 
                  command=lambda: _AE(int(campo_entrada.get()), int(campo_entrada2.get())))
blanco = tk.Label(ventana, text= trgtx + trgty)
salidaFinal = tk.Label(ventana, text=resultado, font=font.Font(family="Arial", size=12))

                 
    #widgets
label.pack()
etiqueta.pack()
campo_entrada.pack()
etiqueta2.pack()
campo_entrada2.pack()
boton.pack()
blanco.pack()
salidaFinal.pack()


    #bucle
ventana.mainloop()