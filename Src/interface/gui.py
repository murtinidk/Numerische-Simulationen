from tkinter import *
import numpy as np
from enum import Enum

class debugOptions(Enum):
    drawID = 1
    drawEQ = 2
    drawEN = 3
    drawLines = 4
    drawNodes = 5

debugSettings = {
    debugOptions.drawID : False,
    debugOptions.drawEQ : False,
    debugOptions.drawEN : False,
    debugOptions.drawLines : True,
    debugOptions.drawNodes : False
}

width = None
height = None
boundary_conditions_str = None
meshWidth = meshHeight = 1000


def get_width():
    try:
        return int(width.get())
    except ValueError:
        #return default if invalid
        return 10

def get_height():
    try:
        return int(height.get())
    except ValueError:
        #return default if invalid
        return 10
        
def get_boundary_condition():
    return boundary_conditions_str.get()

def get_xResolution():
    assert(int(xResolution.get()) > 0)
    try:
        return int(xResolution.get()) + 1
    except ValueError:
        #return default if invalid
        return 10

def get_yResolution():
    assert(int(yResolution.get()) > 0)
    try:
        return int(yResolution.get()) + 1
    except ValueError:
        #return default if invalid
        return 10




def create():
    global width, height, boundary_conditions_str, xResolution, yResolution, meshHeight, meshWidth, meshCanvas, drawMesh
    
    #main window
    root = Tk()
    root.title("Numerische Simulationen: FEM Simulation")
    root.geometry("1500x1200")

    #create input for mesh width and height
    Label(root, text="Width:").grid(row=0, column=0)
    width = Entry(root)
    width.insert(0, "10")
    width.grid(row=0, column=1)

    Label(root, text="Height:").grid(row=1, column=0)
    height = Entry(root)
    height.insert(0, "10")
    height.grid(row=1, column=1)

    Label(root, text="Width Resolution:").grid(row=0, column=2)
    xResolution = Entry(root)
    xResolution.insert(0, "10")
    xResolution.grid(row=0, column=3)
    

    Label(root, text="Height Resolution:").grid(row=1, column=2)
    yResolution = Entry(root)
    yResolution.insert(0, "10")
    yResolution.grid(row=1, column=3)

    Label(root, text="Boundary Conditions:").grid(row=6, column=0)
    boundary_conditions_str = StringVar(root)
    boundary_conditions_str.set("dirichlet")
    boundary_conditions_dropdown = OptionMenu(root, boundary_conditions_str, "dirichlet", "neumann")
    boundary_conditions_dropdown.grid(row=6, column=1)

    
    drawMesh = IntVar()
    Label(root, text="draw Mesh:").grid(row=2, column=2)
    drawMeshButton = Checkbutton(root, variable=drawMesh)
    drawMeshButton.select()
    drawMeshButton.grid(row=2, column=3)

    #start button
    #from main import main_simulation 
    #start_button = Button(root, text="Start", command=main_simulation)
    start_button = Button(root, text="Start", command=lambda: __import__('main').main_simulation())
    start_button.grid(row=16, column=0, columnspan=2)
    
    
    meshCanvas = Canvas(root, width=meshWidth, height=meshHeight, bg="lightgrey")
    meshCanvas.grid(row=30, column=1, columnspan=2)

    #tkinter loop
    root.mainloop()
    #todo: add quit function, maybe in main.py?
    #for freeing resources, maybe add a quit button to the gui
    
def updateGui():
    from main import Data
    global width, height, boundary_conditions_str, meshCanvas
    if Data.hasMesh:
        #update the mesh in the gui
        meshCanvas.delete("all")
        if(drawMesh.get()):
            mesh = Data.getMesh()
            
            if((debugSettings[debugOptions.drawNodes]) or (not debugSettings[debugOptions.drawID]) or (debugSettings[debugOptions.drawEQ])):
                for node in mesh:
                    drawNode(node)
                
            if(debugSettings[debugOptions.drawLines]):
                for elementId in range((Data.getXResolution()-1) * (Data.getYResolution()-1)):
                    drawElement(elementId)
        
def drawElement(elementId):
    from main import Data
    global meshCanvas, meshWidth, meshHeight
    
    if(not Data.hasIEN):
        return
    #draw a element in the mesh
    margin = 80
    lineThickness = 1
    
    largestSize = max(Data.getWidth(), Data.getHeight())
    scale = (meshWidth - 2 * margin) / largestSize
    
    coordsTL = coordsBL = coordsTR = coordsBR = None
    #get the nodes of the element
    ienKeys = Data.getIEN().keys()
    if((0, elementId) in ienKeys):
        coordsTL = Data.mesh[Data.getIENof(0, elementId)].GetCoordinates()
        coordsTL = tuple([coordsTL[0]*scale + margin, coordsTL[1]*scale + margin])
    if((1, elementId) in ienKeys):
        coordsTR = Data.mesh[Data.getIENof(1, elementId)].GetCoordinates()
        coordsTR = tuple([coordsTR[0]*scale + margin, coordsTR[1]*scale + margin])
    if((2, elementId) in ienKeys):
        coordsBL = Data.mesh[Data.getIENof(2, elementId)].GetCoordinates()
        coordsBL = tuple([coordsBL[0]*scale + margin, coordsBL[1]*scale + margin])
    if((3, elementId) in ienKeys):
        coordsBR = Data.mesh[Data.getIENof(3, elementId)].GetCoordinates()
        coordsBR = tuple([coordsBR[0]*scale + margin, coordsBR[1]*scale + margin])
    
    if((not coordsTL is None) and (not coordsBL is None)):
        meshCanvas.create_line(coordsTL, coordsBL, width=lineThickness)
    if((not coordsTL is None) and (not coordsTR is None)):
        meshCanvas.create_line(coordsTL, coordsTR, width=lineThickness)
    if((not coordsTR is None) and (not coordsBR is None)):
        meshCanvas.create_line(coordsTR, coordsBR, width=lineThickness)
    if((not coordsBL is None) and (not coordsBR is None)):
        meshCanvas.create_line(coordsBL, coordsBR, width=lineThickness)

        
def drawNode(node):
    from main import Data
    global meshCanvas, meshWidth, meshHeight
    #draw a node in the mesh
    margin = 80
    nodeRadius = 3

    x, y = node.GetCoordinates()
    largestSize = max(Data.getWidth(), Data.getHeight())
    x += (largestSize - Data.getWidth()) / 2
    y += (largestSize - Data.getHeight()) / 2
    x = int(x / (largestSize) * (meshWidth - 2 * margin) + margin)
    y = int(y / (largestSize) * (meshWidth - 2 * margin) + margin)

    
    if(debugSettings[debugOptions.drawNodes]):
        meshCanvas.create_oval(x-nodeRadius, y-nodeRadius, x+nodeRadius, y+nodeRadius, fill="black")

    if(debugSettings[debugOptions.drawID]):
        meshCanvas.create_text(x + nodeRadius, y - nodeRadius, text= "id:" + str(node.GetIndex()), fill="black", font="Arial 8", anchor=SW)

    
    if(debugSettings[debugOptions.drawEQ]):
        EQid = None
        try:
            EQid = "EQid:" + str(Data.getNEof( node.GetIndex()))
        except Exception as error:
            EQid = error.__str__()
        finally:
            meshCanvas.create_text(x + nodeRadius, y + nodeRadius, text= EQid, fill="black", font="Arial 8", anchor=NW, width=70)
    
    if(debugSettings[debugOptions.drawEN]):
        EN = None
        try:
            #Get dict entries where this node is the result
            EN = {k: v for k, v in Data.getIEN().items() if v == node.GetIndex()}
            #convert to nice text
            EN = "EN:\n" + str("\n".join("({},{})=>{}".format(a, c, v) for (a, c), v in EN.items()))
        except Exception as error:
            EN = error.__str__()
        finally:
            meshCanvas.create_text(x - nodeRadius, y - nodeRadius, text= EN, fill="black", font="Arial 8", anchor=SE, width=90)
