from tkinter import *

width = None
height = None
boundary_conditions_str = None
meshHeight = 1000
meshWidth = 1000


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

def get_resolution():
    try:
        return int(resolution.get())
    except ValueError:
        #return default if invalid
        return 10




def create():
    global width, height, boundary_conditions_str, resolution, meshHeight, meshWidth, meshCanvas
    
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

    Label(root, text="Resolution:").grid(row=2, column=0)
    resolution = Entry(root)
    resolution.insert(0, "10")
    resolution.grid(row=2, column=1)

    Label(root, text="Boundary Conditions:").grid(row=6, column=0)
    boundary_conditions_str = StringVar(root)
    boundary_conditions_str.set("dirichlet")
    boundary_conditions_dropdown = OptionMenu(root, boundary_conditions_str, "dirichlet", "neumann")
    boundary_conditions_dropdown.grid(row=6, column=1)

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
        mesh = Data.getMesh()
        meshCanvas.delete("all")
        for node in mesh:
            drawNode(node)
        
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
    x = int(x / largestSize * (meshWidth - 2 * margin) + margin)
    y = int(y / largestSize * (meshWidth - 2 * margin) + margin)
    meshCanvas.create_oval(x-nodeRadius, y-nodeRadius, x+nodeRadius, y+nodeRadius, fill="black")

    meshCanvas.create_text(x + nodeRadius, y - nodeRadius, text= "id:" + str(node.GetIndex()), fill="black", font="Arial 8", anchor=SW)

    EQid = None
    try:
        EQid = "EQid:" + str(Data.getNEof( node.GetIndex()))
    except Exception as error:
        EQid = error.__str__()
    finally:
        meshCanvas.create_text(x + nodeRadius, y + nodeRadius, text= EQid, fill="black", font="Arial 8", anchor=NW, width=70)
