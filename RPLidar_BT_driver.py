import serial
import math
import time
import pygame
from scipy.spatial import KDTree
import numpy as np
from scipy.spatial import KDTree
import serial
# Define colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
# Initialize Pygame
pygame.init()

bluetooth_port = "COM17"  # Replace with the appropriate port for your Bluetooth device
baud_rate = 9600

# Open the serial port for communication
ser = serial.Serial(bluetooth_port, baud_rate)

# Set up the canvas dimensions
width, height = 800, 600
canvas = pygame.display.set_mode((width, height))
# Set the color for the points
point_color = (255, 0, 0)  # Red
# Close any existing serial port connection on COM13 if there is one
# port = 'COM17'  # Replace with the appropriate port name
# baud_rate = 115200  # Set the baud rate to match your device
# try:
#     existing_serial = serial.Serial(port)
#     if existing_serial.is_open:
#         existing_serial.close()
# except serial.SerialException:
#     pass

limitrange = 40
# Set up serial communication
# s = serial.Serial(port, baud_rate)
refresh_interval = 2  # Set the refresh interval in seconds
prev_refresh_time = 0
count = 0
i = 3
points = []
res = 1
image_filename = "frame.png"
running = True
obstical = []
mindistance = 40

# Set a distance threshold for connecting points
threshold = 5
i = 0  # Connection index
linked_points = set()  # Set to store connected points
try:
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                canvas.fill(BLACK)
                points = []
                obstical = []
                linked_points = set()
                i = 0
                if event.key == pygame.K_UP:
                    res = res + 1                 
                elif event.key == pygame.K_DOWN:
                    res = res - 1
        # Read a line of data from the serial port
        # data = s.readline().decode().strip()
        
        data = ser.readline().decode().rstrip()

        # Split the data into distance and angle
        if data:
            parts = data.split(',')
        else:
            continue

        try:
            reset = float(parts[0])
        except ValueError:
            continue

        try:
            quality = float(parts[1])
        except ValueError:
            continue

        try:
            distance = float(parts[2])
        except ValueError:
            continue
        if distance > 150 or distance < 15:
            continue

        try:
            angle = round(float(parts[3]))
        except ValueError:
            continue 
        if angle > 360 or angle in range(123, 125):
            continue
        if quality != 15:
            continue

        count = count + reset

        # Convert polar coordinates to Cartesian coordinates
        x = int(distance * math.cos(math.radians(angle))*res)
        y = int(distance * math.sin(math.radians(angle))*res)
        
        if len(points) < 500 or count < 1:
            points.append((x+(width/2),y+(height/2)))
            print("build tree",len(points),count,i,data)
        else:
            print("i",i)
        if distance < mindistance:
            obstical.append((x+(width/2),y+(height/2)))


        # Clear the canvas
        if (i == len(points)):
            print("Done",i)
            canvas.fill(BLACK)
            points = []
            obstical = []
            linked_points = set()
            i = 0
            count = 0          
            

        # Find nearest neighbors and connect points
        if len(points) > 2:
            # Build a KDTree
            kdtree = KDTree(points)
            # Find nearest neighbors and connect points
            if i < len(points):
                point = points[i]
                neighbors = kdtree.query_ball_point(point, threshold)

                for index in neighbors:
                    if index != i:
                        neighbor = points[index]
                        pygame.draw.line(canvas, RED, point, neighbor, 1)
                        linked_points.add(point)
                        linked_points.add(neighbor)
                        pygame.draw.circle(canvas, RED, point, 1)
                        pygame.draw.line(canvas, RED, ((width/2),(height/2)), neighbor, 1)
                        pygame.draw.line(canvas, RED, point, ((width/2),(height/2)), 1)

                i += 1

        pygame.draw.circle(canvas, (0,0, 255), (width/2,height/2), 15*res)
        if len(obstical)>50:
            pygame.draw.circle(canvas, (255,0, 0), (width/2,height/2), mindistance*res,1)
        else:
            pygame.draw.circle(canvas, (0,255, 0), (width/2,height/2), mindistance*res,1)
            
        # Update the display
        pygame.display.flip()

    # Quit the game
    pygame.quit()
# except serial.SerialException as e:
#     print(str(e))
# finally:
#     s.close()
except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed.")