import pygame
from globals import *

class VFX(pygame.sprite.Sprite):
    def __init__(self, position, type, size, columns, total, obbox):
        super().__init__()
        base_path = "../assets/Tilesets & Spritesheets/SpriteSheets/"
        sprite_path = f"{base_path}{type}.png"
        self.animation = pygame.image.load(sprite_path)
        self.animation.set_clip(pygame.Rect(0, 0, size, size))
        self.image = self.animation.subsurface(self.animation.get_clip())
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.id = obbox

        # Animation variables
        self.frame = 0
        self.last_update_time = pygame.time.get_ticks()
        self.frame_delay = 150
        self.rectWidth = size
        self.rectHeight = size

        self.states = {}

        for i in range(total):
            row = i // columns
            col = i % columns
            x = col * size
            y = row * size
            self.states[i] = (x, y, size, size)

    def get_frame(self, frame_set):
        # Looping through the sprite sequence
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]

    def animation_clip(self, clipped_rect):
        if isinstance(clipped_rect, dict):
            self.animation.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.animation.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect
    
    def update(self):
        # Update animation frame
        curr_time = pygame.time.get_ticks()
        if curr_time - self.last_update_time >= self.frame_delay:
            self.last_update_time = curr_time
            self.animation_clip(self.states)
            self.image = self.animation.subsurface(self.animation.get_clip())

        # if (type == "sparkle"):
        #     self.image = pygame.transform.scale(self.image, (self.rectWidth * 2, self.rectHeight * 2))

    def draw(self, screen, camera_x, camera_y):
        # Draw VFX only if it hasn't been looted
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
