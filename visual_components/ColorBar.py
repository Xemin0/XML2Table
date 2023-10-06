"""
Static Color Bar to Indicate the Color Range
Based on Provided color-computing method
"""

import tkinter as tk

class ColorBar:
    def __init__(self, root, compute_color_func, W = 25, H = 200):
        self.root = root
        self.compute_color = compute_color_func

        self.canvas = tk.Canvas(self.root, width = W, height = H)
        self.canvas.pack(pady = 20, padx = 20)


        self.W = W
        self.H = H
        self.draw_color_bar(0, 1)


    def draw_color_bar(self, min_val = 0, max_val = 1):
        #bar_height = self.canvas.winfo_height()
        #bar_width = self.canvas.winfo_width()
        num_steps = 100 # Number of color steps in the gradient
        step_height = self.H / num_steps

        for i in range(num_steps):
            value =  min_val + (max_val - min_val) * ( (i+0.0) / num_steps)
            color = self.compute_color(value, min_val, max_val)
            self.canvas.create_rectangle(0, i*step_height, self.W, (i+1)*step_height, fill = color, outline = color)

        self.canvas.create_text(int(self.W / 2) + 2, 0, text = 'min', anchor = 'n')
        self.canvas.create_text(int(self.W / 2) + 2, self.H, text = 'max', anchor = 's')

"""
Test
def compute_color(value, m, n):
    ratio = (value - m)/ (n - m)
    red = int(255 * ratio)
    green = int(255 * (1 - ratio))
    blue = 180
    return f'#{red:02x}{green:02x}{blue:02x}'


window = tk.Tk()
cb = ColorBar(window, compute_color)
window.mainloop()
"""
