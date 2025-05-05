#- main program project file
#- Numerische Simulationen für Digital Engineering, SS 2025
#- Gruppe 6: Ram Abhay, Figo Tobias, Thalmayr Martin

# x = Width
# y = Heigt
# 0 = oben links
#   ----> x
#  |
#  |
# \/
#  y


#inclusions
import interface.gui as gui
import data.dataStorage as data

# initialize the data storage
Data: data.DataClass = data.DataClass()
# declarations
# main function, called on button press in gui
def main_simulation(): 
    global Data
    Data.reset()
    Data.setSize(gui.get_width(), gui.get_height(), gui.get_boundary_condition(), gui.get_xResolution(), gui.get_yResolution())
    print(f"Starting simulation with width={Data.getWidth()}, height={Data.getHeight()}, boundary={Data.getBoundary()}")
    from mesh.meshgen import meshgen 
    meshgen()



#main function 
if __name__ == "__main__":
    gui.create()

