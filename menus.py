import pygame, sys, re
from globals import *

class Menu():
    def __init__(self):
        super().__init__()

    def start_menu(self, screen):
        """ 
        Function is used to populate and display the start menu.
        """
        
        # Load and scale bg image
        background_image = pygame.image.load("../assets/start_menu_bg_image.png")
        background_image = pygame.transform.scale(background_image, screen.get_size())
        
        # Create font and buttons
        font = pygame.font.Font(None, 36)    
        start_btn = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 80, 200, 50)
        options_btn = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 140, 200, 50)
        quit_btn = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 200, 200, 50)
        
        run = True
        while run:
            # Render bg image
            screen.blit(background_image, (0, 0))
            
            # Render button & text; centers text w/ rectangle
            pygame.draw.rect(screen, (44, 53, 130), start_btn)
            start_text = font.render("Start Game", True, (255, 255, 255))
            start_text_rect = start_text.get_rect(center=start_btn.center)
            screen.blit(start_text, start_text_rect)

            pygame.draw.rect(screen, (44, 53, 130), options_btn)
            options_text = font.render("Options", True, (255, 255, 255))
            options_text_rect = options_text.get_rect(center=options_btn.center)
            screen.blit(options_text, options_text_rect)
            
            pygame.draw.rect(screen, (44, 53, 130), quit_btn)
            quit_text = font.render("Quit", True, (255, 255, 255))
            quit_text_rect = quit_text.get_rect(center=quit_btn.center)
            screen.blit(quit_text, quit_text_rect)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if start_btn.collidepoint(event.pos):
                        return "start"
                    elif options_btn.collidepoint(event.pos):
                        return "options"
                    elif quit_btn.collidepoint(event.pos):
                        return "quit"
                        
            pygame.display.update()
            clock.tick(FPS)
            
    def options_menu(self, screen):
        """ 
        Function is used to populate and display the options menu.
        """
        # Load and scale bg image
        background_image = pygame.image.load("../assets/options_menu_bg_image.png")
        background_image = pygame.transform.scale(background_image, (screen.get_width() // 2, screen.get_height()))
        
        font = pygame.font.Font(None, 36)
        
        # Calculate positions for the buttons
        left_column_width = screen.get_width() // 2
        button_width = 200

        controls_btn = pygame.Rect(left_column_width // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 150, button_width, 50)
        back_btn = pygame.Rect(left_column_width // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 210, button_width, 50)
        
        run = True
        while run:
            # Fill left side w/ dark blue
            screen.fill((17, 21, 56)) 
            
            # Fill right side w/ bg image
            screen.blit(background_image, (screen.get_width() // 2, 0))
            
            # Render "Controls" button
            pygame.draw.rect(screen, (44, 53, 130), controls_btn)
            controls_text = font.render("Controls", True, (255, 255, 255))
            controls_text_rect = controls_text.get_rect(center=controls_btn.center)
            screen.blit(controls_text, controls_text_rect)
            
            # Render "Back" button
            pygame.draw.rect(screen, (44, 53, 130), back_btn)
            back_text = font.render("Back", True, (255, 255, 255))
            back_text_rect = back_text.get_rect(center=back_btn.center)
            screen.blit(back_text, back_text_rect)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_ESCAPE:
                        return "back"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if controls_btn.collidepoint(event.pos):
                        result = self.controls_menu(screen)  # Open controls menu
                        if result == "quit":
                            return "quit"
                    if back_btn.collidepoint(event.pos):
                        return "back"
            
            pygame.display.update()
            clock.tick(FPS)

    def controls_menu(self, screen):
        """
        Function is used to populate and display the controls menu.
        """
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 22)
        
        # Back button setup
        button_width = 200
        back_btn = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT + 50, button_width, 50)

        # Placeholder controls text
        controls_text = [
            "Hide: F",
            "Move Left: A",
            "Move Right: D",
            "Open/Close Inventory: I",
            "Interact/Open Menus/Loot: E",
            "Enter Stair Mode: Q",
            "Ride Elevator: C",
            "Pause: Esc"
        ]

        run = True
        while run:
            # Fill the background
            screen.fill((17, 21, 56)) 
            
            # Title
            title = font.render("Controls", True, (255, 255, 255))
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2 + 100, 50))
            screen.blit(title, title_rect)
            
            # Display placeholder controls
            y_offset = 120
            for control in controls_text:
                control_text = small_font.render(control, True, (255, 255, 255))
                control_rect = control_text.get_rect(center=(SCREEN_WIDTH // 2 + 100, y_offset))
                screen.blit(control_text, control_rect)
                y_offset += 20  # Spacing between lines
            
            # Render "Back" button
            pygame.draw.rect(screen, (44, 53, 130), back_btn)
            back_text = font.render("Back", True, (255, 255, 255))
            back_text_rect = back_text.get_rect(center=back_btn.center)
            screen.blit(back_text, back_text_rect)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_ESCAPE:
                        return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_btn.collidepoint(event.pos):
                        return "backToOptions" # Return to options menu
            
            pygame.display.update()
            clock.tick(FPS)
            
    def show_warehouse_menu(self, screen, warehouse):
        """ 
        Display the warehouse menu with scrolling, text wrapping, and scroll hint.
        """
        # Scrolling variables
        warehouse_scroll_offset = 0
        scroll_step = 2  # Number of rows to scroll per step
        grid_cols = 7  # Number of columns in the warehouse grid
        cell_size = 80  # Size of each grid cell
        padding = 10  # Padding between cells
        font = pygame.font.Font(None, 22)
        title_font = pygame.font.Font(None, 36)
        hint_font = pygame.font.Font(None, 18)  # Smaller font for hint text

        warehouse_menu_active = True
        while warehouse_menu_active:
            # Menu overlay setup
            overlay = pygame.Surface(screen.get_size())
            overlay.fill((44, 53, 130))
            
            inner_overlay = pygame.Rect(20, 20, SCREEN_WIDTH * 1.5 - 40, SCREEN_HEIGHT * 1.5 - 40)  # 20px margin
            inner_surface = pygame.Surface((inner_overlay.width, inner_overlay.height))
            inner_surface.fill((17, 21, 56))
            
            overlay.blit(inner_surface, (20, 20))  # 20px margin
            screen.blit(overlay, (0, 0))

            # Add a title for the warehouse inventory
            title = title_font.render("Warehouse Inventory", True, (255, 255, 255))
            screen.blit(title, (inner_overlay.x + 20, inner_overlay.y + 20))

            # Starting position for grid
            x_start, y_start = inner_overlay.x + 20, inner_overlay.y + 60
            x, y = x_start, y_start

            # Calculate visible range of items
            rows_per_screen = (inner_overlay.height - 100) // (cell_size + padding)  # Rows that fit on screen
            start_index = warehouse_scroll_offset * grid_cols
            end_index = start_index + rows_per_screen * grid_cols

            visible_items = warehouse.warehouseItems[start_index:end_index]

            # Display items in grid
            for index, item in enumerate(visible_items):
                cell_center_x = x + cell_size // 2

                if item["image"]:
                    # Draw item image
                    image_size = 50
                    image_x = cell_center_x - image_size // 2
                    image_y = y + 10  # Slightly below the top of the cell
                    screen.blit(pygame.transform.scale(item["image"], (image_size, image_size)), (image_x, image_y))

                # Wrap and draw item name
                text_lines = self.wrap_text(item["name"], font, cell_size - 10)  # Wrap text to fit within the cell width
                text_y = y + cell_size - 10  # Start drawing text below the image
                for line in text_lines:
                    text = font.render(line, True, (255, 255, 255))
                    text_rect = text.get_rect(center=(cell_center_x, text_y))
                    screen.blit(text, text_rect)
                    text_y += text.get_height()  # Move to the next line
                
                # Move to next column or row
                x += cell_size + padding
                if (index + 1) % grid_cols == 0:
                    x = x_start
                    y += cell_size + padding

            # Check if scrolling is available and display the hint
            max_scroll = max(len(warehouse.warehouseItems) // grid_cols - rows_per_screen + 1, 0)
            if max_scroll > 0:
                hint_text = "Scroll to view more of your Warehouse Inventory"
                hint = hint_font.render(hint_text, True, (255, 255, 255))
                hint_x = SCREEN_WIDTH // 2
                hint_y = SCREEN_HEIGHT + 40 + hint.get_height()  # Position at the bottom center of the screen
                screen.blit(hint, (hint_x, hint_y))

            pygame.display.update()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Exit menu
                        warehouse_menu_active = False
                    if event.key == pygame.K_e:  # Close warehouse menu
                        warehouse_menu_active = False
                if event.type == pygame.MOUSEWHEEL:
                    # Handle scrolling
                    if event.y > 0:  # Scroll up
                        warehouse_scroll_offset = max(warehouse_scroll_offset - scroll_step, 0)
                    elif event.y < 0:  # Scroll down
                        warehouse_scroll_offset = min(warehouse_scroll_offset + scroll_step, max_scroll)

    def wrap_text(self, text, font, max_width):
        """
        Wraps the given text into multiple lines to fit within max_width.
        Returns a list of text lines.
        """
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines


    def show_pause_menu(self, screen, font):
        """ 
        Display the pause menu with options: Resume, Options, Quit
        """
        global paused
        
        big_font = pygame.font.Font(None, 72)
        
        # Create an overlay
        overlay = pygame.Surface(screen.get_size())
        overlay.fill((17, 21, 56)) 
        screen.blit(overlay, (0, 0))

        # Create buttons
        resume_btn = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 70, 300, 50)
        options_btn = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 135, 300, 50)
        quit_btn = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 200, 300, 50)

        pygame.draw.rect(screen, (44, 53, 130), resume_btn)
        pygame.draw.rect(screen, (44, 53, 130), options_btn)
        pygame.draw.rect(screen, (44, 53, 130), quit_btn)

        # Button text
        resume_text = font.render("Resume", True, (255, 255, 255))
        options_text = font.render("Options", True, (255, 255, 255))
        quit_text = font.render("Main Menu", True, (255, 255, 255))
        paused_text = big_font.render("PAUSED", True, (255, 255, 255))

        screen.blit(resume_text, (resume_btn.centerx - resume_text.get_width() // 2, resume_btn.centery - resume_text.get_height() // 2))
        screen.blit(options_text, (options_btn.centerx - options_text.get_width() // 2, options_btn.centery - options_text.get_height() // 2))
        screen.blit(quit_text, (quit_btn.centerx - quit_text.get_width() // 2, quit_btn.centery - quit_text.get_height() // 2))
        screen.blit(paused_text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        
        pygame.display.update()

        # Handle events for the pause menu
        pause_menu_active = True
        while pause_menu_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        if resume_btn.collidepoint(event.pos):  # Check if Resume clicked
                            pause_menu_active = False
                            return "resume"
                        elif options_btn.collidepoint(event.pos):  # Check if Options clicked
                            pause_menu_active = False
                            result = self.paused_options_menu(screen, font)
                            if result == "back":
                                return None
                            pygame.display.update()
                        elif quit_btn.collidepoint(event.pos):  # Check if Quit clicked
                            paused = False
                            pause_menu_active = False
                            return "launch_game"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: # User presses escape, close menu
                        paused = False
                        pause_menu_active = False
                        return "resume"
                    
        pygame.display.update()

    def paused_options_menu(self, screen, font):
        """ 
        Display options menu with a "Back" button to return to the pause menu
        """
        pygame.display.update()
        
        # Create an overlay
        overlay = pygame.Surface(screen.get_size())
        overlay.fill((17, 21, 56)) 
        screen.blit(overlay, (0, 0))    
        
        back_btn = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 210, 200, 50)
        controls_btn = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150, 200, 50)
        pygame.draw.rect(screen, (44, 53, 130), back_btn)
        pygame.draw.rect(screen, (44, 53, 130), controls_btn)
        
        back_text = font.render("Back", True, (255, 255, 255))
        controls_text = font.render("Controls", True, (255, 255, 255))
        screen.blit(back_text, (back_btn.centerx - back_text.get_width() // 2, back_btn.centery - back_text.get_height() // 2))
        screen.blit(controls_text, (controls_btn.centerx - controls_text.get_width() // 2, controls_btn.centery - controls_text.get_height() // 2))
        
        pygame.display.update()

        options_menu_active = True
        while options_menu_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        if back_btn.collidepoint(event.pos):  # Check if Back clicked
                            options_menu_active = False
                            return "back"
                        if controls_btn.collidepoint(event.pos):
                            result = self.controls_menu(screen)
                            if result == "quit":
                                return "quit"
                            elif result == "backToOptions":
                                return self.paused_options_menu(screen, font)
                            

    def show_map_menu(self, screen):
        """ 
        Show the neighborhood map and allow the player to select a house to load 
        first_map.tmx 
        """
        
        neighborhood_map = pygame.image.load('../assets/map_selection.png')
        neighborhood_map = pygame.transform.scale(neighborhood_map, screen.get_size())  # Scale the image
        
        screen.blit(neighborhood_map, (0, 0))  # Display the neighborhood map
        
        # Create clickable areas for houses
        house_1_rect = pygame.Rect(85, 160, 100, 100)  # Rect for a house
        
        # Draw house areas
        pygame.draw.rect(screen, (255, 0, 0), house_1_rect, 5)  
        
        pygame.display.update()

        map_menu_active = True
        while map_menu_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_e:
                        map_menu_active = False
                    if event.type == pygame.K_ESCAPE:
                        map_menu_active = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        if house_1_rect.collidepoint(event.pos):  # Check if house 1 clicked
                            # print("House 1 clicked! Loading first_map.tmx...")
                            map_menu_active = False
                            return "load_first_map"
                        
    def show_shop_menu(self, screen, player, warehouse):
        """
        Displays the shop menu where the player can sell items from their inventory
        and buy upgrades or items from the shop. The warehouse inventory supports scrolling.
        """
        font = pygame.font.Font(None, 24)
        big_font = pygame.font.Font(None, 48)

        # Define shop upgrades
        shop_items = [
            {"name": "Increase Inventory Capacity", "price": 500, "effect": lambda: player.inventory.increase_capacity(5)},
            {"name": "Increase Player Speed by 1", "price": 1000, "effect": lambda: player.increase_player_speed(1)}
        ]

        # Menu dimensions
        shop_rect = pygame.Rect(20, 20, SCREEN_WIDTH * 1.5 - 40, SCREEN_HEIGHT * 1.5 - 40)
        shop_surface = pygame.Surface((shop_rect.width, shop_rect.height))
        shop_surface.fill((17, 21, 56))  # Dark blue background

        # Scrolling variable for warehouse inventory
        inventory_scroll_offset = 0
        scroll_step = 40  # Number of pixels to scroll per step

        run = True
        while run:
            # Draw the menu background
            screen.fill((44, 53, 130))
            screen.blit(shop_surface, (shop_rect.x, shop_rect.y))

            # Render titles
            title = big_font.render("Shop Menu", True, (255, 255, 255))
            shop_title = font.render("Shop Items (Click to Buy)", True, (255, 255, 255))
            inventory_title = font.render("Your Inventory (Click to Sell)", True, (255, 255, 255))

            screen.blit(title, (shop_rect.x + shop_rect.width // 2 - title.get_width() // 2, shop_rect.y + 10))
            screen.blit(shop_title, (shop_rect.x + 20, shop_rect.y + 80))
            screen.blit(inventory_title, (shop_rect.x + shop_rect.width // 2 + 20, shop_rect.y + 80))

            # Display shop items (fixed, no scrolling)
            for index, item in enumerate(shop_items):
                y_position = shop_rect.y + 120 + (index * 40)
                item_rect = pygame.Rect(shop_rect.x + 20, y_position, 300, 30)
                pygame.draw.rect(screen, (44, 53, 130), item_rect)
                item_text = font.render(f"{item['name']} - ${item['price']}", True, (255, 255, 255))
                screen.blit(item_text, (item_rect.x + 10, item_rect.y + 5))

            # Display warehouse inventory (supports scrolling)
            for index, item in enumerate(warehouse.warehouseItems):
                y_position = shop_rect.y + 120 + (index * 40) + inventory_scroll_offset
                if shop_rect.y + 120 <= y_position <= shop_rect.bottom - 40:
                    item_rect = pygame.Rect(shop_rect.x + shop_rect.width // 2 + 20, y_position, 300, 30)
                    pygame.draw.rect(screen, (44, 53, 130), item_rect)
                    item_text = font.render(f"{item['name']} - ${item.get('value', 0)}", True, (255, 255, 255))
                    screen.blit(item_text, (item_rect.x + 10, item_rect.y + 5))

            pygame.display.update()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    if event.key == pygame.K_e:
                        run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left-click
                        # Check if a shop item was clicked
                        for index, item in enumerate(shop_items):
                            y_position = shop_rect.y + 120 + (index * 40)
                            item_rect = pygame.Rect(shop_rect.x + 20, y_position, 300, 30)
                            if item_rect.collidepoint(event.pos):
                                if player.currency >= item["price"]:
                                    player.currency -= item["price"]
                                    item["effect"]()
                                    print(f"Bought {item['name']}")
                                else:
                                    print("Not enough money!")

                        # Check if a warehouse inventory item was clicked
                        for index, item in enumerate(warehouse.warehouseItems):
                            y_position = shop_rect.y + 120 + (index * 40) + inventory_scroll_offset
                            if shop_rect.y + 120 <= y_position <= shop_rect.bottom - 40:
                                item_rect = pygame.Rect(shop_rect.x + shop_rect.width // 2 + 20, y_position, 300, 30)
                                if item_rect.collidepoint(event.pos):
                                    player.currency += item.get("value", 0)
                                    warehouse.warehouseItems.pop(index)
                                    print(f"Sold {item['name']}")
                if event.type == pygame.MOUSEWHEEL:
                    # Handle scrolling for warehouse inventory only
                    if event.y > 0:  # Scroll up
                        inventory_scroll_offset = min(inventory_scroll_offset + scroll_step, 0)
                    elif event.y < 0:  # Scroll down
                        inventory_scroll_offset -= scroll_step

    def show_player_inventory(self, screen, player):
        """ 
        Display the player's inventory with scrolling, text wrapping, and scroll hint. 
        """
        # Scrolling variables
        inventory_scroll_offset = 0
        scroll_step = 2  # Number of rows to scroll per step
        grid_cols = 7  # Number of columns in the inventory grid
        cell_size = 80  # Size of each grid cell
        padding = 10  # Padding between cells
        font = pygame.font.Font(None, 22)
        title_font = pygame.font.Font(None, 36)
        hint_font = pygame.font.Font(None, 18)  # Smaller font for hint text

        inventory_open = True
        while inventory_open:
            # Menu overlay setup
            overlay = pygame.Surface(screen.get_size())
            overlay.fill((44, 53, 130))
            
            inner_overlay = pygame.Rect(20, 20, SCREEN_WIDTH * 1.5 - 40, SCREEN_HEIGHT * 1.5 - 40)  # 20px margin
            inner_surface = pygame.Surface((inner_overlay.width, inner_overlay.height))
            inner_surface.fill((17, 21, 56))
            
            overlay.blit(inner_surface, (20, 20))  # 20px margin
            screen.blit(overlay, (0, 0))

            title = title_font.render("Player's Inventory", True, (255, 255, 255))
            screen.blit(title, (inner_overlay.x + 20, inner_overlay.y + 20))

            # Starting position for grid
            x_start, y_start = inner_overlay.x + 20, inner_overlay.y + 60
            x, y = x_start, y_start

            # Calculate visible range of items
            rows_per_screen = (inner_overlay.height - 100) // (cell_size + padding)  # Rows that fit on screen
            start_index = inventory_scroll_offset * grid_cols
            end_index = start_index + rows_per_screen * grid_cols

            visible_items = player.inventory.playerItems[start_index:end_index]

            # Display items in grid
            for index, item in enumerate(visible_items):
                cell_center_x = x + cell_size // 2

                if item["image"]:
                    # Draw item image
                    image_size = 50
                    image_x = cell_center_x - image_size // 2
                    image_y = y + 10  # Slightly below the top of the cell
                    screen.blit(pygame.transform.scale(item["image"], (image_size, image_size)), (image_x, image_y))

                # Wrap and draw item name
                text_lines = self.wrap_text(item["name"], font, cell_size - 10)  # Wrap text to fit within the cell width
                text_y = y + cell_size - 10  # Start drawing text below the image
                for line in text_lines:
                    text = font.render(line, True, (255, 255, 255))
                    text_rect = text.get_rect(center=(cell_center_x, text_y))
                    screen.blit(text, text_rect)
                    text_y += text.get_height()  # Move to the next line
                
                # Move to next column or row
                x += cell_size + padding
                if (index + 1) % grid_cols == 0:
                    x = x_start
                    y += cell_size + padding

            # Check if scrolling is available and display the hint
            max_scroll = max(len(player.inventory.playerItems) // grid_cols - rows_per_screen + 1, 0)
            if max_scroll > 0:
                hint_text = "Scroll to view more of your Inventory"
                hint = hint_font.render(hint_text, True, (255, 255, 255))
                hint_x = SCREEN_WIDTH // 2
                hint_y = SCREEN_HEIGHT + 40 + hint.get_height()  # Position at the bottom center of the screen
                screen.blit(hint, (hint_x, hint_y))

            pygame.display.update()

            # Handle events
            for inv_event in pygame.event.get():
                if inv_event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if inv_event.type == pygame.KEYDOWN:
                    if inv_event.key == pygame.K_ESCAPE:  # Exit inventory
                        inventory_open = False
                    if inv_event.key == pygame.K_i:  # Close inventory
                        inventory_open = False
                if inv_event.type == pygame.MOUSEWHEEL:
                    # Handle scrolling
                    if inv_event.y > 0:  # Scroll up
                        inventory_scroll_offset = max(inventory_scroll_offset - scroll_step, 0)
                    elif inv_event.y < 0:  # Scroll down
                        inventory_scroll_offset = min(inventory_scroll_offset + scroll_step, max_scroll)

    def show_gameover_screen(self, screen, player):
        """
        Display the game-over screen with options.
        """
        font = pygame.font.Font(None, 36)
        title_font = pygame.font.Font(None, 48)
        
        # Calculate player's total score
        total_cash_from_inventory = 0
        total_score = 0

        for item in player.inventory.playerItems:
            if "Cash" in item["name"]:
                # Extract the cash value using regex
                match = re.search(r"\$\d+", item["name"])
                if match:
                    cash_value = int(match.group(0)[1:])  # Remove the "$" and convert to int
                    total_cash_from_inventory += cash_value
            else:
                # Add the value of non-cash items
                total_score += item.get("value", 0)

        total_score += total_cash_from_inventory  # Add cash value from inventory to the total score

        # Clear player's inventory and reset cash
        player.inventory.playerItems = []  # Clear all items

        # Menu options
        lobby_btn = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90, 225, 50)
        quit_btn = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 160, 225, 50)
        
        run = True
        while run:
            screen.fill((17, 21, 56))  # Background color

            # Display title
            title = title_font.render("Game Over!", True, (255, 255, 255))
            screen.blit(title, (SCREEN_WIDTH // 2 + (title.get_width() // 8) - 10, SCREEN_HEIGHT // 4))
            
            # Display score
            score_text = font.render(f"Your Score: {total_score}", True, (255, 255, 255))
            screen.blit(score_text, (SCREEN_WIDTH // 2 + 25, SCREEN_HEIGHT // 3 + 10))
            
            # Render buttons
            pygame.draw.rect(screen, (44, 53, 130), quit_btn)
            pygame.draw.rect(screen, (44, 53, 130), lobby_btn)
            
            # Button text
            quit_text = font.render("Quit", True, (255, 255, 255))
            lobby_text = font.render("Return to Lobby", True, (255, 255, 255))
            
            screen.blit(quit_text, (quit_btn.centerx - quit_text.get_width() // 2, quit_btn.centery - quit_text.get_height() // 2))
            screen.blit(lobby_text, (lobby_btn.centerx - lobby_text.get_width() // 2, lobby_btn.centery - lobby_text.get_height() // 2))
            
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if quit_btn.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    if lobby_btn.collidepoint(event.pos):
                        run = False
                        return "lobby"