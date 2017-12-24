# -*- coding: utf-8 -*-
import os
from lxml import etree
import cv2
import time
from natsort import natsorted

Xml_file="Xml"
Image_file="Images"
format_img="jpg"
ips_fps=10

files=natsorted(os.listdir(Xml_file), key=lambda y: y.lower())

for xml in files:
    tree = etree.parse(Xml_file+"/"+xml)
    objects=[]
    for object in tree.xpath("/annotation/object"):
        objects.append(object.xpath("name")[0].text)
        for coords in object.xpath("bndbox"):
            objects.append(coords[0].text)
            objects.append(coords[1].text)
            objects.append(coords[2].text)
            objects.append(coords[3].text)

    image=cv2.imread(Image_file+"/"+xml[:-3]+format_img)

    cv2.putText(image, Image_file+"/"+xml[:-3]+format_img, (0,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
    for i in range(len(objects) // 5):
        if objects[i * 5] == 'hand':
            cv2.rectangle(image,(int(objects[i * 5 + 1]), int(objects[i * 5 + 2])), (int(objects[i * 5 + 3]), int(objects[i * 5 + 4])),(0,255,0))
        elif objects[i * 5] == 'fist':
            cv2.rectangle(image,(int(objects[i * 5 + 1]), int(objects[i * 5 + 2])), (int(objects[i * 5 + 3]), int(objects[i * 5 + 4])),(0,0,255))
        else:
            cv2.rectangle(image,(int(objects[i * 5 + 1]), int(objects[i * 5 + 2])), (int(objects[i * 5 + 3]), int(objects[i * 5 + 4])),(255,0,0))

    if len(objects)==0:
        print("this file does not contain objects : ",xml[:-3]+format_img)

    cv2.imshow("image",image)
    time.sleep(1/ips_fps)
    if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
        break

