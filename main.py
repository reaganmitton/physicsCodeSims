import pygame
pygame.init()
import math
from pygame.rect import Rect
from sympy import *
from sympy.physics.mechanics import*
init_vprinting()
import scipy
import math
import numpy as np


#random variables
FPS = 60
white = (255, 255, 255)
blue = (106, 159, 181)
red = (153, 0, 0)
object_mass = 1
k = 30
g = 9.81
dt = 1 / FPS
button_rect = pygame.Rect(500, 40, 100, 50)
fixed_s_endpoint = 80
font = pygame.font.SysFont("Arial", 15)
spring_left_boundary = 150
spring_right_boundary = 300
K = 20


#window
(width, height) = (700, 500)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("U and K on a spring")
screen.fill(white)
clock = pygame.time.Clock()


#title
def some_text():
    text_surface = font.render("Potential and Kinetic Energy on an Oscillating Object", True, "blue")
    screen.blit(text_surface, ((20, 15)))

    #github info
    subtext_font = pygame.font.SysFont("Arial", 13)
    text_surface_info = subtext_font.render("Github: reaganmitton", True, "blue")
    screen.blit(text_surface_info, ((20, 35)))

    text_surface = subtext_font.render(f"K: {k} N/M", True, "blue")
    screen.blit(text_surface, ((20, 55)))

    text_surface_2 = subtext_font.render(f"Mass: {object_mass} KG", True, "blue")
    screen.blit(text_surface_2, ((20, 75)))


#draw basic setup
def setUp():
    pygame.draw.rect(screen, red, (80, 350, 40, 90))
    pygame.draw.rect(screen, red, (80, 420, 280, 30))

#loading ruler image
def referencing():
    og_ruler_img = pygame.image.load("ruler.png").convert_alpha()
    resized_ruler_img = pygame.transform.smoothscale(og_ruler_img, (360, 600))
    screen.blit(resized_ruler_img, (60, 190))

def draw_equilibrium():
    pygame.draw.line(screen, "light blue", (240, 420), (240, 330), 4)
    equil_text_surface = font.render("Equilibrium (5 cm)", True, "light blue")
    screen.blit(equil_text_surface, ((200, 300)))

def hookes_law_movement(k, f):
    x0 = 5
    x = f/k + x0
    return

def accel(f, m):
    a = f/m
    return a


class Mass:
    def __init__(self, x, y, color, v, a, x_eq):
        self.x = x
        self.y = y
        self.color = color
        self.speed = 0
        self.x0 = 0
        self.y0 = 5
        self.v = v
        self.a = a
        self.x_eq = x_eq
        self.left_movement = False

    def display(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 40, 40))
        #equilibrium is at 215

    def movement(self):
        if self.left_movement:
            if self.x <= spring_left_boundary:
                self.left_movement = False
                print("moving towards left boundary")
            else:
                self.x -= 1
        else:
            if self.x >= spring_right_boundary:
                self.left_movement = True
                print("moving towards right boundary")
            else:
                self.x += 1
    def physics(self, k, m, t):
        displacement = self.x - self.x_eq
        f = -k*displacement
        self.a = f/m
        self.v += self.a * t
        self.x += self.v * t

        print(f"displacement: {displacement}, force: {f}, accel: {self.a}, vel: {self.v}, pos: {self.x}")
        print("physics mass method running")



class Spring:
    def __init__(self, fixed_x, end_point, rest_l, k, m):
        self.fixed_x = fixed_x
        self.end_point = end_point
        self.rest_l = rest_l
        self.k = k
        self.m = m
        self.left_movement = False

    def draw(self, color, width):
        self.color = color
        self.width = width
        start_pos = (self.fixed_x, 400)
        end_pos = (self.end_point, 400)
        pygame.draw.line(screen, color, start_pos, end_pos, width)
    def movement_force(self, force, time, a):
        '''*self.force = force
        x = hookes_law_movement(k, force)
        self.end_point += x'''
        v = 0
        x = 5
        v += a * time
        self.end_point += v * time

        """if self.left_movement:
            if self.end_point <= spring_left_boundary:
                self.left_movement = False
                print("moving towards left boundary")
            else:
                self.end_point -= 1
        else:
            if self.end_point >= spring_right_boundary:
                self.left_movement = True
                print("moving towards right boundary")
            else:
                self.end_point += 1"""



def draw_play_button(is_running):
    color = "green" if is_running else "orange"
    pygame.draw.rect(screen, color, button_rect)
    text = "stop" if is_running else "play"
    button_txt_surface = font.render(text, True, "yellow" if not is_running else "purple")
    screen.blit(button_txt_surface, (530, 55))


#initializing components
my_spring = Spring(110, 250, 60, 10, 10)
my_mass = Mass(250, 380, "pink", 0, 0, 223)

running = True
running_sim = False

while running:
    dt = clock.tick(FPS) / 1000.0
    screen.fill("white")
    some_text()


    my_mass.display()
    draw_equilibrium()
    my_spring.draw("purple", 4)

    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        button_color = "blue"
    else:
        button_color = "orange"
    draw_play_button(running_sim)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                #running_sim = True
                running_sim = not running_sim
                print("play button clicked")


    if running_sim:
        #my_spring.movement()
        my_mass.physics(k, object_mass, dt)
        my_spring.end_point = my_mass.x

    setUp()
    referencing()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()

