from tkinter import *

width = None
height = None
boundary_conditions_str = None


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




def create():
    global width, height, boundary_conditions_str
    
    #main window
    root = Tk()
    root.title("Numerische Simulationen: FEM Simulation")
    root.geometry("800x600")

    #create input for mesh width and height
    Label(root, text="Width:").grid(row=0, column=0)
    width = Entry(root)
    width.insert(0, "10")
    width.grid(row=0, column=1)

    Label(root, text="Height:").grid(row=1, column=0)
    height = Entry(root)
    height.insert(0, "10")
    height.grid(row=1, column=1)

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


    #tkinter loop
    root.mainloop()
    #todo: add quit function, maybe in main.py?
    #for freeing resources, maybe add a quit button to the gui
    



