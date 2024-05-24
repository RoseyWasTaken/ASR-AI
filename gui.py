import pygame
import os
import threading

# Activate the pygame library
pygame.init()
X = 600
Y = 600

imagePath = "images"

# Create the display surface object of specific dimension (X, Y)
window = pygame.display.set_mode((X, Y))

clock = pygame.time.Clock()

# Set the pygame window name
pygame.display.set_caption('AI Assistant')

# Create a surface object, image is drawn on it
sprites = []

for i in os.listdir(imagePath):
    currentDir = []

    for j in os.listdir(os.path.join(imagePath, i)):
        image = pygame.image.load(os.path.join(imagePath, i, j))
        image = pygame.transform.scale(image, (X, Y))
        currentDir.append(image)

    sprites.append(currentDir)

change_event = threading.Event()
shared_data = {"face": 0,
               "text": ""}

def displayFace():
    face = shared_data["face"]
    # sleeping face = 0
    # speaking face = 1
    # thinking face = 2

    value = 0

    # This loop will run until it is explicitly stopped from the main program
    while True:
        if change_event.is_set():
            face = shared_data["face"]
            change_event.clear()
                    
        clock.tick(2)

        if value >= len(sprites[face]):
            value = 0

        displayImage = sprites[face][value]

        window.blit(displayImage, (0, 0))
        if shared_data["face"] == 1:
            text = shared_data["text"]
            font_size = 36
            font_color = (0, 0, 0)
            line_spacing = 1.2  # Adjust this value to set the spacing between lines
            pygame.font.init()
            font = pygame.font.Font(None, font_size)

            # Split the text into lines based on a maximum line width
            max_line_width = X - 20  # Adjust this value as needed
            lines = []
            current_line = ""
            for word in text.split():
                test_line = current_line + word + " "
                test_width, _ = font.size(test_line)
                if test_width <= max_line_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + " "
            lines.append(current_line)

            # Calculate the total text height
            total_height = len(lines) * int(font_size * line_spacing)

            # Position the text on the window
            text_y = ((Y - total_height) // 2 ) + 200
            for line in lines:
                text_surface = font.render(line, True, font_color)
                text_x = (X - text_surface.get_width()) // 2
                window.blit(text_surface, (text_x, text_y))
                text_y += int(font_size * line_spacing)

        pygame.display.update()

        value += 1

        # Check for any pygame events (necessary to allow window to close)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
