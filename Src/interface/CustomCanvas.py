from tkinter import Canvas, ALL

#code segments from https://www.w3resource.com/python-exercises/tkinter/python-tkinter-canvas-and-graphics-exercise-9.php

class PanableCanvas(Canvas):
    def __init__(self, master, width, height, bg="lightgrey"):
        Canvas.__init__(self, master, width=width, height=height, bg=bg)
        self.bind("<ButtonPress-1>", self.start_pan)
        self.bind("<B1-Motion>", self.pan)
        self.bind("<MouseWheel>", self.zoom_event)      # Windows 
        self.bind("<Button-4>", self.zoom_event_linux)  # Linux scroll up
        self.bind("<Button-5>", self.zoom_event_linux)  # Linux scroll down
        self.scale_factor = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.last_redraw_scale = 1.0

    def start_pan(self, event):
        self.scan_mark(event.x, event.y)

    def pan(self, event):
        self.scan_dragto(event.x, event.y, gain=1)

    def zoom_canvas(self, x, y, factor):
        self.scale(ALL, x, y, factor, factor)
        self.scale_factor *= factor
        self.configure(scrollregion=self.bbox("all"))

    def zoom_event(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        factor = 1.1 if event.delta > 0 else 0.9 #zoom in or out depending on the scroll direction -> delta 
        self.zoom_canvas(x, y, factor)

    def zoom_event_linux(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        factor = 1.0
        if event.num == 4:
            factor = 1.1  # Scroll up -> on linux this is a button map ??
        elif event.num == 5:
            factor = 0.9  # Scroll down
        if factor != 1.0:
            self.zoom_canvas(x, y, factor)