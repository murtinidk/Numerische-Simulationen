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
from tkinter import messagebox

# initialize the data storage
Data: data.DataClass = data.DataClass()
# declarations
# main function, called on button press in gui
def main_simulation(): 
    gui.setStep(gui.simStep.started)
    global Data
    try:
        Data.reset()
        Data.setSize(gui.get_width(), gui.get_height(), gui.get_xResolution(), gui.get_yResolution())
        Data.setLine(gui.get_line())
        Data.setBoundary(gui.getLeftBoundaryValue(), gui.getTopBoundaryValue(), gui.getBottomBoundaryValue(), gui.getRightBoundaryValue())
        Data.setTensor(gui.get_Tensor())
        Data.setIntegrationOrder(gui.getIntegrationOrder())
        from mesh.meshgen import meshgen 
        meshgen()
        from calculation.calculate import calculate
        calculate()
    except Exception as e:
        messagebox.showerror("Unresolved Error in Simulation", f"There was an uncaught Exception:\n{e}")
        return

    gui.setStep(gui.simStep.finished)

#main function 
if __name__ == "__main__":
    from interface.gui import valueInElement
    gui.create()

