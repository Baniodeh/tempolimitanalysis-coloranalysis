from PIL import Image
import os
#import numpy as np
#import cv2

#Hier später Polygon - Class

#Wählbar Rechteck Poylgon 
#stadt-bmaps
#poly1= [[1000,1070],[830,900]]
#poly2 = [[24, 29], [779, 831]]
#ploy3 = [[], []]
#stadt-gmaps
poly1=[[591, 646],[326, 386]]
#poly2 = [[88, 136],[848, 914]]
#zunsweier-bmaps
#poly1 = [[], []]
#poly2 = [[660, 803],[220, 310]]
#zunsweier-gmaps
#poly1 = [[329, 586], [302, 440]]
#poly2 = [[529, 737],[175, 308]]

# Funktion: Zeige das gewnünschte Polygon vor dem Start auf der Karte (Referenzimage und einmal, .draw())
#def draw_polygon(img1, poly):
    #Erstellen Kopie des gewünschten Bildes
    #img = Img1.copy()
    #Verwandeln das Polygon in eine Liste von Punkten (numpy)
    #points = np.array(poly, npint32)
    #Zeichen das Poylgon in schwarz auf das Bild 
    #cv2.polylines(img, [points], True, (0,0,0), thickness = 2)

   #Vergleiche ausgewählte Pixels in allen Bildern mit dem ausgewähltem Referenzbild. Gebe rgb als zusätzlicher Indiz!
   #Funktion: Zeige exakt die Unterschiede und in welchen Prozenten ...

# Create the difference mask
#diff_mask = cv2.bitwise_xor(img1, img2)
# Count the number of non-zero pixels in the mask
#diff_count = cv2.countNonZero(diff_mask)
# Calculate the percentage of differences
#total_pixels = img1.shape[0] * img1.shape[1]
#diff_percentage = (diff_count / total_pixels) * 100

def compare_pixels(img1,img2,poly):
    x=poly[0][0]
    y=poly[1][0]
    for x in range(poly[0][0],poly[0][1]+1,1):
        for y in range(poly[1][0],poly[1][1]+1,1):
            if img1.getpixel((x, y)) != img2.getpixel((x, y)):
                return False  
    return True    
#Öffne aller Bilder zum Vergelichen
def iterate_files(it_path):
    for root, dirs, files in os.walk(it_path):
        for file in files:
           yield os.path.abspath(os.path.join(root, file)),file
#Achtung bei der Wahl des Polygons oben, ändere die Eingabe in if compare_piexels(imgs, polygons)
if __name__ == '__main__':
    img1 = Image.open(r'D:\bilder\stadt-gmaps\gmaps_01.10.2022_0000.png','r')
    #öffne das Bild
    #cv2.imshow('Image with Polygon', img)
    #Warte auf Benutzereingabe
    #cv2.waitkey(0)
    #Schließe das Bild
    #cv2.destroyAllwindows()
    namen=[]
    for file_path,file_name in iterate_files(r'D:\bilder\stadt-gmaps'):
        img2 = Image.open(file_path,'r')
        if compare_pixels(img1,img2,poly1) == False:
               namen.append(file_name)
#Gebe entweder eine Liste aller nicht gleichen Bilder (zum Referenzbild) oder die Anzahl!
    #print(namen)
# Funktion: Zeige in Prozent die Abweichung zum Referenzbild, definiere Toleranz!
    print(len(namen))
#print("Difference percentage:", diff_percentage)
