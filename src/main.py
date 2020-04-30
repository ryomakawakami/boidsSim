from pyglet.gl import *
from pyglet.window import mouse
from boid import *

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        pyglet.window.Window.__init__(self, *args,**kwargs)
        self.flock = Flock(150, windowSize[0], windowSize[1])

    def on_draw(self):
        glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
        glColor3f(1, 0, 0)
        self.flock.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button & mouse.LEFT:
            self.flock.addBoid(x, y, windowSize)

    def update(self, time):
        self.flock.update()
        self.flock.draw()

windowSize = [1200, 600]

window = Window(width = windowSize[0], height = windowSize[1], caption = 'Boids')

pyglet.clock.schedule_interval(window.update, 1/30)
pyglet.app.run()
