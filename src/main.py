from pyglet.gl import *
from pyglet.window import mouse
from boid import *
from force import *

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        pyglet.window.Window.__init__(self, *args,**kwargs)
        self.flock = Flock(100, windowSize)
        self.force = Force(-250)

    def on_draw(self):
        glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
        glColor3f(1, 0, 0)
        self.flock.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self.force.update(x, y)

    def on_mouse_leave(self, x, y):
        self.force.on(False)

    def on_mouse_enter(self, x, y):
        self.force.on(True)

    def on_mouse_press(self, x, y, button, modifiers):
        if button & mouse.LEFT:
            self.flock.addBoid(x, y, windowSize)

    def update(self, time):
        self.flock.update(self.force)
        self.flock.draw()

windowSize = 600

window = Window(width = windowSize, height = windowSize, caption = 'Boids')

pyglet.clock.schedule_interval(window.update, 1/30)
pyglet.app.run()
