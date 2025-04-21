#- main program project file
#- Numerische Simulationen für Digital Engineering, SS 2025
#- Gruppe 6: Ram Abhay, Figo Tobias, Thalmayr Martin

#inclusions
import interface.gui as gui
from mesh.meshgen import meshgen 

# declarations
# main function, called on button press in gui
def main_simulation():
    width = gui.get_width()
    height = gui.get_height()
    boundary = gui.get_boundary_condition()
    print(f"Starting simulation with width={width}, height={height}, boundary={boundary}")
    meshgen()



#main function 
if __name__ == "__main__":
    gui.create()

