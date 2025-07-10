import pygame

class StairHandler:
    def __init__(self, box_x, box_y, box_width, box_height, xdirection, ydirection, destination_y):
        self.stair_box = pygame.Rect(box_x, box_y, box_width, box_height)
        self.stair_box_triggered = False
        self.stair_start_position = None
        self.xdirection = xdirection
        self.ydirection = ydirection
        self.destination_y = destination_y

    def check_stair_trigger(self, player, keys):
        # Check collision with the box and Q key press
        if player.rect.colliderect(self.stair_box) and keys[pygame.K_q]:
            self.stair_box_triggered = True
            self.stair_start_position = player.rect.topleft  # Save the initial player position
            player.traversing = True

    def handle_stair_movement(self, player, keys):
        if self.stair_box_triggered:
            # Move right (upstairs to the right)
            if self.xdirection == 1 and keys[pygame.K_d]:
                player.on_Rstairs = True
                # Allow movement only if the player hasn't reached the destination
                if (self.ydirection == -1 and player.rect.y > self.destination_y) or (self.ydirection == 1 and player.rect.y < self.destination_y):
                    player.rect.x += 1  # Move right
                    player.rect.y += (6 * self.ydirection)  # Move vertically

            # Move left (upstairs to the left)
            if self.xdirection == -1 and keys[pygame.K_a]:
                player.on_Lstairs = True
                # Allow movement only if the player hasn't reached the destination
                if (self.ydirection == -1 and player.rect.y > self.destination_y) or (self.ydirection == 1 and player.rect.y < self.destination_y):
                    player.rect.x -= 1  # Move left
                    player.rect.y += (6 * self.ydirection)  # Move vertically

            # Exit stair mode once the player reaches the destination
            if (self.ydirection == -1 and player.rect.y <= self.destination_y) or (self.ydirection == 1 and player.rect.y >= self.destination_y):
                self.stair_box_triggered = False
                player.on_Rstairs = False
                player.on_Lstairs = False
                player.traversing = False




    def draw(self, screen, camera_x, camera_y):
        # Draw the rectangle adjusted for the camera position
        pygame.draw.rect(screen, (200, 0, 0), 
                        (self.stair_box.x - camera_x, self.stair_box.y - camera_y, self.stair_box.width, self.stair_box.height))


class ElevatorHandler:
    def __init__(self, box_x, box_y, box_width, box_height, destination_y, speed):
        self.elevator_box = pygame.Rect(box_x, box_y, box_width, box_height)
        self.elevator_box_triggered = False
        self.elevator_start_position = None
        self.destination_y = destination_y  # Y-coordinate for the bottom of the elevator
        self.speed = speed  # Speed of elevator movement
        if box_y < destination_y:
            self.direction = 1
        else:
            self.direction = -1

    def check_elevator_trigger(self, player, keys):
        # Check collision with the elevator box and C key press
        if player.rect.colliderect(self.elevator_box) and keys[pygame.K_c]:
            self.elevator_box_triggered = True
            self.elevator_start_position = player.rect.topleft  # Save the initial player position
            player.visible = False  # Make the player invisible
            player.traversing = True
            player.traversingElevator = True

    def handle_elevator_movement(self, player, camera_y):
        if self.elevator_box_triggered:
            # Calculate the remaining distance to the destination
            remaining_distance = self.destination_y - player.rect.y

            # Move the player in the correct direction
            if abs(remaining_distance) <= self.speed:
                # If the player is close enough to the destination, snap to the destination
                player.rect.y = self.destination_y
                camera_y += remaining_distance  # Adjust the camera by the remaining distance
                self.elevator_box_triggered = False
                player.traversingElevator = False
                player.visible = True  # Make the player visible again
                player.traversing = False
            else:
                # Move the player towards the destination
                player.rect.y += self.speed * self.direction
                camera_y += self.speed * self.direction  # Move the camera as well
                player.visible = False

        return camera_y

