from ursina import *

app = Ursina()

window.title = 'Black Hole Simulation'
window.borderless = False
window.fullscreen = False
window.color = color.black

camera.position = (0, 0, -15)

# First entity as a star 
star = Entity(
    model='sphere',
    color=color.white,
    scale=0.1,
    position=(5, 3, 5)
)

player = EditorCamera()

app.run()