from tkinter import Canvas
class PanableCanvas(Canvas):
    def __init__(self, master, width, height, bg="lightgrey"):
        Canvas.__init__(self, master, width=width, height=height, bg=bg)
        self.bind("<ButtonPress-1>", self.start_pan)
        self.bind("<B1-Motion>", self.pan)
        self.bind("<MouseWheel>", self.zoom)  # Windows 
        self.bind("<Button-4>", self.zoom_linux)  # Linux scroll up
        self.bind("<Button-5>", self.zoom_linux)  # Linux scroll down
        self.scale = 1.0
        self.offset_x = 0
        self.offset_y = 0

    def start_pan(self, event):
        self.scan_mark(event.x, event.y)

    def pan(self, event):
        self.scan_dragto(event.x, event.y, gain=1)

    def reset_view(self):
        self.scale = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.configure(scrollregion=self.bbox("all"))
        self.update()

    def zoom(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        factor = 1.1 if event.delta > 0 else 0.9
        self.scale *= factor
        self.scale_all(factor, factor, x, y)
        self.configure(scrollregion=self.bbox("all"))
        self.update()

    def zoom_linux(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        if event.num == 4:
            factor = 1.1  # Scroll up
        elif event.num == 5:
            factor = 0.9  # Scroll down
        else:
            factor = 1.0
        self.scale *= factor
        self.scale_all(factor, factor, x, y)
        self.configure(scrollregion=self.bbox("all"))
        self.update()

    def scale_all(self, scale_x, scale_y, offset_x, offset_y):
        for tag in self.find_all():
            coords = self.coords(tag)
            new_coords = []
            for i in range(0, len(coords), 2):
                x = coords[i]
                y = coords[i+1]
                new_x = (x - offset_x) * scale_x + offset_x
                new_y = (y - offset_y) * scale_y + offset_y
                new_coords.append(new_x)
                new_coords.append(new_y)
            self.coords(tag, *new_coords)