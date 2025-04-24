#- main program project file
#- Numerische Simulationen für Digital Engineering, SS 2025
#- Gruppe 6: Ram Abhay, Figo Tobias, Thalmayr Martin

#inclusions
import interface.gui as gui
from mesh.meshgen import meshgen 
import data.dataStorage

# declarations
# main function, called on button press in gui
def main_simulation():
    Data = data.dataStorage.Data()
    Data.setSize(gui.get_width(), gui.get_height(), gui.get_boundary_condition())
    print(f"Starting simulation with width={Data.getWidth()}, height={Data.getHeight()}, boundary={Data.getBoundary()}")
    meshgen()



#main function 
if __name__ == "__main__":
    gui.create()

