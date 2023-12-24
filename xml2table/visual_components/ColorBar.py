"""
Static Color Bar to Indicate the Color Range
Based on Provided color-computing method
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt

class ColorBar(QWidget):
    def __init__(self, parent, compute_color_func, W = 25, H = 200):
        super().__init__(parent)
        self.compute_color = compute_color_func

        self.W = W
        self.H = H
        self.setMinimumSize(self.W, self.H)
        self.draw_color_bar(0, 1)


    def draw_color_bar(self, min_val = 0, max_val = 1):
        self.min_val = min_val
        self.max_val = max_val
        self.update()  # trigger a repaint of the override method

    def paintEvent(self, event):
        painter = QPainter(self)
        num_steps = 100 # Number of color steps in the gradient
        step_height = self.H / num_steps

        for i in range(num_steps):
            # starting from top-min to bottom-max
            #value =  min_val + (max_val - min_val) * ( (i+0.0) / num_steps)
            # starting from top-max to bottom-min
            value =  self.max_val - (self.min_val + (self.max_val - self.min_val) * ( (i+0.0) / num_steps))
            color = self.compute_color(value, self.min_val, self.max_val)
            # Convert float values to int
            y_pos = int(i * step_height)
            h = int(step_height)
            painter.fillRect(0, y_pos, self.W, h, QColor(color))


        # Draw max and min labels
        fontSize = 12
        painter.setFont(QFont('Arial', fontSize, QFont.Bold))
        painter.drawText(0, fontSize - 2, 'max')
        painter.drawText(2, self.H - 2, 'min')

"""
Test
def compute_color(value, m, n):
    ratio = (value - m)/ (n - m)
    red = int(255 * ratio)
    green = int(255 * (1 - ratio))
    blue = 180
    return f'#{red:02x}{green:02x}{blue:02x}'


"""
