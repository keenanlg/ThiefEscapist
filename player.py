#################################################
# Names:        Caleb Murphy & Keenan Grant     #
# Date:         10/20/2024                      #
# Class:        CPSC 4160                       #
# Assignment:   Final                           #
#################################################

import pygame
from inventory import Inventory

class Character(pygame.sprite.Sprite):
    def __init__(self, position):
    
        # Load image
        self.animation_sheet = pygame.image.load('../assets/Tilesets & Spritesheets/NPCs/Pre-made NPCs/Male/NPC 1MD.png')
        self.grab_sheet = pygame.image.load('../assets/Tilesets & Spritesheets/NPCs/Pre-made NPCs/Male/NPC_1MD_Grab.png')
        
        # Defines area of a single sprite of an image
        self.animation_sheet.set_clip(pygame.Rect(0, 0, 11, 15))
        self.grab_sheet.set_clip(pygame.Rect(0, 0, 11, 15))
        
        # Loads spritesheet images
        self.image = self.animation_sheet.subsurface(self.animation_sheet.get_clip())
        self.rect = self.image.get_rect()
        
        self.image2 = self.grab_sheet.subsurface(self.grab_sheet.get_clip())
        self.rect2 = self.image2.get_rect()
        
        # Position image in the screen surface
        self.rect.topleft = position
        self.rect2.topleft = position
        
        # Variables for looping the frame sequence
        self.frame = 0
        
        # Obtain last updated time for comparison in delays
        self.last_update_time = pygame.time.get_ticks()
        self.idle_last_update_time = pygame.time.get_ticks()
        
        # Frame delay in MS 
        self.frame_delay = 150
        self.idle_frame_delay = 200
        self.grab_delay = 100
        
        # Width & Height of each frame
        self.rectWidth = 11
        self.rectHeight = 15          
        
        # State Variables
        self.wentLeft = False
        self.wentRight = False
        self.isGrabbing = False

        self.speed = 5 #Speed = 5 approx 12.5 seconds from side to side
        
        # Variable for storing money
        self.currency = 150

        self.traversing = False
        
        # Variable for storing score
        self.score = 0
        
        # Inventory
        #! Find a way to add inventory upgrades
        self.inventory = Inventory()
        
        # All states of player moving
        self.walk_states = { 0: (11, 9, self.rectWidth,  self.rectHeight), 
                             1: (43, 9, self.rectWidth,  self.rectHeight), 
                             2: (75, 9, self.rectWidth,  self.rectHeight),
                             3: (107, 9, self.rectWidth,  self.rectHeight)  }
        
        # All states of player idling
        self.idle_states = { 0: (11, 41, self.rectWidth, self.rectHeight),
                             1: (43, 41, self.rectWidth, self.rectHeight),
                             2: (75, 41, self.rectWidth, self.rectHeight) }
        
        # All states of player grabbing something
        self.grab_states = { 0: (11, 10, self.rectWidth,  self.rectHeight),
                             1: (43, 10, self.rectWidth,  self.rectHeight), 
                             2: (75, 10, self.rectWidth,  self.rectHeight), 
                             3: (107, 10, self.rectWidth,  self.rectHeight)  }
        
        # Stair variables
        self.on_Rstairs = False
        self.on_Lstairs = False

        # Elevator variable
        self.visible = True

        self.traversingElevator = False

    def get_frame(self, frame_set):
        # Looping the sprite sequences.
        self.frame += 1
        
        # If loop index is higher that the size of the frame 
        # return to the first frame 
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
            self.isGrabbing = False
        return frame_set[self.frame]

    def animation_clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.animation_sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.animation_sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect
    
    def grab_clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.grab_sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.grab_sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect
    
    def increase_player_speed(self, amount):
        self.speed += amount
        print(f"Player's movement speed has increased by {amount}!")        

    def update(self, direction, scale):
        curr_time = pygame.time.get_ticks()
        
        # Walk Animations - update frame only if delay time has passed
        if curr_time - self.last_update_time >= self.frame_delay:
            self.last_update_time = curr_time
            if direction == 'left':
                self.animation_clip(self.walk_states)
                # Flip image to point other direction
                self.image = pygame.transform.flip(self.animation_sheet.subsurface(self.animation_sheet.get_clip()), True, False)  
                # Set state variables
                self.wentLeft = True
                self.wentRight = False
            if direction == 'right':
                self.animation_clip(self.walk_states)
                self.image = self.animation_sheet.subsurface(self.animation_sheet.get_clip())
                # Set state variables
                self.wentLeft = False
                self.wentRight = True

        # Idle Animations - update frame only if delay time has passed
        if curr_time - self.idle_last_update_time >= self.idle_frame_delay:
            self.idle_last_update_time = curr_time
            if direction == 'idle_left':
                self.animation_clip(self.idle_states)
                # Flip image to point other direction
                self.image = pygame.transform.flip(self.animation_sheet.subsurface(self.animation_sheet.get_clip()), True, False)
            if direction == 'idle_right':
                self.animation_clip(self.idle_states)
                self.image = self.animation_sheet.subsurface(self.animation_sheet.get_clip())
        
        # Grab Animations - update frame only if delay time has passed
        if self.isGrabbing:
            if curr_time - self.grab_last_update_time >= self.grab_delay:
                self.grab_last_update_time = curr_time
                if self.wentRight:
                    self.grab_clip(self.grab_states)
                    self.image = self.grab_sheet.subsurface(self.grab_sheet.get_clip())
                elif self.wentLeft:
                    self.grab_clip(self.grab_states)
                    # Flip image to point other direction
                    self.image = pygame.transform.flip(self.grab_sheet.subsurface(self.grab_sheet.get_clip()), True, False)
        
        # Scale the character's image to match the map scale
        self.image = pygame.transform.scale(self.image, (self.rectWidth * scale, self.rectHeight * scale))

    # Start grab animation
    def start_grab(self):
        self.isGrabbing = True
        self.frame = 0
        self.grab_last_update_time = pygame.time.get_ticks()

    def handle_movement(self, key, SCALE):
        if not self.traversingElevator:
            if key[pygame.K_a] and self.on_Rstairs == False and self.rect.x > 512:
                self.rect.x -= self.speed
                self.update('left', SCALE)
            elif key[pygame.K_d] and self.on_Lstairs == False and self.rect.x < 1744:
                self.rect.x += self.speed
                self.update('right', SCALE)
            elif key[pygame.K_w]:
                self.rect.y -= self.speed
                self.update('up', SCALE)
            elif key[pygame.K_s]:
                self.rect.y += self.speed
                self.update('down', SCALE)
            elif key[pygame.K_e]:
                self.start_grab()
            else:
                # Set idle state
                if self.wentLeft:
                    self.update('idle_left', SCALE)
                else:
                    self.update('idle_right', SCALE)

    def draw(self, screen, camera_x, camera_y):
        # Only draw the player if they are visible
        if self.visible and not self.traversingElevator:
            screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
            pygame.display.update()