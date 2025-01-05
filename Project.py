# Car Racing Game #

from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import time
s_width, s_height = 800, 800
next_regular_spawn_time = 0
_r = 10
_x, _y = 300, 100
car_1_x= 250
car_1_y= 50
car_2_x= 500
car_2_y=50
falling = []
falling_speed = 2
start_time = time.time()
flag_gameOver = False
flag_pause = False
flag_animate = True

def int_FindZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    zone = 0
    if abs(dx) > abs(dy):
        if dx>=0 and dy>0:
            zone = 0
        elif dx<=0 and dy>=0:
            zone = 3
        elif dx<0 and dy<0:
            zone = 4
        elif dx>0 and dy<0:
            zone = 7
    else:
        if dx >= 0 and dy > 0:
            zone = 1
        elif dx < 0 and dy > 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        elif dx >= 0 and dy < 0:
            zone = 6
    return zone

def convertToZero(x,y,zone):
    if zone == 1:
        X, Y = y, x
    elif zone == 2:
        X, Y = y, -x
    elif zone == 3:
        X, Y = -x, y
    elif zone == 4:
        X, Y = -x, -y
    elif zone == 5:
        X, Y = -y, -x
    elif zone == 6:
        X, Y = -y, x
    elif zone == 7:
        X, Y = x, -y
    return int(X),int(Y)

def convertToOriginal(x,y,zone):
    if zone == 1:
        X, Y = y, x
    elif zone == 2:
        X, Y = -y, x
    elif zone == 3:
        X, Y = -x, y
    elif zone == 4:
        X, Y = -x, -y
    elif zone == 5:
        X, Y = -y, -x
    elif zone == 6:
        X, Y = y, -x
    elif zone == 7:
        X, Y = x, -y
    return int(X), int(Y)

def drawPoint(x, y, size=1.5):
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(int(x),int(y))
    glEnd()

def drawLine(x1, y1, x2, y2, color):
    glColor3f(*color)
    zone = int_FindZone(x1, y1, x2, y2)
    if zone != 0:
        x1, y1 = convertToZero(x1,y1,zone)
        x2, y2 = convertToZero(x2, y2, zone)
    dx = x2 - x1
    dy = y2 - y1
    d = 2*dy - dx
    incE = 2*dy
    incNE = 2*(dy-dx)
    y = y1
    for x in range(int(x1), int(x2)):
        if zone != 0:
            original_x, original_y = convertToOriginal(x, y, zone)
            drawPoint(original_x, original_y)
        else:
            drawPoint(x, y)
        if d>0:
            d = d + incNE
            y += 1
        else:
            d = d + incE

def draw_circle(r, value):
   global screen_height, screen_width
   d = 1-r
   x = 0
   y = r
   circle_points(x, y, value)
   while x<y:
       if d<0:
           d = d + 2*x + 3
           x = x + 1
       else:
           d = d + 2*x - 2*y + 5
           x = x + 1
           y = y - 1
       circle_points(x, y, value)

def circle_points(x, y, value):
    cx, cy  = value[0], value[1]
    drawPoint(x+cx, y+cy)
    drawPoint(y+cx, x+cy)
    drawPoint(y+cx, -x+cy)
    drawPoint(x+cx, -y+cy)
    drawPoint(-x+cx, -y+cy)
    drawPoint(-y+cx,-x+cy)
    drawPoint(-y+cx, x+cy)
    drawPoint(-x+cx, y+cy)
    
def draw_restart_button():
    drawLine(20, s_height-30, 60, s_height-30, (0, 1, 1))
    drawLine(20, s_height-30, 30, s_height-20, (0, 1, 1))
    drawLine(20, s_height-30, 30, s_height-40, (0, 1, 1))

def draw_pause_button():
    if flag_pause:
        drawLine(s_width//2 - 5, s_height - 20, s_width//2 - 5, s_height - 40, (0.7, 1, 0))
        drawLine(s_width//2 - 5, s_height - 40, s_width//2 + 15, s_height - 30, (0.7, 1, 0))
        drawLine(s_width//2 - 5, s_height - 20, s_width//2 + 15, s_height - 30, (0.7, 1, 0))
    else:
        drawLine(s_width // 2 + 5, s_height - 20, s_width // 2 + 5, s_height - 40, (1, 0.7, 0))
        drawLine(s_width//2 - 5, s_height - 20, s_width//2 - 5, s_height - 40, (1, 0.7, 0))

def draw_exit_button():
    drawLine(s_width - 40, s_height - 40, s_width - 20, s_height - 20, (1, 0, 0))
    drawLine(s_width - 40, s_height - 20, s_width - 20, s_height - 40, (1, 0, 0))

def draw_(): #Road
    col=glColor3f(1,1,0)
    drawLine(100,0,100,800,(1,0,0))
    drawLine(700,0,700,800,(1,0,0))
    drawLine(90,0,90,800,(0,1,0))
    drawLine(710,0,710,800,(0,1,0))

def draw_car_1(): #car 1
    global car_1_x, car_1_y
    col=glColor3f(1,1,0)
    drawLine(car_1_x, car_1_y,car_1_x+50,car_1_y,(1,1,0)) #H1 Nicher line ta
    drawLine(car_1_x-25, car_1_y+25,car_1_x+75,car_1_y+25,(1,1,0))#H2
    drawLine(car_1_x-25, car_1_y+175,car_1_x+75,car_1_y+175,(1,1,0))#H3
    drawLine(car_1_x, car_1_y+225,car_1_x+50,car_1_y+225,(1,1,0))#H4 uporer line
    drawLine(car_1_x-25, car_1_y+25,car_1_x-25,car_1_y+175,(1,1,0))#V1
    drawLine(car_1_x+75, car_1_y+25,car_1_x+75,car_1_y+175,(1,1,0))#V2
    drawLine(car_1_x, car_1_y,car_1_x-25, car_1_y+25,(1,1,0))#Angel left bottom
    drawLine(car_1_x+50,car_1_y,car_1_x+75, car_1_y+25,(1,1,0))#Angel right bottom
    drawLine(car_1_x-25, car_1_y+175,car_1_x, car_1_y+225,(1,1,0))#Angel left top
    drawLine(car_1_x+75,car_1_y+175,car_1_x+50,car_1_y+225,(1,1,0))#Angel right top
   
def draw_car_2(): #car 2 enemy
    global car_2_x, car_2_y
    col=glColor3f(1,1,0)
    drawLine(car_2_x, car_2_y,car_2_x+50,car_2_y,(1,0,0)) #H1 Nicher line ta
    drawLine(car_2_x-25, car_2_y+25,car_2_x+75,car_2_y+25,(1,0,0))#H2
    drawLine(car_2_x-25, car_2_y+175,car_2_x+75,car_2_y+175,(1,0,0))#H3
    drawLine(car_2_x, car_2_y+225,car_2_x+50,car_2_y+225,(1,0,0))#H4 uporer line
    drawLine(car_2_x-25, car_2_y+25,car_2_x-25,car_2_y+175,(1,0,0))#V1
    drawLine(car_2_x+75, car_2_y+25,car_2_x+75,car_2_y+175,(1,0,0))#V2
    drawLine(car_2_x, car_2_y,car_2_x-25, car_2_y+25,(1,0,0))#Angel left bottom
    drawLine(car_2_x+50,car_2_y,car_2_x+75, car_2_y+25,(1,0,0))#Angel right bottom
    drawLine(car_2_x-25, car_2_y+175,car_2_x, car_2_y+225,(1,0,0))#Angel left top
    drawLine(car_2_x+75,car_2_y+175,car_2_x+50,car_2_y+225,(1,0,0))#Angel right top
circle_flag = False
cross_flag = False
triangle_flag = False
def draw_triangle(x,y):
    drawLine(x,y,x+15,y,(1,1,1)) #H1 Nicher line ta
    drawLine(x,y,x+7.5,y+15,(1,1,1))#H2
    drawLine(x+7.5,y+15,x+15,y,(1,1,1))

def draw_cross(x,y):
    drawLine(x,y,x+15,y+15,(1,1,1)) #H1 Nicher line ta
    drawLine(x,y+15,x+15,y,(1,1,1))#H2

def mouse_click(button, state, x, y):
    global s_width, s_height, _x, _y, _r, falling, falling_speed, shot, shot_speed, flag_gameOver, flag_pause, flag_animate, lives, score, misfire
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        print(f"Mouse click at: ({x}, {y})")
        y = s_height - y
        if (s_width - 40 <= x <= s_width - 20) and (s_height - 40 <= y <= s_height - 20):
            print(f"Goodbye. Your Final Score: {score}")
            glutLeaveMainLoop()
        elif (s_width // 2 - 20 <= x <= s_width // 2 + 16) and (s_height - 50 <= y <= s_height - 10):
            if flag_gameOver == False:
                flag_pause = not flag_pause
                flag_animate = False
        elif (20 <= x <= 60) and (s_height - 50 <= y <= s_height - 10):
            print("Starting Over")
            flag_gameOver = False
            flag_pause = False
            default_all()
            
def keyboardListener(key, x, y): #Car 1 left right
    global car_1_x, car_2_x
    if not flag_pause and not flag_gameOver:
        move = 5
        if key == b'l': #left
            if car_1_x > (100+30):  #left border boundry
                car_1_x -= move
        elif key == b'r': #right
            if car_1_x < (700-80-20):#right border boun
                car_1_x += move
            collision()
    glutPostRedisplay()
def collision():  #Car Collision
    global car_1_x, car_2_x, car_2_y, car_1_y, score
    b_1_left = car_1_x - 25
    b_1_right = car_1_x + 75
    b_1_top = car_1_y + 225
    b_1_bottom = car_1_y
    # Car_2 Box 
    b_2_left = car_2_x - 25
    b_2_right = car_2_x + 75
    b_2_top = car_2_y + 225
    b_2_bottom = car_2_y
    # Check for overlap on both x and y axes
    if b_1_right >= b_2_left and b_1_left <= b_2_right:  # Check if horizontal overlap
        if b_1_top >= b_2_bottom and b_1_bottom <= b_2_top:  # Check if vertical overlap
            # Collision detected
            print(f"Game Over. Your Final Score : {score}")
            glutLeaveMainLoop()


import random
import time

# Timing variables
last_fall_time = time.time()
fall_interval = random.uniform(0, 3) 
batch_start_time = time.time()
batch_interval = 10 
falling_elements = [] 
falling_elements_positions = [] 
batch_elements_count = 0 

score=0

def update_falling_elements():
    global f_start_y, finish, score,last_fall_time, fall_interval, batch_start_time, car_2_x, car_2_y, falling_elements, falling_elements_positions, batch_elements_count, car_1_x, car_1_y
    current_time = time.time()
    if current_time - last_fall_time >= fall_interval:
        last_fall_time = current_time  # Reset the timer for the next element
        fall_interval = random.uniform(1, 4)  
        if batch_elements_count < 3:  # Ensure only 3 elements (triangle, circle, cross) per batch
            if batch_elements_count == 0:
                falling_elements.append("triangle")
            elif batch_elements_count == 1:
                falling_elements.append("circle")
            else:
                falling_elements.append("cross")
            falling_elements_positions.append([random.randint(130, 620), s_height])
            batch_elements_count += 1

    if batch_elements_count == 3 and current_time - batch_start_time >= batch_interval:
        batch_start_time = current_time  # Reset 
        batch_elements_count = 0  # Reset
    #Manage Car 1 special characters
    b_1_left = car_1_x - 25
    b_1_right = car_1_x + 75
    b_1_top = car_1_y + 225
    for i, element in enumerate(falling_elements):
        element_x, element_y = falling_elements_positions[i]
        if element == "triangle":
            if b_1_left <= element_x <= b_1_right and b_1_left <= element_x + 15 <= b_1_right and element_y <= b_1_top :
                if car_1_y + 200 <= 600: #Finishing line :600
                    car_1_y += 50
                    
                    print("Car collided with triangle! Speed increased.")
                    
                falling_elements.pop(i)
                falling_elements_positions.pop(i)
                break
        elif element == "circle":
            
            if b_1_left <= element_x - 10 <= b_1_right and b_1_left <= element_x + 10 <= b_1_right and element_y + 10 <= b_1_top :      
                    
                score+=10 
                print(f"Hurray! Your Current Score : {score}")
                 
                falling_elements.pop(i)
                falling_elements_positions.pop(i)
                break
        elif element == "cross":
            
            if b_1_left <= element_x <= b_1_right and b_1_left <= element_x + 15 <= b_1_right and element_y <= b_1_top :
                if car_1_y >= 100: 
                    car_1_y -= 50
                     
                    print("Car collided with cross! Speed decreased.")
                    
                falling_elements.pop(i)
                falling_elements_positions.pop(i)
                break
    #Manage car 2 collision
    b_2_left = car_2_x - 50
    b_2_right = car_2_x + 75
    b_2_top = car_2_y + 225
    for i, element in enumerate(falling_elements):
        element_x, element_y = falling_elements_positions[i]
        if element == "triangle":
            
            if b_2_left <= element_x <= b_2_right and b_2_left <= element_x + 15 <= b_2_right and element_y <= b_2_top :
                if car_2_y + 200 <= 600: #Finishing line :600
                    car_2_y += 50
                     
                    print("Car collided with triangle! Speed increased.")
                    
                falling_elements.pop(i)
                falling_elements_positions.pop(i)
                break
        if element == "cross":
            
            if b_2_left <= element_x <= b_2_right and b_2_left <= element_x + 15 <= b_2_right and element_y <= b_2_top :
                if car_2_y >= 150: #Finishing line :600
                    car_2_y -= 50
                     
                    print("Car collided with cross! Speed decreased.")
                    
                falling_elements.pop(i)
                falling_elements_positions.pop(i)
                break
    
    if current_time - start_time >=30:   
        draw_finish_line()
    if finish == True:
        if b_1_top >= f_start_y:
            print(f'Car 1 wins. Final score : {score}')
                   
            glutLeaveMainLoop()
        elif b_2_top >= f_start_y:
            print('Car 2 wins')
            
            glutLeaveMainLoop()
def default_all():
    global f_start_y,start_time, score, car_1_x, car_1_y, car_2_x, car_2_y, falling_elements, falling_elements_positions,finish,batch_element_count,s_height
    car_1_x = 250
    car_1_y = 50
    car_2_x = 500
    car_2_y = 50
    falling_elements = []
    falling_elements_positions = []
    finish = False
    start_time = time.time()
    f_start_y= s_height-20
    batch_element_count = 0 
      
def draw_falling_elements():
    global falling_elements, falling_elements_positions,finish
    for i, element in enumerate(falling_elements):
        x, y = falling_elements_positions[i]
        if element == "triangle":
            draw_triangle(x, y)
        elif element == "circle":
            draw_circle(10, [x, y])  # Passing a default radius of 10
        elif element == "cross":
            draw_cross(x, y)

        
        falling_elements_positions[i][1] -= falling_speed

        
        if falling_elements_positions[i][1] <= 0:
            falling_elements.pop(i)
            falling_elements_positions.pop(i)
            break  
#Finishing Line
finish = False
f_start_x=100
f_start_y=s_height-20
def draw_finish_line():
    global s_height, f_start_x, f_start_y, finish
    finish = True
    drawLine(f_start_x, f_start_y, f_start_x + 600, f_start_y, (1, 1, 1))  # Bottom line
    drawLine(f_start_x, f_start_y + 20, f_start_x + 600, f_start_y + 20, (1, 1, 1))  # Top line
    for x in range(f_start_x, f_start_x + 580, 6):  #Adjust spacing
        drawLine(x, f_start_y + 20, x + 20, f_start_y, (1, 1, 1))
        drawLine(x, f_start_y, x + 20, f_start_y + 20, (1, 1, 1))
    
def animate_finish():
    global f_start_x, f_start_y
    f_start_y -=2

#Divider---------------x---------------------
def drawPnt(x, y, size=15):
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(int(x),int(y))
    glEnd()

def drawLin(x1, y1, x2, y2, color):
    glColor3f(*color)
    zone = int_FindZone(x1, y1, x2, y2)
    if zone != 0:
        x1, y1 = convertToZero(x1,y1,zone)
        x2, y2 = convertToZero(x2, y2, zone)
    dx = x2 - x1
    dy = y2 - y1
    d = 2*dy - dx
    incE = 2*dy
    incNE = 2*(dy-dx)
    y = y1
    for x in range(int(x1), int(x2)):
        if zone != 0:
            original_x, original_y = convertToOriginal(x, y, zone)
            drawPnt(original_x, original_y)
        else:
            drawPnt(x, y)
        if d>0:
            d = d + incNE
            y += 1
        else:
            d = d + incE
divider_y = 1  # Starting position of the divider
divider_speed = 3  # Speed of the divider movement
# Dash parameters
dash_length = 30  # Length of each dash
gap_length = 50  # Gap between dashes
line_color = (1, 1, 1)  # White color
def draw_divider():
    """Draw a dashed vertical divider using the Midpoint Line Algorithm."""
    global divider_y
    y = divider_y
    
    divider_x = s_width // 2
    
    total_dash_height = dash_length + gap_length
    
    while y < s_height + total_dash_height:
        drawLin(divider_x, y, divider_x, y + dash_length, line_color)
        y += total_dash_height

    
    y = divider_y - total_dash_height
    while y > -dash_length:
        drawLin(divider_x, y, divider_x, y + dash_length, line_color)
        y -= total_dash_height

def animate_divider():
    
    global divider_y
    divider_y -= divider_speed
    
    if divider_y <= -dash_length - gap_length:
        divider_y += dash_length + gap_length
def display():
    global start_time, timeout
    glClear(GL_COLOR_BUFFER_BIT)
    # Update and draw falling elements
    update_falling_elements()
    draw_falling_elements()
    draw_divider()
    draw_()
    draw_car_1()
    draw_car_2()
    draw_pause_button()
    draw_exit_button()
    draw_restart_button()
    glutSwapBuffers()

def animation():
    global finish, flag_anim
    if not flag_pause and not flag_gameOver:
        if finish:
            animate_finish()
        animate_divider()
        glutPostRedisplay()


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(s_width, s_height)
glutCreateWindow(b"Shoot The Circles!")
glOrtho(0, s_width, 0, s_height, -1, 1)
glClearColor(0, 0, 0, 1)
glutDisplayFunc(display)
glutIdleFunc(animation)
glutMouseFunc(mouse_click)
glutKeyboardFunc(keyboardListener)
# glutSpecialFunc(special_keys)
glutMainLoop()
