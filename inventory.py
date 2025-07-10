import pygame

class Inventory:
    def __init__(self):
        self.playerItems = []
        self.warehouseItems = []
        self.playerCapacity = 21

    def add_item(self, item, image_path, value):
        """
        Add an item and its image to the inventory.
        Checks to see if player has inventory space:
            \nyes - add item
            \nno - state inventory full
        """
        
        if len(self.playerItems) < self.playerCapacity:
            self.playerItems.append({"name": item, "image": pygame.image.load(image_path) if image_path else None,
                                     "value": value})
        else:
            print("Inventory full! Purchase upgrade to increase capacity.")
            
    def return_items(self, items):
        if items == "player":
            return self.playerItems
        else:
            return self.warehouseItems
        
    def increase_capacity(self, amount):
        self.playerCapacity += amount
        print(f"Inventory capacity increased to {self.playerCapacity}!")

    def display(self, screen, items):
        """
        Displays the inventory as a grid.
        """
        
        font = pygame.font.Font(None, 22)
        grid_cols = 7  # Number of columns in the inventory grid
        cell_size = 80  # Size of each grid cell
        padding = 10  # Padding between cells
        x_start, y_start = 50, 50  # Starting position for inventory grid
        x, y = x_start, y_start

        if items == "player":
            for index, item in enumerate(self.playerItems):
                # Calculate cell center
                cell_center_x = x + cell_size // 2

                # Draw item image
                if item["image"]:
                    image_size = 50
                    image_x = cell_center_x - image_size // 2
                    image_y = y + 10  # Slightly below the top of the cell
                    screen.blit(pygame.transform.scale(item["image"], (image_size, image_size)), (image_x, image_y))

                # Draw item name (centered below the image)
                text = font.render(item["name"], True, (255, 255, 255))
                text_rect = text.get_rect(center=(cell_center_x, y + cell_size - 5))  # Adjust y for spacing
                screen.blit(text, text_rect)

                # Move to next column or row
                x += cell_size + padding
                if (index + 1) % grid_cols == 0:
                    x = x_start
                    y += cell_size + padding
        else:
            for index, item in enumerate(self.warehouseItems):
                # Calculate cell center
                cell_center_x = x + cell_size // 2

                # Draw item image
                if item["image"]:
                    image_size = 50
                    image_x = cell_center_x - image_size // 2
                    image_y = y + 10  # Slightly below the top of the cell
                    screen.blit(pygame.transform.scale(item["image"], (image_size, image_size)), (image_x, image_y))

                # Draw item name (centered below the image)
                text = font.render(item["name"], True, (255, 255, 255))
                text_rect = text.get_rect(center=(cell_center_x, y + cell_size - 5))  # Adjust y for spacing
                screen.blit(text, text_rect)

                # Move to next column or row
                x += cell_size + padding
                if (index + 1) % grid_cols == 0:
                    x = x_start
                    y += cell_size + padding