import numpy as np
from field import field
import geometer as geo
from matplotlib.patches import Circle


class ball:
    def __init__(self, circle):
        self.circle = circle
        self.press = None
        self.x = 0
        self.y = 0
    # connect to events
    def connect(self):
        self.cidpress = self.circle.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.circle.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.circle.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    # if the press event was inside a circle, select that circle
    def on_press(self, event):
        if event.inaxes != self.circle.axes: return
        contains, attrd = self.circle.contains(event)
        if not contains: return
        x0, y0 = self.circle.center[0], self.circle.center[1]
        self.press = x0, y0, event.xdata, event.ydata

    # if the mouse is moving, and the circle is pressed, move the circle
    def on_motion(self, event):
        if self.press is None: return
        if event.inaxes != self.circle.axes: return

        x0, y0, xpress, ypress = self.press

        dx = event.xdata - xpress
        dy = event.ydata - ypress

        self.circle.center[0] = (x0 + dx)
        self.circle.center[1] = (y0 + dy)
        self.x = self.circle.center[0]
        self.y = self.circle.center[1]

        self.circle.figure.canvas.draw()

    # when the circle is released, redraw the canvas
    def on_release(self, event):
        'on release we reset the press data'
        self.press = None
        self.circle.figure.canvas.draw()

    # allow the robot circle to be disconnected from the mpl figure
    def disconnect(self):
        'disconnect all the stored connection ids'
        self.circle.figure.canvas.mpl_disconnect(self.cidpress)
        self.circle.figure.canvas.mpl_disconnect(self.cidrelease)
        self.circle.figure.canvas.mpl_disconnect(self.cidmotion)

    # calculate distance between robot and point (x,y)
    def distance(self, x, y):
        length = (x - self.circle.center[0]) ** 2 + (y - self.circle.center[1]) ** 2
        return np.sqrt(length)

