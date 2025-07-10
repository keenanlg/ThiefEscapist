import pygame
import random

class NPC(pygame.sprite.Sprite):
    def __init__(self, position, patrol_start, patrol_end, speed, name, direction):
        super().__init__()
        
        # Load NPC animation sheet
        base_path = "../assets/Tilesets & Spritesheets/NPCs/Pre-made NPCs/"
        sprite_path = f"{base_path}{name}.png"
        self.animation_sheet = pygame.image.load(sprite_path)
        
        # Define area of a single sprite
        self.animation_sheet.set_clip(pygame.Rect(0, 0, 11, 15))
        self.image = self.animation_sheet.subsurface(self.animation_sheet.get_clip())
        self.rect = self.image.get_rect()
        
        # Position image on the screen
        self.rect.topleft = position
        
        # Patrol variables
        self.patrol_start = patrol_start
        self.patrol_end = patrol_end
        self.speed = speed # Speed = 2, approx 30 seconds from side to side
        self.direction = direction  # 1 for right, -1 for left
        
        # Animation variables
        self.frame = 0
        self.last_update_time = pygame.time.get_ticks()
        self.frame_delay = 150
        self.rectWidth = 11
        self.rectHeight = 15
        
        # Animation states
        self.walk_states = { 
            0: (11, 9, self.rectWidth, self.rectHeight), 
            1: (43, 9, self.rectWidth, self.rectHeight), 
            2: (75, 9, self.rectWidth, self.rectHeight), 
            3: (107, 9, self.rectWidth, self.rectHeight) 
        }

        # All states of player idling
        self.idle_states = { 
            0: (11, 41, self.rectWidth, self.rectHeight),
            1: (43, 41, self.rectWidth, self.rectHeight),
            2: (75, 41, self.rectWidth, self.rectHeight) 
        }

        self.sight_length = 224 # 3.5 tile distance
        self.alerted = False
        self.visible = True
        self.node_index = 0
        self.path_node_coords = None
        self.idle_timer = 0
        self.idle_duration = 5000
        self.return_to_start = False
        self.is_idle = False
        self.target_x = 0
        self.target_y = 0
        self.patrol = True
        self.stairs = False
        self.elevator = False
        self.player_rect = None

        self.indicator = pygame.image.load("../assets/UI/Icons/Siren.png")
        self.indicator_rect = self.indicator.get_rect()
        self.indicate = False

    def get_line_of_sight(self):
        if self.direction == 1:  # Facing right
            return pygame.Rect(self.rect.right, self.rect.top, self.sight_length, self.rect.height)
        else:  # Facing left
            return pygame.Rect(self.rect.left - self.sight_length, self.rect.top, self.sight_length, self.rect.height)

    def get_frame(self, frame_set):
        # Looping through the sprite sequence
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]

    def animation_clip(self, clipped_rect):
        if isinstance(clipped_rect, dict):
            self.animation_sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.animation_sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect
    
    def set_path_node_coords(self, path_node_coords):
        self.path_node_coords = path_node_coords
        self.patrol = False
    
    def move_in_path(self, path_node_coords):
        self.speed = 5
        if not self.get_line_of_sight().colliderect(self.player_rect) and self.return_to_start:
            self.speed = 2
            # self.alerted = False
        if self.get_line_of_sight().colliderect(self.player_rect) and not self.stairs and not self.elevator and self.alerted:
            self.rect.x += self.speed * self.direction
            # self.alerted = True
        else:
            if self.node_index < len(path_node_coords) - 1:
                self.target_x, self.target_y = path_node_coords[self.node_index + 1]
                # Determine the movement direction
                if abs(self.target_x - self.rect.x) > self.speed or abs(self.target_y - self.rect.y) > self.speed:
                    # Diagonal movement
                    if abs(self.target_x - self.rect.x) > self.speed and abs(self.target_y - self.rect.y) > self.speed:
                        self.rect.x += self.speed if self.target_x > self.rect.x else -self.speed
                        self.rect.y += self.speed if self.target_y > self.rect.y else -self.speed
                        self.direction = 1 if self.target_x > self.rect.x else -1
                        self.visible = True
                        self.indicate = False
                        self.stairs = True
                        self.elevator = False
                    # Horizontal movement
                    elif abs(self.target_x - self.rect.x) > self.speed:
                        self.rect.x += self.speed if self.target_x > self.rect.x else -self.speed
                        self.direction = 1 if self.target_x > self.rect.x else -1
                        self.visible = True
                        self.indicate = False
                        self.stairs = False
                        self.elevator = False
                    # Vertical movement
                    elif abs(self.target_y - self.rect.y) > self.speed:
                        self.rect.y += 3 if self.target_y > self.rect.y else -3
                        self.visible = False
                        self.indicate = True
                        self.elevator = True
                        self.stairs = False
                        self.indicator_rect.topleft = (self.rect.x + 36, self.target_y - 31)
                else:
                    # Node reached
                    self.node_index += 1
                    
            else:
                if abs(self.rect.x - self.target_x) <= 5 and abs(self.rect.y - self.target_y) <= 5 and not self.return_to_start:
                    self.is_idle = True
                else:
                    # Once back at start position, reset path and idle again
                    self.return_to_start = False
                    self.path_node_coords.reverse()  # Restore the path nodes
                    self.idle_timer = pygame.time.get_ticks()  # Restart idle timer
                    self.visible = True
                    self.node_index = 0
                    self.patrol = True
                    self.is_idle = False
    
    def update_npc(self, player, scale):
        self.player_rect = player.rect
        if self.patrol:
            # Patrol logic
            self.rect.x += self.speed * self.direction

            # Reverse direction when reaching patrol bounds
            if self.rect.x <= self.patrol_start or self.rect.x >= self.patrol_end:
                self.direction *= -1
        elif not self.return_to_start:
            self.move_in_path(self.path_node_coords)
        
        if self.is_idle:
            if self.idle_timer == 0:  # Start the idle timer
                self.idle_timer = pygame.time.get_ticks()

            # Check if 5 seconds have passed
            elif pygame.time.get_ticks() - self.idle_timer >= 5000:
                self.idle_timer = 0   # Reset the timer for future use
                self.return_to_start = True
                self.is_idle = False  # Exit idle state
                self.node_index = 0  # Reset the node index
                self.path_node_coords.reverse()
            
        if self.return_to_start:
            self.move_in_path(self.path_node_coords)
            
        # Update animation frame
        curr_time = pygame.time.get_ticks()
        if curr_time - self.last_update_time >= self.frame_delay:
            self.last_update_time = curr_time
            if self.is_idle and self.direction == 1:
                self.animation_clip(self.idle_states)
                self.image = self.animation_sheet.subsurface(self.animation_sheet.get_clip())
            elif self.is_idle and self.direction == -1:
                self.animation_clip(self.idle_states)
                self.image = pygame.transform.flip(self.animation_sheet.subsurface(self.animation_sheet.get_clip()), True, False)
            elif self.direction == 1:  # Moving right
                self.animation_clip(self.walk_states)
                self.image = self.animation_sheet.subsurface(self.animation_sheet.get_clip())
            elif self.direction == -1:  # Moving left
                self.animation_clip(self.walk_states)
                self.image = pygame.transform.flip(self.animation_sheet.subsurface(self.animation_sheet.get_clip()), True, False)

        # Line of sight detection
        if self.get_line_of_sight().colliderect(player.rect):
            if player.visible:
                self.alerted = True
                self.speed = 4
            elif self.alerted:  # Player is hiding but was seen before
                self.speed = 4
        else:
            self.speed = 2
            self.alerted = False

        # Scale the NPC's image to match the map scale
        self.image = pygame.transform.scale(self.image, (self.rectWidth * scale, self.rectHeight * scale))
        self.indicator = pygame.transform.scale(self.indicator, (self.rectWidth, self.rectHeight))

    def draw(self, surface, camera_x, camera_y):
        # Draw NPC on the screen with camera offset if the NPC is visible
        if self.visible:
            surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        if self.indicate:
            surface.blit(self.indicator, (self.indicator_rect.x - camera_x, self.indicator_rect.y - camera_y))

class ShopNPC(pygame.sprite.Sprite):
    def __init__(self, position, name, scale):
        super().__init__()
        
        # Load NPC animation sheet
        base_path = "../assets/Tilesets & Spritesheets/NPCs/Pre-made NPCs/"
        sprite_path = f"{base_path}{name}.png"
        self.animation_sheet = pygame.image.load(sprite_path)
        
        # Define area of a single sprite
        self.animation_sheet.set_clip(pygame.Rect(0, 0, 11, 15))
        self.image = self.animation_sheet.subsurface(self.animation_sheet.get_clip())
        self.rect = self.image.get_rect()
        
        # Position the NPC on the screen
        self.rect.topleft = position
        
        # Animation variables
        self.frame = 0
        self.last_update_time = pygame.time.get_ticks()
        self.frame_delay = 200
        self.rectWidth = 11
        self.rectHeight = 15
        
        # Idle animation states
        self.idle_states = { 
            0: (11, 41, self.rectWidth, self.rectHeight),
            1: (43, 41, self.rectWidth, self.rectHeight),
            2: (75, 41, self.rectWidth, self.rectHeight) 
        }

        # Scale the NPC's image to match the map scale
        self.scale = scale

    def get_frame(self, frame_set):
        # Looping through the sprite sequence
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]

    def animation_clip(self, clipped_rect):
        if isinstance(clipped_rect, dict):
            self.animation_sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.animation_sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect

    def update(self):
        # Update animation frame
        curr_time = pygame.time.get_ticks()
        if curr_time - self.last_update_time >= self.frame_delay:
            self.last_update_time = curr_time
            self.animation_clip(self.idle_states)
            self.image = self.animation_sheet.subsurface(self.animation_sheet.get_clip())
        
        # Scale the NPC's image to match the map scale
        self.image = pygame.transform.scale(self.image, (self.rectWidth * self.scale, self.rectHeight * self.scale))

    def draw(self, surface, camera_x, camera_y):
        # Draw ShopNPC on the screen with camera offset
        flipped_image = pygame.transform.flip(self.image, True, False)
        surface.blit(flipped_image, (self.rect.x - camera_x, self.rect.y - camera_y))