import random
import tkinter
from PIL import Image, ImageTk
import os
import cv2
import numpy as np
import writexml

# we provide paths to our files
img_file = "Images" # this is the file where are stored our pictures
csv_file = "listing.csv" # this is a csv file where we store all positions
xml_file = "Xml" # this is the file where all Xmls will be created

# We create our variables.
exist=os.path.isfile(csv_file) 
fichiercoord = open(csv_file, "a")
if (exist==False):
    fichiercoord.write("filename,width,height,class,xmin,ymin,xmax,ymax,class\n")
listimg = os.listdir(img_file)
total_img=len(listimg)
for i in os.listdir(xml_file):
    listimg.remove(i.split('.')[0] + ".jpg")
random.shuffle(listimg)
if len(listimg)==0:
    print("aucun fichier à traiter.")
    exit
position = 0
debut = [0, 0]
fin = [40, 40]
mains = []

# We create our window
window = tkinter.Tk(className="decoupage")

# We fill it
image = Image.open(img_file + "/" + listimg[position])
canvas = tkinter.Canvas(window, width=image.size[0], height=image.size[1])
canvas.pack()
image_tk = ImageTk.PhotoImage(image)
canvas.create_image(image.size[0] // 2 + 2, image.size[1] // 2 + 2, image=image_tk)
bob = canvas.create_rectangle(debut[0], debut[1], fin[0], fin[1], outline='orange')
sv = tkinter.StringVar()
sv.set("coords : (" + str(debut[0]) + "," + str(debut[1]) + "," + str(fin[0]) + "," + str(fin[1]) + ")")
label = tkinter.Label(window, textvariable=sv)
label.pack()
filename = tkinter.StringVar()
filename.set(listimg[position])
label = tkinter.Label(window, textvariable=filename)
label.pack()
alreadydone = tkinter.StringVar()
nb_xml = len(os.listdir(xml_file))
alreadydone.set("nombre d'images traitées :" + str(nb_xml)+"/"+str(total_img))
label = tkinter.Label(window, textvariable=alreadydone)
label.pack()
label = tkinter.Label(window, text="Left clic : hand",fg="green")
label.pack(side=tkinter.LEFT,expand=True)
label = tkinter.Label(window, text="Center clic : fist",fg="red")
label.pack(side=tkinter.LEFT,expand=True)
label = tkinter.Label(window, text="Right clic : spine",fg="blue")
label.pack(side=tkinter.LEFT,expand=True)

# This function is called when we move our mouse inside the window
def deplacementcadre(event):
    global debut, fin
    largeur = fin[0] - debut[0]
    hauteur = fin[1] - debut[1]
    debut[0] = event.x - largeur / 2
    debut[1] = event.y - hauteur / 2
    fin[0] = event.x + largeur / 2
    fin[1] = event.y + hauteur / 2
    canvas.coords(bob, debut[0], debut[1], fin[0], fin[1])
    sv.set("coords : (" + str(debut[0]) + "," + str(debut[1]) + "," + str(fin[0]) + "," + str(fin[1]) + ")")


# This function reduce or increase the size of our square
def echelonnage(event):
    global debut, fin, image
    if event.delta > 0:
        if fin[1] - debut[1] < image.size[1] and fin[0] - debut[0] < image.size[0]:
            debut[0] -= 1
            debut[1] -= 1
            fin[0] += 1
            fin[1] += 1
    else:
        if debut[0] < fin[0]:
            debut[0] += 1
            debut[1] += 1
            fin[0] -= 1
            fin[1] -= 1
    canvas.coords(bob, debut[0], debut[1], fin[0], fin[1])
    sv.set("coords : (" + str(debut[0]) + "," + str(debut[1]) + "," + str(fin[0]) + "," + str(fin[1]) + ")")


# the function witch store all our clics
def enregistrer(event):
    global mains, listimg, position, debut, fin, image, canvas, img_file
    debutmin = list(debut)
    finmin = list(fin)
    imgMatrix = cv2.imread(img_file + "/" + listimg[position], 0)
    if debutmin[0] < 0:
        debutmin[0] = 0
    if debutmin[1] < 0:
        debutmin[1] = 0
    if finmin[0] > image.size[0] - 1:
        finmin[0] = image.size[0] - 1
    if finmin[1] > image.size[1] - 1:
        finmin[1] = image.size[1] - 1
    while np.mean(imgMatrix[int(debutmin[1]):int(finmin[1]), int(debutmin[0])]) == 255:
        debutmin[0] += 1
        if finmin[0] - debutmin[0] == 0:
            return
    while np.mean(imgMatrix[int(debutmin[1]):int(finmin[1]), int(finmin[0])]) == 255:
        finmin[0] -= 1
    while np.mean(imgMatrix[int(debutmin[1]), int(debutmin[0]):int(finmin[0])]) == 255:
        debutmin[1] += 1
    while np.mean(imgMatrix[int(finmin[1]), int(debutmin[0]):int(finmin[0])]) == 255:
        finmin[1] -= 1
    
    if event.num==1:
        canvas.create_rectangle(debutmin[0], debutmin[1], finmin[0], finmin[1], outline="green")
        mains.append("hand")
    elif event.num==2:
        canvas.create_rectangle(debutmin[0], debutmin[1], finmin[0], finmin[1], outline="red")
        mains.append("fist")
    else:
        canvas.create_rectangle(debutmin[0], debutmin[1], finmin[0], finmin[1], outline="blue")
        mains.append("spine")

    mains = mains + debutmin + finmin


# function to take the next picture and create a xml and a line in csv for the old one.
def onReturnKey(event):
    global position, image, image_tk, canvas, bob, img_file, mains, xml_file, nb_xml,total_img,fichiercoord,label
    position += 1
    if position > len(listimg) - 1:
        tkinter.Label(window, text="no more pictures availables.").pack()
        return
    image = Image.open(img_file + "/" + listimg[position])
    image_tk = ImageTk.PhotoImage(image)
    canvas.create_image(image.size[0] // 2 + 2, image.size[1] // 2 + 2, image=image_tk)
    bob = canvas.create_rectangle(debut[0], debut[1], fin[0], fin[1], outline='orange')

    path = os.path.abspath(img_file + "/" + listimg[position - 1])
    xml = writexml.writeXML(img_file, listimg[position - 1], path, 512, 424, 3, mains)
    with open(xml_file + "/" + os.path.splitext(listimg[position - 1])[0] + ".xml", "w") as file:
        file.write(xml)
    for i in range(len(mains) // 5):
        fichiercoord.write(
            listimg[position - 1] + "," + str(int(mains[i * 5 + 1])) + "," + str(int(mains[i * 5 + 2])) + "," +
            str(int(mains[i * 5 + 3])) + "," + str(int(mains[i * 5 + 4])) + "," + mains[i * 5] + "\n")
    mains = []
    filename.set(listimg[position])
    nb_xml += 1
    alreadydone.set("nombre d'images traitées :" + str(nb_xml)+"/"+str(total_img))


#If we do a mistake, we can remove the last object with this function
def clear(event):
    global position, image, image_tk, canvas, bob, img_file, mains, xml_file, nb_xml,total_img
    mains=mains[0:-5]
    image = Image.open(img_file + "/" + listimg[position])
    image_tk = ImageTk.PhotoImage(image)
    canvas.create_image(image.size[0] // 2 + 2, image.size[1] // 2 + 2, image=image_tk)
    bob = canvas.create_rectangle(debut[0], debut[1], fin[0], fin[1], outline='orange')
    for i in range(len(mains)//5):
        if mains[i*5] == 'hand':
            canvas.create_rectangle(mains[i*5+1], mains[i*5+2], mains[i*5+3], mains[i*5+4], outline='green')
        elif mains[i * 5] == 'fist':
            canvas.create_rectangle(mains[i*5+1], mains[i*5+2], mains[i*5+3], mains[i*5+4], outline='red')
        else:
            canvas.create_rectangle(mains[i*5+1], mains[i*5+2], mains[i*5+3], mains[i*5+4], outline='blue')

#function to counter an issue linked to the focus on our canvas
def removeFocus(event):
    global label
    label.focus_set()

# We create our events
window.bind('<Return>', onReturnKey)
canvas.bind("<Motion>", deplacementcadre)
canvas.bind("<MouseWheel>", echelonnage)
canvas.bind("<Button-1>", enregistrer)
canvas.bind("<Button-2>", enregistrer)
canvas.bind("<Button-3>", enregistrer)
canvas.bind('<Return>', onReturnKey)
window.bind('<BackSpace>', clear)
canvas.bind('<FocusIn>',removeFocus)
tkinter.mainloop()
