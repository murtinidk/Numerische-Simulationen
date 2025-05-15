from tkinter import *
from interface.CustomCanvas import PanableCanvas
import numpy as np
from enum import Enum
#config loading and file stuff
from tkinter import messagebox, filedialog
import configparser #config file loading
import os #file loading

###default values
#default config path
config_path = "settings.conf"

#default settings
DEFAULTS = {
    'width': '10',
    'height': '10',
    'xResolution': '10',
    'yResolution': '10',
    'boundary': 'dirichlet',
    'drawMesh': '1'
}


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

#load settings from file
def load_settings(path=None):
    cfg = configparser.ConfigParser()
    #get default values
    vals = DEFAULTS.copy()
    file_to_load = path or config_path
    if os.path.exists(file_to_load):
        try:
            cfg.read(file_to_load)
            #overwrite default values with loaded values
            for key in DEFAULTS:
                vals[key] = cfg.get('Mesh', key, fallback=DEFAULTS[key])
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load settings:\n{e}")
    else:
        messagebox.showinfo("Load Settings", f"No config found at {file_to_load}, using defaults.")
    return vals



def save_settings(vals, path=None):
    #save settings to default or specified path
    cfg = configparser.ConfigParser()
    cfg['Mesh'] = vals
    file_to_save = path or config_path
    try:
        with open(file_to_save, 'w') as f:
            cfg.write(f)
        messagebox.showinfo("Save Settings", f"Settings saved to {file_to_save}")
    except Exception as e:
        messagebox.showerror("Save Error", f"Failed to save settings:\n{e}")


def get_width():
    try:
        return int(width.get())
    except ValueError:
        #return default if invalid
        print("not a valid width input, reverting to default value 10")
        return 10

def get_height():
    try:
        return int(height.get())
    except ValueError:
        #return default if invalid
        print("not a valid height input, reverting to default value 10")
        return 10
        
def get_boundary_condition():
    return boundary_conditions_str.get()

def get_xResolution():
    assert(int(xResolution.get()) > 1)
    try:
        return int(xResolution.get())
    except ValueError:
        #return default if invalid
        return 10

def get_yResolution():
    assert(int(yResolution.get()) > 1)
    try:
        return int(yResolution.get())
    except ValueError:
        #return default if invalid
        return 10




def create():
    global width, height, boundary_conditions_str, xResolution, yResolution, meshHeight, meshWidth, meshCanvas, drawMesh , config_path
    #try load settings from file
    #if not found, use default values
    settings = load_settings()


    #main window
    root = Tk()
    img = PhotoImage(file='./resources/logo.png')
    root.iconphoto(False, img)
    root.title("Numerische Simulationen: FEM Simulation")
    root.geometry("1500x1200")
    root.tk_setPalette( "#FFFFFF" ) #fix linux color issues

    
    #CONFIG FILE PICKER 
    Label(root, text="Config File:").grid(row=6, column=2, sticky=E)
    config_label = Label(root, text=config_path, anchor=W)
    config_label.grid(row=6, column=3, columnspan=3, sticky=W+E)
    def choose_file():
        nonlocal config_label
        file = filedialog.askopenfilename(
            title="Select config file",
            filetypes=[("INI files", "*.conf *.ini"), ("All files", "*")]
        )
        if file:
            config_path = file
            config_label.config(text=config_path)
            # reload with new file
            vals = load_settings(config_path)
            # update entries
            width.delete(0, END); width.insert(0, vals['width'])
            height.delete(0, END); height.insert(0, vals['height'])
            xResolution.delete(0, END); xResolution.insert(0, vals['xResolution'])
            yResolution.delete(0, END); yResolution.insert(0, vals['yResolution'])
            boundary_conditions_str.set(vals['boundary'])
            drawMesh.set(int(vals['drawMesh']))

    Button(root, text="Choose Config File", command=choose_file).grid(row=6, column=2)




    #create input for mesh width and height
    Label(root, text="Width:").grid(row=0, column=0)
    width = Entry(root)
    width.insert(0, settings['width'])
    width.grid(row=0, column=1)

    Label(root, text="Height:").grid(row=1, column=0)
    height = Entry(root)
    height.insert(0, settings['height'])
    height.grid(row=1, column=1)

    Label(root, text="Width Node Resolution:").grid(row=0, column=2)
    xResolution = Entry(root)
    xResolution.insert(0, settings['xResolution'])
    xResolution.grid(row=0, column=3)
    

    Label(root, text="Height Node Resolution:").grid(row=1, column=2)
    yResolution = Entry(root)
    yResolution.insert(0, settings['yResolution'])
    yResolution.grid(row=1, column=3)

    Label(root, text="Boundary Conditions:").grid(row=6, column=0)
    boundary_conditions_str = StringVar(root)
    boundary_conditions_str.set(settings['boundary'])
    boundary_conditions_dropdown = OptionMenu(root, boundary_conditions_str, "dirichlet", "neumann")
    boundary_conditions_dropdown.grid(row=6, column=1)

    
    drawMesh = IntVar(value=int(settings['drawMesh']))
    Label(root, text="draw Mesh:").grid(row=2, column=2)
    drawMeshButton = Checkbutton(root, variable=drawMesh)
    drawMeshButton.select()
    drawMeshButton.grid(row=2, column=3)

    #start button
    #from main import main_simulation 
    #start_button = Button(root, text="Start", command=main_simulation)
    start_button = Button(root, text="Start", command=lambda: __import__('main').main_simulation())
    start_button.grid(row=16, column=0, columnspan=2)
    
    #load settings button
    def on_load():
        vals = load_settings(config_path)
        width.delete(0, END); width.insert(0, vals['width'])
        height.delete(0, END); height.insert(0, vals['height'])
        xResolution.delete(0, END); xResolution.insert(0, vals['xResolution'])
        yResolution.delete(0, END); yResolution.insert(0, vals['yResolution'])
        boundary_conditions_str.set(vals['boundary'])
        drawMesh.set(int(vals['drawMesh']))

    #save settings button
    def on_save_click():
        vals = {
            'width': width.get(),
            'height': height.get(),
            'xResolution': xResolution.get(),
            'yResolution': yResolution.get(),
            'boundary': boundary_conditions_str.get(),
            'drawMesh': str(drawMesh.get())
        }
        save_settings(vals, config_path)

    Button(root, text="Load Settings", command=on_load).grid(row=7, column=2)
    Button(root, text="Save Settings", command=on_save_click).grid(row=8, column=2)




    #canvas pannable / zoomable
    meshCanvas = PanableCanvas(root, width=meshWidth, height=meshHeight, bg="lightgrey")
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
            drawArrow()
            
            if((debugSettings[debugOptions.drawNodes]) or (not debugSettings[debugOptions.drawID]) or (debugSettings[debugOptions.drawEQ])):
                for node in mesh:
                    drawNode(node)
                
            if(debugSettings[debugOptions.drawLines]):
                for elementId in range((Data.getXResolution()-1) * (Data.getYResolution()-1)):
                    drawElement(elementId)

def drawArrow():
    from main import Data
    global meshCanvas, meshWidth, meshHeight
    #draw the arrow in the mesh
    margin = 80
    largestSize = max(Data.getWidth(), Data.getHeight())
    scale = (meshWidth - 2 * margin) / largestSize
    xOffset = (largestSize - Data.getWidth()) / 2
    yOffset = (largestSize - Data.getHeight()) / 2

    xArrowCoordsBegining = tuple([(0 + xOffset)*scale + margin, margin/3])
    xArrowCoordsEnd =      tuple([(Data.getWidth() +xOffset)*scale + margin, margin/3])
    yArrowCoordsBegining = tuple([margin/3, (0 + yOffset)*scale + margin])
    yArrowCoordsEnd =      tuple([margin/3, (Data.getHeight() + yOffset)*scale + margin])

    
    meshCanvas.create_text(xArrowCoordsEnd, text= "X", fill="black", font="Arial 10", anchor=W)
    meshCanvas.create_line(xArrowCoordsBegining, xArrowCoordsEnd, arrow=LAST, width=3)
    meshCanvas.create_text(yArrowCoordsEnd, text= "Y", fill="black", font="Arial 10", anchor=N)
    meshCanvas.create_line(yArrowCoordsBegining, yArrowCoordsEnd, arrow=LAST, width=3)

        
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
    xOffset = (largestSize - Data.getWidth()) / 2
    yOffset = (largestSize - Data.getHeight()) / 2
    
    coordsTL = coordsBL = coordsTR = coordsBR = None
    #get the nodes of the element
    ienKeys = Data.getIEN().keys()
    if((0, elementId) in ienKeys):
        coordsTL = Data.mesh[Data.getIENof(0, elementId)].GetCoordinates()
        coordsTL = tuple([(coordsTL[0] + xOffset)*scale + margin, (coordsTL[1] + yOffset)*scale + margin])
    if((1, elementId) in ienKeys):
        coordsTR = Data.mesh[Data.getIENof(1, elementId)].GetCoordinates()
        coordsTR = tuple([(coordsTR[0] + xOffset)*scale + margin, (coordsTR[1] + yOffset)*scale + margin])
    if((2, elementId) in ienKeys):
        coordsBL = Data.mesh[Data.getIENof(2, elementId)].GetCoordinates()
        coordsBL = tuple([(coordsBL[0] + xOffset)*scale + margin, (coordsBL[1] + yOffset)*scale + margin])
    if((3, elementId) in ienKeys):
        coordsBR = Data.mesh[Data.getIENof(3, elementId)].GetCoordinates()
        coordsBR = tuple([(coordsBR[0] + xOffset)*scale + margin, (coordsBR[1] + yOffset)*scale + margin])
    
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
