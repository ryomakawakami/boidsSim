from pyglet.gl import *
from boid import *

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        pyglet.window.Window.__init__(self, *args,**kwargs)
        self.flock = Flock(1)

    def on_draw(self):
        glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
        glColor3f(1, 0, 0)
        self.flock.draw()

    def update(self, time):
        self.flock.update()
        self.flock.draw()

window = Window(width = 500, height = 500, caption = 'Boids')

pyglet.clock.schedule_interval(window.update, 1/30)
pyglet.app.run()
