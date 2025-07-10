#################################################
# Names:        Caleb Murphy & Keenan Grant     #
# Date:         10/20/2024                      #
# Class:        CPSC 4160                       #
# Assignment:   Final                           #
#################################################

import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, scale):
        super().__init__(groups)
        TILE_SIZE = 16
        self.image = pygame.transform.scale(surface, (TILE_SIZE * scale, TILE_SIZE * scale))
        self.rect = self.image.get_rect(topleft = pos)
        
class ObjectTile(pygame.sprite.Sprite):
    def __init__(self, object, groups, scale):
        super().__init__(groups)
        #! Find out how to load text on Tiled
        
        # Extract object properties
        pos = (object.x * scale, object.y * scale)
        width = object.width * scale
        height = object.height * scale
        rotation = getattr(object, 'rotation', 0)  # Default to 0 if no rotation is specified
        
        # Load and scale the object's image
        original_image = pygame.transform.scale(object.image, (int(width), int(height)))
        
        # Apply rotation if necessary
        if rotation != 0:
            # print(f"{rotation}")
            self.image = pygame.transform.rotate(original_image, -rotation)  # Tiled's rotation is clockwise
        else:
            self.image = original_image
        
        # Adjust the position to account for the rotation
        self.rect = self.image.get_rect(center=(pos[0] + width / 2, pos[1] + height / 2))
        