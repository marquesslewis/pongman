#!/usr/bin/python

import pyglet
from pyglet.gl import *
from math import pi, sin, cos

winXSize = 1280
winYSize = 768

#location of the paddle
paddle_x = int(0.75*winXSize)
paddle_y = winYSize/2
paddle_size = 200

#location of the ball
x1 = winXSize/2
y1 = winYSize/2
dx1 = 400
dy1 = 400 

ballRadius = 30

soundIsOn = True

win = pyglet.window.Window(winXSize, winYSize)

def update_position(dt):
  global x1, dx1, y1, dy1, winXSize, winYSize, ballRadius, ballSound, soundIsOn

  if(x1 > (winXSize-ballRadius) or x1 < ballRadius) : 
    dx1 = -dx1
    if( soundIsOn): ballSound.play()
  x1 += dt*dx1
  if(y1 > (winYSize-ballRadius) or y1 < ballRadius) : 
    dy1 = -dy1
    if( soundIsOn): ballSound.play()
  y1 += dt*dy1

  #print "pt 1 is now ", x1, " ", y1

def circle(x, y, radius):

    #iterations = int(2*radius*pi)
    iterations = 28
    s = sin(2*pi / iterations)
    c = cos(2*pi / iterations)

    dx, dy = radius, 0

    glColor4f(1.0, 1.0, 0.0, 1.0)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    for i in range(iterations-2):
        glVertex2f(x+dx, y+dy)
        dx, dy = (dx*c - dy*s), (dy*c + dx*s)
    glEnd()

def draw_paddle():
  glColor4f(0.2, 0.2, 1.0, 1.0)
  glLineWidth(4)
  glBegin(GL_LINES)
  glVertex2i(int(paddle_x), int(paddle_y+paddle_size/2))
  glVertex2i(int(paddle_x), int(paddle_y-paddle_size/2))
  glEnd()

def set_paddle_location(x, y):
  global paddle_y
  paddle_y = y

def ball_hit_paddle():
  global x1, ballRadius, paddle_size, paddle_x, paddle_y
  if (paddle_x - x1 < ballRadius) and ((y1 > paddle_y-paddle_size/2) and (y1 < paddle_y+paddle_size/2)):
    return True

def hit_the_ball():
  global soundIsOn, hitSound
  global dx1
  dx1 = -dx1
  if( soundIsOn): hitSound.play()

@win.event
def on_mouse_motion(x, y, dx, dy):
  win.clear()
  set_paddle_location(x,y)

@win.event
def on_draw():
  global x1, y1, ballRadius

  glClear(GL_COLOR_BUFFER_BIT)

  glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

  circle(x1, y1, ballRadius)

  draw_paddle()

  if ball_hit_paddle():
    hit_the_ball()

if __name__ == '__main__':
  if(soundIsOn): ballSound = pyglet.media.load('pong.wav', streaming=False)
  if(soundIsOn): hitSound = pyglet.media.load('hit.wav', streaming=False)
  pyglet.clock.schedule_interval(update_position, 1/50.0)
  pyglet.app.run()

