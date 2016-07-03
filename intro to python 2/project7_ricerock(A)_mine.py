http://www.codeskulptor.org/#user41_Re8Sur7ZeZfDLA2.py
# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
SCREEN_SIZE = [WIDTH, HEIGHT]
c = 0.05

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]

        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.thrust_center = [self.image_center[0] + self.image_size[0], self.image_center[1]]


    def draw(self, canvas):

        # draw ship with fire
        if self.thrust:
            canvas.draw_image(self.image, self.thrust_center, self.image_size, self.pos, self.image_size, self.angle)
        # draw ship without fire
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def inc_ang_vel(self, delta):
        self.angle_vel += delta

    def turn_on_thruster(self):
        self.thrust = True
    def turn_off_thruster(self):
        self.thrust = False

    def update(self):
        global c
        NUM_DIMENSIONS = 2

        # Update the position of a ship
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        # Update the friction
        self.vel[0] *= (1-c)
        self.vel[1] *= (1-c)

        # Ship's position wraps around the screen when it goes off the edge
        for d in range(NUM_DIMENSIONS):
            self.pos[d] = (self.pos[d] + self.vel[d]) % SCREEN_SIZE[d]

        # Velocity update - acceleration in direction of forward vector
        # Compute the forward vector pointing in the direction the ship is facing
        forward = angle_to_vector(self.angle)

        if  self.thrust:
            # add thrust sound when ship is thrusting
            ship_thrust_sound.play()
            # accelerate the ship when ship is thrusting
            self.vel[0] += forward[0] * 0.4
            self.vel[1] += forward[1] * 0.4
        else:
            ship_thrust_sound.rewind()


        # increment and decrement the angular velocity by a fixed amount
        self.angle = (self.angle + self.angle_vel) % (2 * math.pi)

    def shoot(self):
        global a_missile

        pos = [0, 0]
        forward = angle_to_vector(self.angle)
        vel_factor = 2
        vel = [forward[0] * vel_factor + self.vel[0], forward[1] * vel_factor + self.vel[1]]

        NUM_DIMENSIONS = 2

        for d in range(NUM_DIMENSIONS):
            pos[d] = self.pos[d] + forward[d] * self.radius

        a_missile = Sprite(pos, vel, 0, 0, missile_image, missile_info, missile_sound)

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        # rock moves
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        # rock's position wraps around the screen when it goes off the edge
        NUM_DIMENSIONS = 2
        for d in range(NUM_DIMENSIONS):
            self.pos[d] = (self.pos[d] + self.vel[d]) % SCREEN_SIZE[d]
        # increment and decrement the angular velocity by a fixed amount
        self.angle = (self.angle + self.angle_vel) % (2 * math.pi)

def draw(canvas):
    global time

    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    if a_missile != None:
        a_missile.draw(canvas)

    # update ship and sprites
    my_ship.update()
    a_rock.update()
    if a_missile != None:
        a_missile.update()

    # live and score system
    canvas.draw_text('Lives', (100, 75), 30, 'White')
    canvas.draw_text('Score', (600, 75), 30, 'White')
    canvas.draw_text(str(lives), (100, 120), 30, 'White')
    canvas.draw_text(str(score), (600, 120), 30, 'White')

# timer handler that spawns a rock
def rock_spawner():
    global a_rock
    vel = [0,0]

    vel[0] = (random.random() - 0.5)* 3
    vel[1] = (random.random() - 0.5)* 2
    ang = random.random()* 2 * math.pi
    ang_vel = (random.random()- 0.5)* 0.4

    pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]

    a_rock = Sprite(pos, vel, ang, ang_vel, asteroid_image, asteroid_info)

UP_KEY = 38
LEFT_KEY = 37
RIGHT_KEY = 39
SPACE_KEY = 32

def keydown(key):
    #  turn the thrusters on/off in response to up/down arrow keys
    if UP_KEY == key:
        my_ship.turn_on_thruster()

    # ship turns in response to left/right arrow keys
    if LEFT_KEY == key:
        my_ship.inc_ang_vel(-0.1)
    if RIGHT_KEY == key:
        my_ship.inc_ang_vel(0.1)

    if SPACE_KEY == key:
        my_ship.shoot()

def keyup(key):
    #  turn the thrusters on/off in response to up/down arrow keys
    if UP_KEY == key:
        my_ship.turn_off_thruster()

    if LEFT_KEY == key:
        my_ship.inc_ang_vel(0.1)
    if RIGHT_KEY == key:
        my_ship.inc_ang_vel(-0.1)


# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = None
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
