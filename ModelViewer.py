# Most of this code was skidded from an old project, "Collin"

from turtle import width
import ursina as urs

class orbit_object(urs.Entity):
    def update(self):
        if destroy: urs.application.quit()
        orbit.rotation_y -= rotatespeed
        if urs.mouse.middle and not urs.held_keys["shift"]:
            urs.camera.orthographic = False
            orbit.rotation_y += urs.mouse.velocity[0] * urs.time.dt * 30000
            orbit.rotation_x -= -urs.mouse.velocity[1] * urs.time.dt * 25000
            
            if orbit.rotation_x > 90:
                orbit.rotation_x = 90
            
            if orbit.rotation_x < -90:
                orbit.rotation_x = -90
    
def init():
    global app, orbit, destroy, rotatespeed, debugtext
    app = urs.Ursina()
    urs.window.title = 'Model View'
    urs.window.forced_aspect_ratio = 1
    urs.window.windowed_size = urs.window.fullscreen_size / 2.5
    urs.window.borderless = False
    urs.window.fullscreen = False
    urs.window.exit_button.visible = False
    urs.window.fps_counter.enabled = False
    urs.window.icon = "icon.ico"

    urs.window.color = urs.Color(0.1, 0.1, 0.1, 1)

    x = 2

    urs.Texture.default_filtering = "bilinear"

    urs.camera.rotation_y = 180
    urs.camera.rotation_x = 0
    urs.camera.position = (0, 0, x)
    urs.camera.fov = 30

    orbit = orbit_object(model="cube", visible=False)
    urs.camera.parent = orbit
    orbit.rotation_x -= 30
    orbit.rotation_y -= 45


    debugtext = urs.Text(text="", position=(0, 0.4, 0), origin=(0, 0))
    debugtext.scale = (2, 2)


    destroy = False
    rotatespeed = 0.5

if __name__ == "__main__":
    init()