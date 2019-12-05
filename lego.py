#!/usr/bin/env python
# coding: utf-8

# In[157]:



from solid import *
from solid.utils import *
import viewscad

r = viewscad.Renderer(openscad_exec='C:\Program Files\OpenSCAD\openscad.exe')


# In[223]:


def lego(M,N,h=7.8):
    '''M is the length and N is the width'''
    D = 4.6
    S = 3.1 # spacing
    es = 1.2 # extra space thickness
    t = 7.4 # thickness
    cd = (S+D)
    L = cd*(M-1)
    W = cd*(N-1)
    c = cylinder(t/2,h,segments=100)
    c1 = translate([0,L,0])(c)
    y = hull()(c1,c)
    y1 = translate([W,0,0])(y)
    z = hull()(y,y1)
    c1 = cylinder(D/2,h)
    for i in range(0,M):
        c2 = (translate([0,cd*i,0])(cylinder(D/2,h*2,segments=100)))
        c1 = c1+c2
    c = c1
    for ii in range(0,N):
        c3 = (translate([cd*ii,0,0])(c1))
        c = c+c3
    final = z-c
    if L>W:
        return L, final
    else: 
        return W, final


# In[224]:


Longest,f = lego(1,5)
r.render(f)


# Part B

# In[225]:


def NEMASTANDARDS(INPUT):
    NEMAHeight = {'NEMA 8' : 20.32,'NEMA 11' : 27.94,'NEMA 14' : 35.56,'NEMA 17' : 43.18,'NEMA 23' : 58.42,'NEMA 34' : 86.36,'NEMA 42' : 106.68}
    NEMAboltSpacing = {'NEMA 8' : 16,'NEMA 11' : 23,'NEMA 14' : 26,'NEMA 17' : 31,'NEMA 23' : 47.14,'NEMA 34' : 69.7,'NEMA 42' : 88.9}
    NEMAShaftClearance = {'NEMA 8' : 6,'NEMA 11' : 7,'NEMA 14' : 7,'NEMA 17' :7,'NEMA 23' : 9,'NEMA 34' : 11,'NEMA 42' : 20}
    NEMAPilotClearance = {'NEMA 8' : 1.5,'NEMA 11' : 2,'NEMA 14' : 2,'NEMA 17' : 2,'NEMA 23' : 1.6,'NEMA 34' : 1.6,'NEMA 42' : 1.6}
    NEMABoltDiameter = {'NEMA 8' : 3.1,'NEMA 11' : 4.1,'NEMA 14' : 4.1,'NEMA 17' : 3.2,'NEMA 23' : 5.1,'NEMA 34' : 5.9,'NEMA 42' : 7.1}
    NEMAPilotDiameter = {'NEMA 8' : 15,'NEMA 11' : 22,'NEMA 14' : 22,'NEMA 17' : 22,'NEMA 23' : 38.1,'NEMA 34' : 73,'NEMA 42' : 55.5244}
    NEMAShaftLength = {'NEMA 8' : 24.003,'NEMA 11' : 24.003,'NEMA 14' : 24.003,'NEMA 17' : 24.003,'NEMA 23' : 20.574,'NEMA 34' : 31.75,'NEMA 42' : 35.052}
    NEMAShaftDiameter = {'NEMA 8' : 4,'NEMA 11' : 5,'NEMA 14' : 5,'NEMA 17' : 5,'NEMA 23' : 6.35,'NEMA 34' : 9.5,'NEMA 42' : 16}
    dimensions = [NEMAHeight[INPUT],NEMAboltSpacing[INPUT],NEMAShaftClearance[INPUT],NEMAPilotClearance[INPUT], NEMABoltDiameter[INPUT],NEMAPilotDiameter[INPUT], NEMAShaftLength[INPUT],NEMAShaftDiameter[INPUT]]
    return dimensions


# In[226]:


def NEMAMount(func,Standard):
    '''func pulls in the standard, Standard is the value of the NEMA standard is defined by NEMA designation '''
    d = NEMASTANDARDS(Standard)
    base = cube([d[0],d[0],d[3]*2])
    hole = translate([d[0]/2,d[0]/2,0])(cylinder(d[2]/2,d[3]*3,segments=100))
    hole2 = translate([d[0]/2,d[0]/2,0])(cylinder(d[5]/2,d[3],segments=100))
    s = base-hole-hole2
    #base with hole till here
    sp = translate([(-d[0]+d[1])/2,(-d[0]+d[1])/2,0])(s)
    # Shifts object
    mountingHole = cylinder(d[4]/2,d[3]*3,segments=100)
    s = sp-mountingHole
    sn1 = translate([d[1],0,0])(mountingHole)
    sn2 = translate([0,d[1],0])(mountingHole)
    sn3 = translate([d[1],d[1],0])(mountingHole)
    snew = s-sn1-sn2-sn3
    s = translate([-(-d[0]+d[1])/2,-(-d[0]+d[1])/2,0])(snew)
    s = translate([7.4/2,7.4/2,0])(s)
    number = int(d[0]/4/2)
    long,add = lego(1,number,h=(d[3]*2))
    add = translate([7.4/2+(d[0]-long)/2,0,0])(add)
    add1 = rotate(90,[0,0,1])(add)
    add2 = translate([0,d[0]+7.4,0])(add)
    add3 = translate([d[0]+7.4,0,0])(add1)
    s = s+add+add1+add2+add3
    r.render(s)
    return s

snew = NEMAMount(NEMASTANDARDS,'NEMA 17')


# Part C

# In[229]:


def adaptor(func,Standard):
    '''func is the NEMA standard function and Standard is the NEMA standard to use for a look up'''
    d = NEMASTANDARDS(Standard)
    #index 7 is the shaft diameter and index 6 is the shaft length
    c = cylinder(d[7],d[6]+d[7]/4,segments=500)
    c2 = cylinder(d[7]/2,d[6],segments=500)
    c1 = translate([0,0,d[6]+d[7]/4])(cylinder(4.6/2,7.8*1.5,segments=500))
    s = c-c2+c1
    return s
r.render(adaptor(NEMASTANDARDS,'NEMA 17'))


# In[199]:


# generate an scad file the generate to stl
def exportScadFile(obj):
    import os
    cwd = os.getcwd()
    print(cwd)
    output = scad_render(obj).strip().replace('\n','').replace("\t","")
    return output


# In[230]:


exportScadFile(adaptor(NEMASTANDARDS,'NEMA 17'))


# In[ ]:




