from PIL import Image
import os
import csv  

#Build your polygons, Select Pixels with GIMP or Krita (Fälle wie mit Mareike Sigloch besprochen am 16.01.23, https://mitmachen.offenburg.de/offenburg/de/survey/57544)
# ##Fälle Zunsweier##
# Nur der Knick zwischen Michael-Armburster und Geroldsecker (Done: gmaps_zunsweier_knick.csv)
#lp_zunsweier_knick_light = [[1070, 509], [1092, 499], [1086, 502], [1105, 493], [1096, 465]]
# (Done): gmaps_zunsweier_knick_long.csv
#lp_zunsweier_knick_heavy = [[1101,501], [1071,508], [1077,506], [1095,443], [1111,496], [1096,449], [1087, 507], [1025, 535], [1070, 509], [1092, 499], [1086, 502], [1105, 493], [1096, 465]]

## für das Projekt Tempo-30 in Zunsweier untersuche bitte den Bereich (Michael-Armbruster Straße und Geroldsecker Str.) zwischen den beiden folgenden Koordinaten
#-	Im Norden: 48°25'44.3"N 7°57'09.4"E (48.428974, 7.952621)
#-	Im Süden: 48°25'02.3"N 7°56'32.0"E (48.417295, 7.942212)
#lp_zunsweier_gesamt_very_light = [[1237,203], [1093,431], [1102,463], [1054,515], [977,607], [728,1052]] (Done)
#lp_zunsweier_gesamt_mild = [[1237,203], [118,301], [1221,221], [1093,431], [1102,463],[1099, 473], [106,518], [1054,515], [977,607],[946,644],[726, 1076], [728,1052]] (Done)

##Fälle Stadt##
#a)Okenstrasse nördlich bis südlich mit Einmündung 
#lp_stadt_oken = [[898,158], [891,176], [885,192], [871,232], [874,244], [916,253]]
#b)bis Freiburgerplatz
#lp_freiburgerplatz = [[922,85], [921,76], [922,81], [928, 56], [951, 5]]
#c) Knoten Ag. f. Arbeit 
#lp_knoten_WWOG = [[1168, 708], [1191, 708], [1196, 709], [1184, 709], [1169, 699], [1168, 716]]
#d) 4 Strassen: Weingartenstr., Wilhelmstr., Ortenbergerstr., Grabenallee - Knoten Stadt Bückel
#lp_weingartenstr = [[1405, 653], [1394, 661], [1307, 679], [1199, 701], [1202, 706]]
#lp_ortenbergerstr = [[1473, 902], [1433, 874], [1386, 853], [1244, 751], [1225, 740], [1192, 760], [1230, 843]]
#lp_grabenallee_plus_bückel = [[1115, 738], [1076,760], [1047, 765], [995, 783], [983, 778], [935, 783], [889, 737], [860, 714]]
lp_wilhelmstr = [[1062, 428], [1080, 479], [1108, 549], [1151, 642], [1163, 683]]

#Funktion: Ziege vordifinierte Polygone vor dem Analysestart (am Referenzbild, .draw())

header = ['Date', 'Timestamp', 'Source', 'Location', 'Traffic_Color']

def generate_list_farbe(list_pixel,list_farbe,path):
    for pixel in list_pixel:
        img = Image.open(path,'r')
        rgbp = img.getpixel((pixel[0],pixel[1]))
        #fliessender Verkeher
        if rgbp == (99, 214, 104, 255):
            #print('fliessend')
            list_farbe.append('fliessend')
        #Erhöhtes Verkehrsaufkommen
        elif rgbp == (255, 151, 77, 255):
            list_farbe.append('erhoeht')
        #Sehr erhöhtes Verkehrsaufkommen
        elif rgbp == (242, 60, 50, 255):  
            list_farbe.append('sehr erhoeht')
        #Stockender Verkehr
        elif rgbp == (129, 31, 31, 255):
            list_farbe.append('stockend')
        elif rgbp == (255, 255, 255, 255) or rgbp == (241, 243, 244, 255):
            list_farbe.append('keine Daten')
    return list_farbe

 
def generate_final_color(list_farbe):
    if 'stockend' in list_farbe:
        return 'stockend'
    elif 'sehr erhoeht' in list_farbe:
        return 'sehr erhoeht'
    elif 'erhoeht' in list_farbe:
        return 'erhoeht'
    elif  'fliessend' in list_farbe:
        return 'fliessend'
    return 'keine Daten'
    


        
def iterate_files(it_path):
    for root, dirs, files in os.walk(it_path):
        for file in files:
            yield os.path.abspath(os.path.join(root, file)),file

def get_metadata(img):
    metadata=img.split('_')
    if len(metadata) == 3:
        metadata.insert(1,'stadt')
    metadata[3]=metadata[3].split('.')[0]  
    return metadata

if __name__ == '__main__':

    with open('lp_wilhelmstr.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        
        for file_path,file_name in iterate_files(r'D:\bilder\stadt-gmaps'):
            list_farbe=[]
            metadata = get_metadata(file_name)
            traffic = generate_final_color(generate_list_farbe(lp_wilhelmstr,list_farbe,file_path))    
            data = metadata[2],metadata[3],metadata[0],metadata[1],traffic
            writer.writerow(data)

    f.close()

