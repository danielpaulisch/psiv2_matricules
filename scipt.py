import sys
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import os
from skimage.segmentation import clear_border
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'
""" 
assert len(sys.argv)>1, "No s'ha passat imatge"
imatge=sys.argv[1]"""
imatge='Imatges\\matricula_10.jpg'
path = os.getcwd()
carpeta_dades="\\"+str(imatge)

path+=carpeta_dades



img =  cv.imread(path)

img_gris = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
b,g,r = cv.split(img)
imagen_b=b*0.6>img_gris
#imagenes.append( img_gris)




median = cv.medianBlur(img_gris, 3)
ret, th = cv.threshold(median, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)
kernel = np.ones((5,5), np.uint8)
opening = cv.morphologyEx(th, cv.MORPH_OPEN, kernel)
edge_touching_removed = clear_border(opening)
contours, hierarchy = cv.findContours(edge_touching_removed, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
imagen_edge_removed=edge_touching_removed
#


median = cv.medianBlur(imagen_edge_removed, 3)
ret, th = cv.threshold(median, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)
kernel = np.ones((3,3), np.uint8)
img_erosion = cv.erode(th, kernel, iterations=4)
opening = cv.morphologyEx(th, cv.MORPH_ERODE,  np.ones((1,30), np.uint8))
imagen_opening=opening

#
img_erosion = cv.erode(imagen_opening, kernel, iterations=7)
img_dilation = cv.dilate(img_erosion, kernel, iterations=7)
img_dilation = cv.dilate(img_dilation, np.ones((2,9), np.uint8), iterations=15)
img_dilation = cv.dilate(img_dilation, kernel, iterations=5)

contour,hier = cv.findContours(img_dilation,cv.RETR_CCOMP,cv.CHAIN_APPROX_SIMPLE)

for cnt in contour:
    cv.drawContours(img_dilation,[cnt],0,255,-1)

gray = cv.bitwise_not(img_dilation)

kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(3,3))
res = cv.morphologyEx(gray,cv.MORPH_OPEN,kernel)
res = cv.bitwise_not(res)

imagenes_cnt=res



comb=imagenes_cnt*imagen_b

comb = cv.erode(comb, kernel, iterations=5)
comb = cv.dilate(comb, kernel, iterations=5)
comb = cv.erode(comb, kernel, iterations=5)
comb = cv.dilate(comb, kernel, iterations=5)

imagenes_combinadas=comb
#


cnts,_=cv.findContours(cv.Canny(imagenes_cnt,100,200),cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
#

    
contornos_millor=cnts[0]
area_max=0
no_entrat=True
for c in cnts:
    area = cv.contourArea(c)
    coord = cv.boundingRect(c)
    imagen_recortada = imagenes_combinadas[coord[1]:coord[1]+coord[3],coord[0]:coord[0]+coord[2]]
    
    if np.sum(imagen_recortada)>0 and area>area_max:#len(approx)==4 and area>4000:
        area_max=area
        contornos_millor=c
        no_entrat=False

if no_entrat:     
    area_max=0
    for c in cnts:
        area = cv.contourArea(c)
        coord = cv.boundingRect(c)
        imagen_recortada = imagenes_combinadas[coord[1]:coord[1]+coord[3],coord[0]:coord[0]+coord[2]]
        
        if area>area_max:#len(approx)==4 and area>4000:
            area_max=area
            contornos_millor=c      


#



epsilon = 0.02*cv.arcLength(contornos_millor,True)
approx = cv.approxPolyDP(contornos_millor,epsilon,True)
#print(len(approx))
x,y,w,h = cv.boundingRect(approx)
coord=(x,y,w,h)  
rec = cv.rectangle(img//255,(x,y),(x+w,y+h),(255,255,255),2)
ll_matricula=rec




    
imagen_recortada = img_gris[coord[1]:coord[1]+coord[3],coord[0]:coord[0]+coord[2]]
#ll_recortadas.append(imagen_recortada)


def comprovador(texte):
    if len(texte)==7:
        if texte[0] in ("1234567890"):
            if texte[1] in ("1234567890"):
                if texte[2] in ("1234567890"):
                    if texte[3] in ("1234567890"):
                        if texte[4] in ("WRTYPSDFGHJKLZXCVBNM"):
                            if texte[5] in ("WRTYPSDFGHJKLZXCVBNM"):
                                if texte[6] in ("WRTYPSDFGHJKLZXCVBNM"):
                                    return True
    return False

def netejar_lectura(text):
    
    
    #separa per \n ?
        #identificar el punt mig entre nombres i lletres
        # tirar cap a la esquerra i dreta
        # comprovar
    matricula_bona=False
    matricula = ""
    uncleared_ll = list(text.lower())
    ll=[]
    for l in uncleared_ll:
        if l in ("1234567890wrtypsdfghjklzxcvbnm"):
            ll.append(l)
    
    mitjos=[]
    for (x,letra) in enumerate(ll[:-1]):
        if letra in ("1234567890")and x<len(ll):
            if ll[x+1] in ("wrtypsdfghjklzxcvbnm"):
                mitjos.append(x)

    for punt in mitjos:
        try:
            if ll[punt-1] in ("1234567890"):
                if ll[punt-2] in ("1234567890"):
                    if ll[punt-3] in ("1234567890"):
                        if ll[punt+2] in ("wrtypsdfghjklzxcvbnm"):
                            if ll[punt+3] in ("wrtypsdfghjklzxcvbnm"):
                                matricula_bona=True
                                matricula=ll[punt-3:punt+4]
                                matricula=''.join(matricula).upper()
        except IndexError:
            pass
            #pass

    if not matricula_bona:
        count = 0
        ll = list(text.lower())
        matricula = ""

        for letra in ll:
            if count < 4:
                if letra in ("1234567890"):
                    count += 1
                    matricula += letra
                else:
                    count = 0
            elif count < 7:
                if letra in ("wrtypsdfghjklzxcvbnm"):
                    count += 1
                    matricula += letra.upper()
            



    return matricula

def girar(imagen_recortada):

    gray = cv.bitwise_not(imagen_recortada)
    thresh = cv.threshold(gray, 0, 255,	cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
    thresh = 255 - thresh
    

    cnts,_=cv.findContours(cv.Canny(thresh,100,200),cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
    contornos_millor=cnts[0]
    area_max=0
    for c in cnts:
        area = cv.contourArea(c)
        if area>area_max:#len(approx)==4 and area>4000:
            area_max=area
            contornos_millor=c
            
    angle  = cv.minAreaRect(contornos_millor)[-1]

    if angle < -45:
        angle =  (90 + angle)
        
    
    else:
        angle = -( 90 - angle)
        

    (h, w) = imagen_recortada.shape[:2]
    center = (w // 2, h // 2)
    M = cv.getRotationMatrix2D(center, -angle, 1.0)
    rotated = cv.warpAffine(imagen_recortada, M, (w, h), flags=cv.INTER_CUBIC, borderMode=cv.BORDER_REPLICATE)
    return rotated




text = pytesseract.image_to_string(imagen_recortada,config='--psm 11')


resultat = netejar_lectura(text)



if not comprovador(resultat):
    girada=girar(imagen_recortada)#girar imatge
    text = pytesseract.image_to_string(girada,config='--psm 11')#llegir
    text_netejat=netejar_lectura(text)#netejar
    if comprovador(text_netejat):#compara
        resultat=text_netejat#substituiir si millor
    elif len(text_netejat)>len(resultat):#compara
        resultat=text_netejat#substituiir si millor
    else:
        pass   


print(resultat)

    
    