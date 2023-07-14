import serial
import math
import matplotlib.pyplot as plt
import time
import pygame

# Initialize Pygame
pygame.init()

# Set up the canvas dimensions
width, height = 800, 600
canvas = pygame.display.set_mode((width, height))

# Set the color for the points
point_color = (255, 0, 0)  # Red

# Close any existing serial port connection on COM13 if there is one
port = 'COM13'  # Replace with the appropriate port name
baud_rate = 115200  # Set the baud rate to match your device
try:
    existing_serial = serial.Serial(port)
    if existing_serial.is_open:
        existing_serial.close()
except serial.SerialException:
    pass

limitrange = 40
# Set up serial communication
s = serial.Serial(port, baud_rate)
refresh_interval = 2  # Set the refresh interval in seconds
prev_refresh_time = 0
i = 0
points = []
res = 1
image_filename = "frame.png"
running = True
obstical = []
mindistance = 40
try:
    while running:
        # Read a line of data from the serial port
        data = s.readline().decode().strip()

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
        if angle > 360 or angle in [122,123,124,125]:
            continue


        # Convert polar coordinates to Cartesian coordinates
        x = distance * math.cos(math.radians(angle))*res
        y = distance * math.sin(math.radians(angle))*res
        
        points.append((x+(width/2),y+(height/2)))
        if distance < mindistance:
            obstical.append((x+(width/2),y+(height/2)))

        # # Check if it's time to refresh the plot
        elapsed_time = time.time() - prev_refresh_time
        if elapsed_time >= refresh_interval:
            # Refresh the plot
            pygame.image.save(canvas, image_filename)
            canvas.fill((0, 0, 0))
            points = []
            obstical = []
            # Store the current time as the new previous refresh time
            prev_refresh_time = time.time()
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    res = res + 1
                elif event.key == pygame.K_DOWN:
                    res = res - 1

        # Clear the canvas
        canvas.fill((0, 0, 0))
        pygame.draw.circle(canvas, (255,0, 255), (width/2,height/2), 15*res,1)
        if len(obstical)>10:
            pygame.draw.circle(canvas, (255,0, 0), (width/2,height/2), mindistance*res,1)
        else:
            pygame.draw.circle(canvas, (0,255, 0), (width/2,height/2), mindistance*res,1)
        # Draw the points on the canvas
        for point in points:
            pygame.draw.circle(canvas, point_color, point, 1)

        # Update the display
        pygame.display.flip()

    # Quit the game
    pygame.quit()
except serial.SerialException as e:
    print(str(e))
finally:
    s.close()
