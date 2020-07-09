import tkinter as Tk
from tkinter.filedialog import askopenfilename
import numpy as np
from stl import mesh

root= Tk.Tk()




canvas1 = Tk.Canvas(root, width = 300, height = 300)
canvas1.pack()

def choosefile ():  
    
    filename = askopenfilename()
    print(filename)
    readfile(filename)


def readfile (filename):
    your_mesh = mesh.Mesh.from_file(filename)
    volume, cog, inertia = your_mesh.get_mass_properties()
    print("Volume  = {0}".format(volume))
    print("Position of the center of gravity (COG) = {0}".format(cog))
    print("Inertia matrix at expressed at the COG  = {0}".format(inertia[0,:]))
    print("                                          {0}".format(inertia[1,:]))
    print("                                          {0}".format(inertia[2,:]))
    
button1 = Tk.Button(text='Upload File',command=choosefile, bg='brown',fg='white')
canvas1.create_window(150, 150, window=button1)

root.mainloop()
