from tkinter import *
from interface.CustomCanvas import PanableCanvas
import numpy as np
from enum import Enum
import calculation.element as element
#config loading and file stuff
from tkinter import messagebox, filedialog
import configparser #config file loading
import os #file loading
import pickle #for saving/loading data
###default values

ColorResolution = 64
Margin = 80

#default settings
DEFAULTS = {
    'width': '10',
    'height': '10',
    'xResolution': '10',
    'yResolution': '10',
    # 'boundary': 'dirichlet',
    'topBoundaryType': 'neumann',
    'rightBoundaryType': 'dirichlet',
    'bottomBoundaryType': 'dirichlet',
    'leftBoundaryType': 'dirichlet',
    'line_type': 'dirichlet',
    #values
    'topBoundaryValue': '0',
    'rightBoundaryValue': '0',
    'bottomBoundaryValue': '0',
    'leftBoundaryValue': '0',
    
    #debug options
    'options_renderAnything': '1',
    'options_drawID': '0',
    'options_drawEQ': '0',
    'options_drawEN': '0',
    'options_drawLines': '0',
    'options_drawNodes': '0',
    'options_drawValues': '1',
    'options_writeValues': '0',
    'options_drawOnFinish': '0'
}

BOUNDARY_TYPE_OPTIONS = ["dirichlet", "neumann", "none"]


class debugOptions(Enum):
    renderAnything = 0
    drawID = 1
    drawEQ = 2
    drawEN = 3
    drawLines = 4
    drawNodes = 5
    drawValues = 6
    writeValues = 7
    drawOnFinish = 8

debugSettings = {
    debugOptions.renderAnything : 1,
    debugOptions.drawID : 1,
    debugOptions.drawEQ : 1,
    debugOptions.drawEN : 1,
    debugOptions.drawLines : 1,
    debugOptions.drawNodes : 1,
    debugOptions.drawValues : 1,
    debugOptions.writeValues : 1,
    debugOptions.drawOnFinish : 1
}

width = None
height = None
# boundary_conditions_str = None
meshWidth = meshHeight = 1000

class simStep(Enum):
    none = 0
    started = 1
    meshGen = 2
    boundaryConditions = 3
    meshTables = 4
    systemMatrix = 5
    solveSystem = 6
    drawingColors = 7
    finished = 8
    simStepNum = 9

SimSteps = {
    simStep.none: "None",
    simStep.started: "Started",
    simStep.meshGen: "Mesh Generation",
    simStep.boundaryConditions: "Boundary Conditions",
    simStep.meshTables: "Mesh Tables",
    simStep.systemMatrix: "System Matrix",
    simStep.solveSystem: "Solve System",
    simStep.drawingColors: "Drawing Colors",
    simStep.finished: "Finished"
}

#load settings from file
def load_settings(path=None):
    cfg = configparser.ConfigParser()
    #get default values
    vals = DEFAULTS.copy()
    file_to_load = config_path
    if os.path.exists(file_to_load):
        try:
            cfg.read(file_to_load)
            #overwrite default values with loaded values
            for key in DEFAULTS:
                vals[key] = cfg.get('FEM Sim Config', key, fallback=DEFAULTS[key])
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load settings:\n{e}")
    else:
        messagebox.showinfo("Load Settings", f"No config found at {file_to_load}, using defaults.")
    return vals



def save_settings(vals, path=None):
    #save settings to default or specified path
    cfg = configparser.ConfigParser()
    cfg['FEM Sim Config'] = vals
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
        raise Exception("Width input not valid")

def get_height():
    try:
        return int(height.get())
    except ValueError:
        raise Exception("Height input not valid")
        
def get_boundary_condition():
    return boundary_conditions_str.get()

def get_xResolution():
    assert(int(xResolution.get()) > 1)
    try:
        return int(xResolution.get())
    except ValueError:
        raise Exception("Width Resolution input not valid")

def get_yResolution():
    assert(int(yResolution.get()) > 1)
    try:
        return int(yResolution.get())
    except ValueError:
        raise Exception("Height Resolution input not valid")
    
def getLeftBoundaryType():
    try:
        return left_boundary.get()
    except ValueError:
        raise Exception("LeftboundaryType not a valid boundary input")

def getLeftBoundaryValue():
    try:
        return float(left_value.get())
    except ValueError:
        raise Exception("Leftboundary not a valid boundary value input")

def getRightBoundaryType():
    try:
        return right_boundary.get()
    except ValueError:
        raise Exception("RightboundaryType not a valid boundary input")

def getRightBoundaryValue():
    try:
        return float(right_value.get())
    except ValueError:
        raise Exception("Rightboundary not a valid boundary value input")

def getTopBoundaryType():
    try:
        return top_boundary.get()
    except ValueError:
        raise Exception("TopboundaryType not a valid boundary input")

def getTopBoundaryValue():
    try:
        return float(top_value.get())
    except ValueError:
        raise Exception("Topboundary not a valid boundary value input")

def getBottomBoundaryType():
    try:
        return bottom_boundary.get()
    except ValueError:
        raise Exception("BottomboundaryType not a valid boundary input")

def getBottomBoundaryValue():
    try:
        return float(bottom_value.get())
    except ValueError:
        raise Exception("Bottomboundary not a valid boundary value input")


def get_line():
    x = int(width.get())
    y = int(height.get())
    try:
        x1 = float(X1.get())
        y1 = float(Y1.get())
        x2 = float(X2.get())
        y2 = float(Y2.get())
        value = float(line_value.get())
    except ValueError:
        return None
    if x1 <= 0 or x2 <= 0 or y1 <= 0 or y2 <= 0 or x1 >= x or x2 >= x or y1 >= y or y2 >= y:
        raise ValueError
    return np.array([x1,y1,x2,y2, value])
    
def create():
    global width, height, boundary_conditions_str, xResolution, yResolution, meshHeight, meshWidth, meshCanvas , config_path, step_text, root
    global X1, Y1, X2, Y2, line_frame, line_value, line_type
    global top_value, top_boundary, right_value, right_boundary, bottom_boundary, bottom_value, left_boundary, left_value
    #default config path
    global config_path
    config_path = "settings.conf"
    line_type = ''

    #try load settings from file
    #if not found, use default values
    settings = load_settings()
    #transfer debugoptions from settings to debugSettings
    for key in debugSettings.keys():
        debugSettings[key] = int(settings[f'options_{key.name}'])

    #main window
    root = Tk()
    img = PhotoImage(file='./resources/logo.png')
    root.iconphoto(False, img)
    root.title("Numerische Simulationen: FEM Simulation")
    root.geometry("1500x1200")
    root.tk_setPalette( "#FFFFFF" ) #fix linux color issues

    #CONFIG FILE PICKER 
    #Label(root, text="Config File:").grid(row=6, column=2, sticky=E)
    config_label = Label(root, text=config_path, anchor=W)
    config_label.grid(row=5, column=3, columnspan=3, sticky=W+E)
    
    def choose_setting_file():
        global config_path
        
        file = filedialog.askopenfilename(
            title="Select config file",
            filetypes=[("INI files", "*.conf *.ini"), ("All files", "*")]
        )
        if file:
            config_path = file
            config_label.config(text=config_path)
            # reload with new file
            # vals = load_settings(config_path)
            
    #this button is only for selecting the path, loading and saving from path is per own button
    Button(root, text="Choose Config File", command=choose_setting_file).grid(row=5, column=2)

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

    #-----------------BOUNDARY INPUT-----------------
    #------------- TOP, RIGHT, BOTTOM, LEFT ---------
    Label(root, text="Boundary Conditions:").grid(row=6, column=0)
    #Subframe/grid
    boundary_frame = Frame(root)
    boundary_frame.grid(row=6, column=1, rowspan=2)
    bfieldwidth = 7
    #TOP
    Label(boundary_frame, text="Top:").grid(row=0, column=0)
    top_value = Entry(boundary_frame, width=bfieldwidth) # make value entry field smaller...
    top_value.insert(0,settings['topBoundaryValue']) #insert from loaded or default settings
    top_value.grid(row=0, column=1)
    top_boundary = StringVar(root, settings['topBoundaryType'])
    OptionMenu(boundary_frame, top_boundary, *BOUNDARY_TYPE_OPTIONS).grid(row=1, column=1)
    #Right
    Label(boundary_frame, text="Right:").grid(row=0, column=2)
    right_value = Entry(boundary_frame, width=bfieldwidth)
    right_value.insert(0, settings['rightBoundaryValue'])
    right_value.grid(row=0, column=3)
    right_boundary = StringVar(root, settings['rightBoundaryType'])
    OptionMenu(boundary_frame, right_boundary, *BOUNDARY_TYPE_OPTIONS).grid(row=1, column=3)
    
    #bottom
    Label(boundary_frame, text="Bottom:").grid(row=0, column=4)
    bottom_value = Entry(boundary_frame, width=bfieldwidth)
    bottom_value.insert(0, settings['bottomBoundaryValue'])
    bottom_value.grid(row=0, column=5)
    bottom_boundary = StringVar(root, settings['bottomBoundaryType'])
    OptionMenu(boundary_frame, bottom_boundary, *BOUNDARY_TYPE_OPTIONS).grid(row=1, column=5)
    
    #left
    Label(boundary_frame, text="Left:").grid(row=0, column=6)
    left_value = Entry(boundary_frame, width=bfieldwidth)
    left_value.insert(0, settings['leftBoundaryValue'])
    left_value.grid(row=0, column=7)
    left_boundary = StringVar(root, settings['leftBoundaryType'])
    OptionMenu(boundary_frame, left_boundary, *BOUNDARY_TYPE_OPTIONS).grid(row=1, column=7)
    
    # boundary_conditions_str = StringVar(root)
    # boundary_conditions_str.set(settings['boundary'])
    # boundary_conditions_dropdown = OptionMenu(root, boundary_conditions_str, "dirichlet", "neumann")
    # boundary_conditions_dropdown.grid(row=8, column=1)

    Label(root, text="Line Input:").grid(row=4, column=0)

    line_frame = Frame(root)
    line_frame.grid(row=4, column=1, rowspan=1, columnspan=1)
    lfieldwidth = 7

    Label(line_frame, text="X1:").grid(row=0, column=0)
    X1 = Entry(line_frame, width=lfieldwidth)
    X1.grid(row=0, column=1)
    Label(line_frame, text="Y1:").grid(row=0, column=2)
    Y1 = Entry(line_frame, width=lfieldwidth)
    Y1.grid(row=0, column=3)
    Label(line_frame, text="X2:").grid(row=0, column=4)
    X2 = Entry(line_frame, width=lfieldwidth)
    X2.grid(row=0, column=5)
    Label(line_frame, text="Y2:").grid(row=0, column=6)
    Y2 = Entry(line_frame, width=lfieldwidth)
    Y2.grid(row=0, column=7)
    Label(line_frame, text="Line Value:").grid(row=0, column=8)
    line_value = Entry(line_frame, width=lfieldwidth)
    line_value.grid(row=0, column=9)
    line_type = StringVar(root, settings['line_type'])
    OptionMenu(line_frame, line_type, "dirichlet", "neumann", "none").grid(row=0, column=11)
    
    
    renderingOptions_frame = Frame(root)
    renderingOptions_frame.grid(row=0, column=8, rowspan=8, columnspan=1)

    for i, option in enumerate(debugSettings.keys()):
        Label(renderingOptions_frame, text=option.name).grid(row=i, column=0)
        debugSettings[option] = IntVar(value=int(debugSettings[option]))
        debugButton = Checkbutton(renderingOptions_frame, variable=debugSettings[option], command=updateGui)
        debugButton.grid(row=i, column=1)

    #start button
    #from main import main_simulation 
    #start_button = Button(root, text="Start", command=main_simulation)
    
    start_frame = Frame(root)
    start_frame.grid(row=16, column=1, rowspan=1, columnspan=1)
    start_button = Button(start_frame, text="Start", command=lambda: __import__('main').main_simulation())
    start_button.grid(row=0, column=0, columnspan=1)
    step_text = Label(start_frame, text="Sim Step: None")
    step_text.grid(row=0, column=1, columnspan=1)
    setStep(simStep.none)
    
    #load settings button
    def load_settings_button():
        #takes path from config_path from function/button selecting the settings file 
        vals = load_settings(config_path)
        #update the gui with the loaded values
        width.delete(0, END); width.insert(0, vals['width'])
        height.delete(0, END); height.insert(0, vals['height'])
        xResolution.delete(0, END); xResolution.insert(0, vals['xResolution'])
        yResolution.delete(0, END); yResolution.insert(0, vals['yResolution'])
        top_boundary.set(vals['topBoundaryType'])
        right_boundary.set(vals['rightBoundaryType'])
        bottom_boundary.set(vals['bottomBoundaryType'])
        left_boundary.set(vals['leftBoundaryType'])
        top_value.delete(0, END); top_value.insert(0, vals['topBoundaryValue'])
        right_value.delete(0, END); right_value.insert(0, vals['rightBoundaryValue'])
        bottom_value.delete(0, END); bottom_value.insert(0, vals['bottomBoundaryValue'])
        left_value.delete(0, END); left_value.insert(0, vals['leftBoundaryValue'])
        debugSettings[debugOptions.renderAnything].set(int(vals['options_renderAnything']))
        debugSettings[debugOptions.drawID].set(int(vals['options_drawID']))
        debugSettings[debugOptions.drawEQ].set(int(vals['options_drawEQ']))
        debugSettings[debugOptions.drawEN].set(int(vals['options_drawEN']))
        debugSettings[debugOptions.drawLines].set(int(vals['options_drawLines']))
        debugSettings[debugOptions.drawNodes].set(int(vals['options_drawNodes']))
        debugSettings[debugOptions.drawValues].set(int(vals['options_drawValues']))
        debugSettings[debugOptions.writeValues].set(int(vals['options_writeValues']))
        debugSettings[debugOptions.drawOnFinish].set(int(vals['options_drawOnFinish']))
        
    #save settings button
    def save_setting_button():
        vals = {
            'width': width.get(),
            'height': height.get(),
            'xResolution': xResolution.get(),
            'yResolution': yResolution.get(),
            # 'boundary': boundary_conditions_str.get(),
            'topBoundaryType': top_boundary.get(),
            'rightBoundaryType': right_boundary.get(),
            'bottomBoundaryType': bottom_boundary.get(),
            'leftBoundaryType': left_boundary.get(),
            'topBoundaryValue': top_value.get(),
            'rightBoundaryValue': right_value.get(),
            'bottomBoundaryValue': bottom_value.get(),
            'leftBoundaryValue': left_value.get(),
            'options_renderAnything': str(debugSettings[debugOptions.renderAnything].get()),
            'options_drawID': str(debugSettings[debugOptions.drawID].get()),
            'options_drawEQ': str(debugSettings[debugOptions.drawEQ].get()),
            'options_drawEN': str(debugSettings[debugOptions.drawEN].get()),
            'options_drawLines': str(debugSettings[debugOptions.drawLines].get()),
            'options_drawNodes': str(debugSettings[debugOptions.drawNodes].get()),
            'options_drawValues': str(debugSettings[debugOptions.drawValues].get()),
            'options_writeValues': str(debugSettings[debugOptions.writeValues].get()),
            'options_drawOnFinish': str(debugSettings[debugOptions.drawOnFinish].get()),
        }
        save_settings(vals, config_path)

    Button(root, text="Load Settings", command=load_settings_button).grid(row=6, column=2)
    Button(root, text="Save Settings", command=save_setting_button).grid(row=7, column=2)

    #program data loading/saving    
    def save_data_button(file_path):
        from main import Data
        if Data.hasMesh:
            try:
                save_data(file_path)
                messagebox.showinfo("Save Data", f"Data saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save data:\n{e}")
        else:
            messagebox.showwarning("Save Warning", "No mesh data to save.")
            
    def save_data(file_path):
        with open(file_path, 'wb') as file:
            from main import Data
            pickle.dump(Data, file)

    #save data button, asks for file name with picker for pickle
    Button(root, text="Save Data", command=lambda: save_data_button(filedialog.asksaveasfilename(
        title="Save data as",
        defaultextension=".pkl",
        filetypes=[("Pickle files", "*.pkl"), ("All files", "*")]
    ))).grid(row=6, column=3)

    #load data button, asks for file name with picker for pickle
    def load_data_button(file_path):
        try:
            with open(file_path, 'rb') as file:
                from main import Data
                pickle_data = pickle.load(file)
                #check if data is right type
                if isinstance(pickle_data, type(Data)):
                    #update the Data object with the loaded data
                    Data.__dict__.update(pickle_data.__dict__)
                else:
                    raise TypeError("Loaded data is not of type Data")
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load data:\n{e}")
        #update the gui
        updateGui()
    
    Button(root, text="Load Data", command=lambda: load_data_button(filedialog.askopenfilename(
        title="Load data",
        filetypes=[("Pickle files", "*.pkl"), ("All files", "*")]
    ))).grid(row=7, column=3)
    
    #CFS export button 
    def export_cfs_button():
        from main import Data
        #check if there are results to export
        if Data.getHasResult() == False:
            messagebox.showwarning("No results", "No results to export")
            return
        #check if there is already a results.cfs
        if os.path.exists("results.cfs"):
            #ask for overwrite
            if messagebox.askyesno("Overwrite", "results.cfs already exists. Overwrite?"):
                #deete old file
                try:
                    os.remove("results.cfs")
                except Exception as e:
                    messagebox.showerror("Delete Error", f"Failed to delete old results.cfs:\n{e}")
                    return
                #write new file
                Data.exportCFS()
                messagebox.showinfo("Export CFS", "CFS file exported to results.cfs")
            else:
                return
        
    cfs_button = Button(root, text="Export CFS", command=export_cfs_button)
    cfs_button.grid(row=16, column=3)

    #canvas pannable / zoomable
    meshCanvas = PanableCanvas(root, width=meshWidth, height=meshHeight, bg="lightgrey")
    meshCanvas.grid(row=30, column=0, columnspan=21, sticky=N+S+E+W, padx=5, pady=5)
    root.grid_rowconfigure(30, weight=1)
    root.grid_columnconfigure(20, weight=1)

    #tkinter loop
    root.mainloop()
    #todo: add quit function, maybe in main.py?
    #for freeing resources, maybe add a quit button to the gui

#unused
def closeGui():
    #close the gui
    from main import Data
    if(Data.hasMesh):
        Data.mesh = None
        Data.hasMesh = False
    meshCanvas.delete("all")
    meshCanvas.destroy()
    print("GUI closed")    

def updateGui():
    from main import Data
    global width, height, boundary_conditions_str, meshCanvas, root
    if(debugSettings[debugOptions.drawOnFinish].get() and not Data.getHasResult()):
        return
    root.update()
    if Data.hasMesh:
        #update the mesh in the gui
        meshCanvas.delete("all")
        if(debugSettings[debugOptions.renderAnything].get()):
            if(debugSettings[debugOptions.drawValues].get() and Data.getHasResult()):
                drawColor()
            mesh = Data.getMesh()
            drawArrow()
            drawLine(Data.getLine())
            
            if((debugSettings[debugOptions.drawNodes].get()) or (not debugSettings[debugOptions.drawID].get()) or (debugSettings[debugOptions.drawEQ].get())):
                for node in mesh:
                    drawNode(node)
                
            if(debugSettings[debugOptions.drawLines].get()):
                for elementId in range((Data.getXResolution()-1) * (Data.getYResolution()-1)):
                    drawElement(elementId)

def drawArrow():
    from main import Data
    global meshCanvas, meshWidth, meshHeight
    #draw the arrow in the mesh
    xArrowCoordsBegining = globalToMeshCoords(0, 0)
    xArrowCoordsEnd = globalToMeshCoords(Data.getWidth(),0)
    yArrowCoordsBegining = globalToMeshCoords(0, 0)	
    yArrowCoordsEnd = globalToMeshCoords(0, Data.getHeight())
    xArrowCoordsBegining = (xArrowCoordsBegining[0], xArrowCoordsBegining[1] - 2*Margin/3)
    xArrowCoordsEnd = (xArrowCoordsEnd[0], xArrowCoordsEnd[1] - 2*Margin/3)
    yArrowCoordsBegining = (yArrowCoordsBegining[0] - 2*Margin/3, yArrowCoordsBegining[1])
    yArrowCoordsEnd = (yArrowCoordsEnd[0] - 2*Margin/3, yArrowCoordsEnd[1])

    meshCanvas.create_text(xArrowCoordsEnd, text= "X", fill="black", font="Arial 10", anchor=W)
    meshCanvas.create_line(xArrowCoordsBegining, xArrowCoordsEnd, arrow=LAST, width=3)
    meshCanvas.create_text(yArrowCoordsEnd, text= "Y", fill="black", font="Arial 10", anchor=N)
    meshCanvas.create_line(yArrowCoordsBegining, yArrowCoordsEnd, arrow=LAST, width=3)

#draw a element in the mesh
#there would be faster ways to just dra a mesh, but we want to check the correctness of the IEN dict
def drawElement(elementId):
    from main import Data
    global meshCanvas, meshWidth, meshHeight
    
    if(not Data.hasIEN):
        return
    
    lineThickness = 1
    coordsTL = coordsBL = coordsTR = coordsBR = None
    ienKeys = Data.getIEN().keys()
    if((0, elementId) in ienKeys):
        coordsTL = Data.mesh[Data.getIENof(0, elementId)].GetCoordinates()
        coordsTL = globalToMeshCoords(coordsTL[0], coordsTL[1])
    if((1, elementId) in ienKeys):
        coordsTR = Data.mesh[Data.getIENof(1, elementId)].GetCoordinates()
        coordsTR = globalToMeshCoords(coordsTR[0], coordsTR[1])
    if((2, elementId) in ienKeys):
        coordsBL = Data.mesh[Data.getIENof(2, elementId)].GetCoordinates()
        coordsBL = globalToMeshCoords(coordsBL[0], coordsBL[1])
    if((3, elementId) in ienKeys):
        coordsBR = Data.mesh[Data.getIENof(3, elementId)].GetCoordinates()
        coordsBR = globalToMeshCoords(coordsBR[0], coordsBR[1])
    
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
    x, y = globalToMeshCoords(x, y)
    
    if(debugSettings[debugOptions.drawNodes].get()):
        meshCanvas.create_oval(x-nodeRadius, y-nodeRadius, x+nodeRadius, y+nodeRadius, fill="black")

    if(debugSettings[debugOptions.drawID].get()):
        meshCanvas.create_text(x + nodeRadius, y - nodeRadius, text= "id:" + str(node.GetIndex()), fill="black", font="Arial 8", anchor=SW)

    if(debugSettings[debugOptions.drawEQ].get()):
        EQid = None
        try:
            EQid = "EQid:" + str(Data.getNEof( node.GetIndex()))
        except Exception as error:
            EQid = error.__str__()
        finally:
            meshCanvas.create_text(x - nodeRadius, y + nodeRadius, text= EQid, fill="black", font="Arial 8", anchor=NE, width=70)
    
    if(debugSettings[debugOptions.drawEN].get()):
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

    if(debugSettings[debugOptions.writeValues].get()):
        if(not node.GetResult() is None):
            text = "Result:" + f"{node.GetResult():.3f}"
        elif(not node.GetDirichletBoundary() is None):
            text = "Dirichlet:" + f"{node.GetDirichletBoundary():.3f}"
        else:
            text = "Result: None"
        meshCanvas.create_text(x + nodeRadius, y + nodeRadius, text= text, fill="black", font="Arial 8", anchor=NW, width=70)

def drawLine(line):
    from main import Data
    global meshCanvas, meshWidth, meshHeight
    if not Data.hasLine:
        return
    
    lineThickness = 2

    x1, y1, x2, y2 = line
    coords1 = globalToMeshCoords(x1, y1)
    coords2 = globalToMeshCoords(x2, y2)

    meshCanvas.create_line(coords1, coords2, width=lineThickness+0.5, fill='#AAA', smooth=True)
    meshCanvas.create_line(coords1, coords2, width=lineThickness, fill='#000', smooth=True)

def setStep(step: simStep):
    global step_text, SimSteps
    text = " Sim Step [" + str(step.value) + "/" + str(simStep.simStepNum.value - 1) + "]: " + SimSteps[step]
    step_text.config(text= text)
    print(text)
    step_text.update()

def drawColor():
    from main import Data
    global meshCanvas, meshWidth, meshHeight, ColorResolution
    colorRes = ColorResolution / max(Data.getXResolution(), Data.getYResolution())
    colorRes = max(1, int(colorRes))

    if not Data.getHasResult():
        return

    minValue = np.inf
    maxValue = -np.inf
    for node in Data.getMesh():
        if node.GetValue() is not None:
            minValue = min(minValue, node.GetValue())
            maxValue = max(maxValue, node.GetValue())
    valueRange = maxValue - minValue

    for e in range(Data.getNe()):
        element_ = element.Element(e)
        TL = element_.GetNodeTL()
        BR = element_.GetNodeBR()
        xmin, ymin = TL.GetCoordinates()
        xmax, ymax = BR.GetCoordinates()
        #the border of the individual dolour sections
        xborder = np.linspace(xmin, xmax, colorRes+1)
        yborder = np.linspace(ymin, ymax, colorRes+1)
        #the probe points in the middle of the sections
        xprobe = np.linspace(xmin, xmax, 2*colorRes+1)[::2]
        yprobe = np.linspace(ymin, ymax, 2*colorRes+1)[::2]
        for i in range(colorRes):
            for j in range(colorRes):
                x1, y1 = globalToMeshCoords(xborder[i], yborder[j])
                x2, y2 = globalToMeshCoords(xborder[i+1], yborder[j+1])
                value = valueInElement(xprobe[i], yprobe[j], e)
                #make sure not every value is the same, which would draw random grainy colors
                if valueRange == 0:
                    valueRange = 1
                #also check for small rounding errors
                if valueRange < maxValue / 100000:
                    valueRange = maxValue / 100000
                hottness = (value - minValue) / valueRange #should be from 0 to 1
                # sometimes it is not. clamp it
                #hottness = max(0, min(1, hottness))
                r = int(hottness * 192) + 63
                g = 63
                b = int((1 - hottness) * 192) + 63
                color = "#%02x%02x%02x" % (r, g, b)
                meshCanvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

def valueInElement(x, y, elementId):
    from main import Data

    element_ = element.Element(elementId)
    #get the nodes of the elemen
    TL = element_.GetNodeTL()
    BL = element_.GetNodeBL()
    TR = element_.GetNodeTR()
    BR = element_.GetNodeBR()

    xmin, ymin = TL.GetCoordinates()
    xmax, ymax = BR.GetCoordinates()
    assert x >= xmin and x <= xmax, "x not in range of element"
    assert y >= ymin and y <= ymax, "y not in range of element"

    factorXmax = (x - xmin) / (xmax - xmin)
    factorXmin = (xmax - x) / (xmax - xmin)
    factorYmax = (y - ymin) / (ymax - ymin)
    factorYmin = (ymax - y) / (ymax - ymin)

    #calculate the contribution of each node to the point
    TLcontribution = factorXmin * factorYmin
    BLcontribution = factorXmin * factorYmax
    TRcontribution = factorXmax * factorYmin
    BRcontribution = factorXmax * factorYmax

    #get the result of each node
    return TL.GetValue() * TLcontribution + BL.GetValue() * BLcontribution + TR.GetValue() * TRcontribution + BR.GetValue() * BRcontribution

def globalToMeshCoords(x, y):
    from main import Data
    global meshWidth, meshHeight, Margin, meshCanvas, root
    #convert global coordinates to mesh coordinates
    canvasWidth = meshCanvas.winfo_width()
    canvasHeight = meshCanvas.winfo_height()
    smallestCanvasSize = min(canvasWidth, canvasHeight)
    largestCanvasSize = max(canvasWidth, canvasHeight)

    largestSize = max(Data.getWidth(), Data.getHeight())
    scale = (smallestCanvasSize - 2 * Margin) / largestSize
    xOffset = (largestSize - Data.getWidth()) / 2
    yOffset = (largestSize - Data.getHeight()) / 2
    xCanvasOffset = (largestCanvasSize - canvasHeight) / 2
    yCanvasOffset = (largestCanvasSize - canvasWidth) / 2
    x_canvas = (x + xOffset) * scale + Margin + xCanvasOffset
    y_canvas = (y + yOffset) * scale + Margin + yCanvasOffset
    return (x_canvas, y_canvas)