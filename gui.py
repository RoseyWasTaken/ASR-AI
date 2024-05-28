import pygame
import os

imagePath = "images"

X = 600
Y = 600

sprites = {}

# sprites = {"sleeping": [pygame.image1, pygame.image2],
#           "thinking": [pygame.image3, pygame.image4], ... 
#           }

# sprites["thinking"] = "pygame.images"

def init_pygame():
    pygame.init()

    window = pygame.display.set_mode((X, Y))

    pygame.display.set_caption('AI Assistant')

    return window

def load_sprites():

    for i in os.listdir(imagePath):
        currentDir = []

        for j in os.listdir(os.path.join(imagePath, i)):
            image = pygame.image.load(os.path.join(imagePath, i, j))
            image = pygame.transform.scale(image, (X, Y))
            currentDir.append(image)

        sprites[i] = currentDir
    
    return sprites

window = init_pygame()
sprites = load_sprites()

def display_face(face, text=""):


        displayImage = sprites[face][0]

        window.blit(displayImage, (0, 0))

        if face == "speaking":
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

        # Check for any pygame events (necessary to allow window to close)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return