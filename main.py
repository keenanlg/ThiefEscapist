#################################################
# Names:        Caleb Murphy & Keenan Grant     #
# Date:         10/20/2024                      #
# Class:        CPSC 4160                       #
# Assignment:   Final                           #
#################################################

# Lines: 2314

# Imports
import pygame, sys, loot
from player import Character
from tile import Tile, ObjectTile
from menus import Menu
from floor_traversal import *
from pytmx.util_pygame import load_pygame
from astar import *
from npc import NPC, ShopNPC
from inventory import Inventory
from loot import *
from vfx import VFX
from globals import *
from astar import *
import re, time
import random

# Init Pygame
pygame.init()

# Create screen, caption, and load lobby map
screen = pygame.display.set_mode((SCREEN_WIDTH * 1.5, SCREEN_HEIGHT * 1.5))
pygame.display.set_caption("Thief Escapist")
current_map = "lobby"

# Create sprite group
sprite_group = pygame.sprite.Group()

# Load the currency icon
currency_icon = pygame.image.load("../assets/UI/Icons/Currency.png")  
currency_icon = pygame.transform.scale(currency_icon, (16, 16))  

# Position and Speed of Camera
camera_x = 255 * CAMERA_SCALE
camera_y = 200 * CAMERA_SCALE

# Create objects
player = Character(position = (835, 956))
shop_npc = None
menu_obj = Menu()

# Create warehouse's inventory
warehouse_inv = Inventory()

# Global rects
van_rect = None
exit_rect = None
clipboard_rect = None
exit_fm_rect = None
shop_rect = None
stolen_npc4_position = None
stolen_item_flag = False

lobby_loaded = False
first_map_loaded = False
tutorial_played = False

big_font = pygame.font.Font(None, 56)
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

def game_loop(screen, sprite_group, player, camera_x, camera_y):
    """
    This function controls the entire loop of the game. Once the game
    starts, it will be utilizing this function for all functionality.
    """
    global tmx_data, paused, shop_npc, exit_door_data, exit_door_disabled_time, stolen_npc4_position, random_item, path_node_coords
    
    path_node_coords = []

    if current_map == "lobby" and lobby_loaded == False:
        load_lobby_map()
    
    # Load map
    load_map(tmx_data)

    floor1_items = ["Door Dresser", "StairSafe", "Fireplace", "Left Table", "Kitchen Cabinet"]
    floor2_items = ["Desk", "Washer1", "Washer2", "Arcade", "Arcade Hide", "Bathroom Sink"]
    
    # Randomly select items to have stolen detection
    random_item = random.choice(floor1_items + floor2_items)

    if current_map == "first_map":
        # Keep track of how long door should remain disabled
        exit_door_disabled_time = time.time()

        # Print random item for debugging
        print("Random item:", random_item)
    
    # Game loop
    run = True
    while run:
        clock.tick(FPS)
        
        # Display FPS in Application Caption
        pygame.display.set_caption(f"Thief Escapist - FPS: {clock.get_fps():.2f}")
        
        if paused:
            result = menu_obj.show_pause_menu(screen, font)
            if result == "launch_game":
                launch_game()
                continue
            elif result == "resume":
                paused = False
                continue
            elif result is None:
                continue

        # Draw sprite groups with adjusted camera
        for sprite in sprite_group:
            screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y - camera_y))

        if shop_npc and current_map == "lobby":
            shop_npc.update()
            shop_npc.draw(screen, camera_x, camera_y)
            
            render_shop_text(screen, tmx_data, camera_x, camera_y)
            
        # Input data
        key = pygame.key.get_pressed()

        if current_map == "first_map":
            # create_graph()
            # graph.visualize_graph(screen, camera_x, camera_y)
            
            for effect in vfx:
                if effect.id in looted_objects_id:
                    vfx.remove(effect)

            # Draw the purple rectangle if an item has been stolen
            # if stolen_npc4_position:
            #     rect_pos = (stolen_npc4_position.x - camera_x, stolen_npc4_position.y - camera_y, stolen_npc4_position.width, stolen_npc4_position.height)
            #     pygame.draw.rect(screen, (255, 0, 255), rect_pos)  # Purple rectangle

            # Update vfx and render them
            for effect in vfx:
                effect.update()
                effect.draw(screen, camera_x, camera_y)
            
            # Update NPCs and render them
            for npc in npcs:
                npc.update_npc(player, SCALE)
                npc.draw(screen, camera_x, camera_y)
                
                if npc.rect.colliderect(player.rect) and npc.alerted:
                    selection = menu_obj.show_gameover_screen(screen, player)
                    player.visible = True
                    if selection == "lobby":
                        load_lobby_map()
                        continue
            
            # Handle elevators and update camera_y
            for elevator in elevator_boxes:
                elevator.check_elevator_trigger(player, key)
                if elevator.elevator_box_triggered:  # Only adjust camera_y for active elevators
                    camera_y = elevator.handle_elevator_movement(player, camera_y)
                    
            # Update camera position during normal gameplay if no elevator is active
            if not any(elevator.elevator_box_triggered for elevator in elevator_boxes):
                camera_x = player.rect.x - (SCREEN_WIDTH // 2 + 96)
                camera_y = player.rect.y - (SCREEN_HEIGHT // 2)
            
            for stair_box in stair_boxes:
                # stair_box.draw(screen, camera_x, camera_y)
                stair_box.check_stair_trigger(player, key)
                stair_box.handle_stair_movement(player, key) 
            
            
        if current_map != "first_map":
            camera_x = player.rect.x - (SCREEN_WIDTH // 2 + 96)
            camera_y = player.rect.y - (SCREEN_HEIGHT // 2)
            
        # Handle player's movement
        player.handle_movement(key, SCALE)

        # Clamp the camera position within the map bounds
        camera_x = max(0, min(camera_x, HOUSE_WIDTH - (HOUSE_WIDTH / 2.5)))
        camera_y = max(0, min(camera_y, HOUSE_HEIGHT))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                handle_event(event)

        # Draw player   
        player.draw(screen, camera_x, camera_y)
        
        # Diplay currency on screen
        screen.blit(currency_icon, (10, 10))
        money_text = small_font.render(f"Money: {player.currency:.2f}", True, (255, 255, 255))
        screen.blit(money_text, (30, 11))
        
        # Display player's score on screen
        player_score_text = small_font.render(f"Score: {player.score}", True, (255, 255, 255))
        screen.blit(player_score_text, (10, 30))
        
        pygame.display.update()
                
def load_map(tmx_data):
    """ 
    This function is used to load all map data and create the
    appropriate tile objects. 
    """
    global van_rect, exit_rect, clipboard_rect, exit_fm_rect, shop_rect
    
    # Cycle through all tile layers & loads all
    for layer in tmx_data.visible_layers:
        if hasattr(layer, 'data'):
            for x, y, surf in layer.tiles():
                pos = (x * TILE_SIZE * SCALE, y * TILE_SIZE * SCALE)
                Tile(pos = pos, surface = surf, groups = sprite_group, scale = SCALE)

    # Cycle through all object layers & loads all
    for object in tmx_data.objects:
        if object.image:
            ObjectTile(object = object, groups = sprite_group, scale = SCALE)
    
    # Check if the "Collisions" layer exists
    collisions_layer = None
    try:
        collisions_layer = tmx_data.get_layer_by_name("Collisions")
    except ValueError:
        print("No 'Collisions' layer found, skipping collision processing.")
    
    if collisions_layer != None:
        collisions_layer = tmx_data.get_layer_by_name("Collisions")
        for object in collisions_layer:
            if object.name == "Van":
                van_rect = create_rect(object)
                # print(f"Van rect created at: {van_rect.topleft} with size: {van_rect.size}")
            if object.name == "Exit Door":
                exit_rect = create_rect(object)
                # print(f"Exit rect created at: {exit_rect.topleft} with size: {exit_rect.size}") 
            if object.name == "Clipboard Wall":
                clipboard_rect = create_rect(object)
                # print(f"Clipboard rect created at: {clipboard_rect.topleft} with size: {clipboard_rect.size}")
            if object.name == "Exit Door FM":
                exit_fm_rect = create_rect(object)
                # print(f"Exit Door in FM rect created at: {exit_fm_rect.topleft} with size: {exit_fm_rect.size}")
            if object.name == "Shop":
                shop_rect = create_rect(object)

def create_rect(obj):
    # print(f"Processing object: {obj.name}, Type: {obj.type}")
    if obj.type == "Polygon":
        if hasattr(obj, 'points'):
            points = [(point.x * SCALE, point.y * SCALE) for point in obj.points]
            # print(f"Polygon points: {points}")
        else:
            # print(f"Polygon object {obj.name} does not have 'points' attribute.")
            return None
        min_x = min([point[0] for point in points])
        min_y = min([point[1] for point in points])
        max_x = max([point[0] for point in points])
        max_y = max([point[1] for point in points])
        rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
        # print(f"Created rect for {obj.name}: {rect}")
        return rect
    elif obj.type == "Rectangle":
        if hasattr(obj, 'as_points'):
            points = [(point.x * SCALE, point.y * SCALE) for point in obj.as_points]
            # print(f"Rectangle points: {points}")
        else:
            # print(f"Rectangle object {obj.name} does not have 'as_points' attribute.")
            return None
        min_x = min([point[0] for point in points])
        min_y = min([point[1] for point in points])
        max_x = max([point[0] for point in points])
        max_y = max([point[1] for point in points])
        rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
        # print(f"Created rect for {obj.name}: {rect}")
        return rect
    else:
        # print(f"Object {obj.name} has an unsupported type: {obj.type}")
        return None

def handle_event(event):
    """ 
    This function is used to handle the KEYDOWN events made via
    the user. Helper function is needed to reduce clutter in main
    game loop.
    """
    global paused, looted_objects, exit_door_disabled_time, stolen_npc4_position, S3B2_position, E2B2_position, S3B2_distance, E2B2_distance, npc4
    
    # Pause
    if event.key == pygame.K_ESCAPE:
        paused = not paused

    keys = pygame.key.get_pressed()
    if keys[pygame.K_f]:
        for obj in tmx_data.objects:
            item_rect = pygame.Rect(obj.x * SCALE, obj.y * SCALE, obj.width * SCALE, obj.height * SCALE)
            if obj.name == "Fireplace" and player.rect.colliderect(item_rect):
                player.visible = False
            if obj.name == "Bed" and player.rect.colliderect(item_rect):
                player.visible = False
            if obj.name == "Bench" and player.rect.colliderect(item_rect):
                player.visible = False
            if obj.name == "Refrigerator" and player.rect.colliderect(item_rect):
                player.visible = False
            if obj.name == "Arcade Hide" and player.rect.colliderect(item_rect):
                player.visible = False
            if obj.name == "Shower1" and player.rect.colliderect(item_rect):
                player.visible = False
            if obj.name == "Shower2" and player.rect.colliderect(item_rect):
                player.visible = False
            if obj.name == "Beds" and player.rect.colliderect(item_rect):
                player.visible = False
            if obj.name == "Movie Room" and player.rect.colliderect(item_rect):
                player.visible = False
            if obj.name == "Attic Wardrobe" and player.rect.colliderect(item_rect):
                player.visible = False
            if obj.name == "Attic Box Lg1" and player.rect.colliderect(item_rect):
                player.visible = False
            if obj.name == "Attic Box Lg2" and player.rect.colliderect(item_rect):
                player.visible = False
                
    if keys[pygame.K_a] or keys[pygame.K_d]:
        player.visible = True
    
    # Interaction
    if event.key == pygame.K_e:
        for obj in tmx_data.objects:
            if obj.name == "Fireplace":
                loot.loot_tables(obj, player, loot.fireplace_loot_table)
            if obj.name == "StairSafe":
                loot.loot_tables(obj, player, loot.safe_loot_table)
            if obj.name == "Desk":
                loot.loot_tables(obj, player, loot.desk_loot_table)
            # if obj.name == "Sidetable":
            #     loot.loot_tables(obj, player, loot.sidetable_loot_table)
            if obj.name == "Door Dresser":
                loot.loot_tables(obj, player, loot.door_dresser_loot_table)
            if obj.name == "Kitchen Cabinet":
                loot.loot_tables(obj, player, loot.kitchen_cabinet_loot_table)
            if obj.name == "Attic Safe":
                loot.loot_tables(obj, player, loot.attic_safe_loot_table)
            if obj.name == "Attic Box Lg":
                loot.loot_tables(obj, player, loot.attic_boxes_large_loot_table)
            if obj.name == "Attic Box Lg1":
                loot.loot_tables(obj, player, loot.attic_boxes_large_loot_table)
            if obj.name == "Attic Box Lg2":
                loot.loot_tables(obj, player, loot.attic_boxes_large_loot_table)
            if obj.name == "Attic Box Sm":
                loot.loot_tables(obj, player, loot.attic_boxes_small_loot_table)
            if obj.name == "Attic Wardrobe":
                loot.loot_tables(obj, player, loot.attic_wardrobe_loot_table)
            # if obj.name == "Shower":
            #     loot.loot_tables(obj, player, loot.shower_loot_table)
            if obj.name == "Bathroom Sink":
                loot.loot_tables(obj, player, loot.bathroom_sink_loot_table)
            if obj.name == "Arcade":
                loot.loot_tables(obj, player, loot.arcade_game_loot_table)
            if obj.name == "Arcade Hide":
                loot.loot_tables(obj, player, loot.arcade_game_loot_table)
            if obj.name == "Washer1":
                loot.loot_tables(obj, player, loot.washer_dryer_loot_table)
            if obj.name == "Washer2":
                loot.loot_tables(obj, player, loot.washer_dryer_loot_table)
            if obj.name == "Wardrobe":
                loot.loot_tables(obj, player, loot.wardrobe_loot_table)
            # if obj.name == "Right Table":
            #     loot.loot_tables(obj, player, loot.table_loot_table)
            if obj.name == "Left Table":
                loot.loot_tables(obj, player, loot.table_loot_table)
            # if obj.name == "Refrigerator":
            #     loot.loot_tables(obj, player, loot.refrigerator_loot_table)
            # if obj.name == "Kitchen Sink":
            #     loot.loot_tables(obj, player, loot.kitchen_sink_loot_table)
            if obj.name == "Movie Room":
                loot.loot_tables(obj, player, loot.sidetable_loot_table)
            if obj.name == random_item and player.rect.colliderect(obj.x * SCALE, obj.y * SCALE, obj.width * SCALE, obj.height * SCALE):
                stolen_npc4_position = pygame.Rect(npc4.rect.x, npc4.rect.y, npc4.rect.width, npc4.rect.height)
                stolen_npc4_y = stolen_npc4_position.y
                S3B2_distance = abs(stolen_npc4_position.x - S3B2_position.x)
                E2B2_distance = abs(stolen_npc4_position.x - E2B2_position.x)
                print("S3B2 distance:", S3B2_distance)
                print("E2B2 distance:", E2B2_distance)
                random_obj_pos = (obj.x * SCALE, obj.y * SCALE)
                path_node_coords = create_graph(S3B2_distance, E2B2_distance, stolen_npc4_y, obj.name, random_obj_pos)
                npc4.set_path_node_coords(path_node_coords)

            if van_rect is not None and obj.name == "Van" and player.rect.colliderect(van_rect):
                result = menu_obj.show_map_menu(screen)
                if result == "load_first_map":
                    load_first_map()
                else:
                    print("error with van_rect")
                return
            if exit_rect is not None and obj.name == "Exit Door" and player.rect.colliderect(exit_rect):
                pygame.quit()
                sys.exit()
            if clipboard_rect is not None and obj.name == "Clipboard Wall" and player.rect.colliderect(clipboard_rect):
                menu_obj.show_warehouse_menu(screen, warehouse_inv)
                return
            if exit_fm_rect is not None and obj.name == "Exit Door FM" and player.rect.colliderect(exit_fm_rect) and (time.time() - exit_door_disabled_time >= 30):
                transfer_items_calculate_score(player, warehouse_inv)
                load_lobby_map()
                return
            if shop_rect is not None and obj.name == "Shop" and player.rect.colliderect(shop_rect):
                menu_obj.show_shop_menu(screen, player, warehouse_inv)
                return

    # Open inventory
    if event.key == pygame.K_i:
        menu_obj.show_player_inventory(screen, player)

def play_music(music_file, volume, fadeout_time=1000):
    """
    Plays the specified music file with a fade transition if needed.
    """
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(fadeout_time)  # Fade out current music
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1, 0, 1000)  # Loop the music indefinitely


def load_first_map():
    """
    Load the first map and spawn NPCs and stair boxes
    """
    global tmx_data, current_map, lobby_loaded, first_map_loaded, shop_npc
    
    tmx_data = load_pygame('../tmx/first_map.tmx')  # Load the first map
    current_map = 'first_map'  # Set the current map to first_map.tmx
    lobby_loaded = False
    first_map_loaded = True
    
    # Play thief music
    play_music("../assets/mapMusic.mp3", 0.05)

    # Move player futher into the house on spawn
    player.rect.x = 535
    
    # Make player face right on map load
    player.wentLeft = False
    player.wentRight = True

    # Reset and spawn NPCs, stair boxes, and any other objects
    npcs_traversals_vfx()

    # Initialize the game loop for the first map
    game_loop(screen, sprite_group, player, camera_x, camera_y)
    
def load_lobby_map():
    """
    Load the lobby map
    """
    global tmx_data, current_map, lobby_loaded, first_map_loaded, shop_npc
    tmx_data = load_pygame('../tmx/lobby.tmx')
    current_map = 'lobby'
    lobby_loaded = True
    first_map_loaded = False

    # Play lobby music
    play_music("../assets/lobbyMusic.mp3", 0.25)
    
    if shop_npc is None:
        shop_npc = ShopNPC(position=(1425, 956), name="Female/NPC 13", scale=SCALE)
        
    # Move player back to spawn point
    player.rect.x = 835
    player.rect.y = 956
    
    # Reset player speed from upgrades
    player.speed = 5
    
    # Initialize the game loop for lobby
    game_loop(screen, sprite_group, player, camera_x, camera_y)
    
def npcs_traversals_vfx():
    global npcs, stair_boxes, elevator_boxes, vfx, looted_objects, looted_objects_id, npc4, S3B2_position, E2B2_position
    
    # Reset looted items on map launch
    looted_objects.clear()
    looted_objects_id.clear()
    
    # Spawn NPCs for the first map
    npc1 = NPC(position=(1024, 956), patrol_start=512, patrol_end=1728, speed=2, name = "Male/NPC 4", direction = 1) #1st floor
    npc2 = NPC(position=(1728, 768), patrol_start=512, patrol_end=1728, speed=2, name = "Female/NPC 11", direction = -1) #2nd floor
    npc3 = NPC(position=(832, 576), patrol_start=512, patrol_end=1728, speed=2, name = "Male/NPC 3", direction = 1) #3rd floor
    npc4 = NPC(position=(1344, 384), patrol_start=512, patrol_end=1728, speed=2, name = "Female/NPC 6", direction = -1) #4th floor

    npcs = [npc1, npc2, npc3, npc4]

    # Spawn stair boxes for the first map
    stair1_box1 = StairHandler(box_x = 795, box_y = 960, box_width = 20, box_height = 20, xdirection = 1, ydirection = -1, destination_y = 774)
    stair1_box2 = StairHandler(box_x = 995, box_y = 768, box_width = 20, box_height = 20, xdirection = -1, ydirection = 1, destination_y = 956)
    stair2_box1 = StairHandler(box_x = 1324, box_y = 768, box_width = 20, box_height = 20, xdirection = 1, ydirection = -1, destination_y = 580)
    stair2_box2 = StairHandler(box_x = 1506, box_y = 576, box_width = 20, box_height = 20, xdirection = -1, ydirection = 1, destination_y = 770)
    stair3_box1 = StairHandler(box_x = 952, box_y = 576, box_width = 20, box_height = 20, xdirection = -1, ydirection = -1, destination_y = 390)
    stair3_box2 = StairHandler(box_x = 752, box_y = 384, box_width = 20, box_height = 20, xdirection = 1, ydirection = 1, destination_y = 576)

    S3B2_position = stair3_box2.stair_box

    stair_boxes = [stair1_box1, stair1_box2, stair2_box1, stair2_box2, stair3_box1, stair3_box2]

    # Spawn elevator boxes    
    elevator1_box1 = ElevatorHandler(box_x = 986, box_y = 944, box_width = 80, box_height = 68, destination_y = 576, speed = 3)
    elevator1_box2 = ElevatorHandler(box_x = 986, box_y = 560, box_width = 80, box_height = 68, destination_y = 956, speed = 3)
    elevator2_box1 = ElevatorHandler(box_x = 1688, box_y = 944, box_width = 80, box_height = 68, destination_y = 384, speed = 3)
    elevator2_box2 = ElevatorHandler(box_x = 1688, box_y = 368, box_width = 80, box_height = 68, destination_y = 956, speed = 3)

    E2B2_position = elevator2_box2.elevator_box

    elevator_boxes = [elevator1_box1, elevator1_box2, elevator2_box1, elevator2_box2]

    #Spawn vfx
    #Sparkles
    Sfireplace = VFX((1136, 978), "sparkle32", 32, 3, 10, 44)
    safe1 = VFX((878, 982), "sparkle32", 32, 3, 10, 101)
    dining_table = VFX((1290, 972), "sparkle32", 32, 3, 10, 52)
    kitchen_sink = VFX((1482, 980), "sparkle32", 32, 3, 10, 86)
    washer = VFX((910, 788), "sparkle32", 32, 3, 10, 56)
    washer2 = VFX((980, 788), "sparkle32", 32, 3, 10, 57)
    bth1_sink = VFX((1600, 790), "sparkle32", 32, 3, 10, 62)
    bedr1 = VFX((660, 780), "sparkle32", 32, 3, 10, 100)
    movie_room = VFX((1662, 592), "sparkle32", 32, 3, 10, 124)
    bth2_sink = VFX((646, 590), "sparkle32", 32, 3, 10, 64)
    safe2 = VFX((1104, 400), "sparkle32", 32, 3, 10, 73)
    front_drawer = VFX((592, 968), "sparkle32", 32, 3, 10, 87)
    arcade1 = VFX((1052, 788), "sparkle32", 32, 3, 10, 58)
    arcade2 = VFX((1180, 788), "sparkle32", 32, 3, 10, 60)

    Lwardrobe = VFX((576, 384), "sparkle32", 32, 3, 10, 66)
    Lbox1 = VFX((648, 400), "sparkle32", 32, 3, 10, 67)
    Lbox2 = VFX((776, 400), "sparkle32", 32, 3, 10, 68)
    Lbox3 = VFX((840, 400), "sparkle32", 32, 3, 10, 72)
    Lbox4 = VFX((1224, 400), "sparkle32", 32, 3, 10, 69)
    Lbox5 = VFX((1352, 400), "sparkle32", 32, 3, 10, 70)
    Lbox6 = VFX((1544, 400), "sparkle32", 32, 3, 10, 71)
    
    #Hidings
    bench = VFX((675, 978), "hiding64", 64, 7, 49, None)
    Hfireplace = VFX((1120, 970), "hiding64", 64, 7, 49, None)
    refrigerator = VFX((1600, 960), "hiding64", 64, 7, 49, None)
    bed = VFX((548, 768), "hiding64", 64, 7, 49, None)
    arcadeGreen = VFX((1160, 768), "hiding64", 64, 7, 49, None)
    shower1 = VFX((1728, 768), "hiding64", 64, 7, 49, None)
    shower2 = VFX((520, 576), "hiding64", 64, 7, 49, None)
    beds = VFX((1188, 576), "hiding64", 64, 7, 49, None)
    movie = VFX((1640, 576), "hiding64", 64, 7, 49, None)
    dresser = VFX((571, 384), "hiding64", 64, 7, 49, None)
    box1 = VFX((1211, 384), "hiding64", 64, 7, 49, None)
    box2 = VFX((1531, 384), "hiding64", 64, 7, 49, None)

    vfx = [Sfireplace, safe1, dining_table, kitchen_sink, washer, washer2, bth1_sink, bedr1, movie_room, bth2_sink, safe2,
           Lwardrobe, Lbox1, Lbox2, Lbox3, Lbox4, Lbox5, Lbox6, arcade1, arcade2, front_drawer,
           bench, Hfireplace, refrigerator, bed, arcadeGreen, shower1, shower2, beds, movie, dresser, box1, box2]
    
def create_graph(S3B2_distance, E2B2_distance, stolen_npc4_y, destination, destination_pos):
    global graph, path_node_coords

    graph = Graph(S3B2_distance, E2B2_distance, stolen_npc4_y, destination, destination_pos)
    path = graph.a_star_algorithm()
    path_node_coords = graph.get_path_coordinates(path)
    print(f"Shortest path: {' -> '.join(path)}")
    return path_node_coords

def render_shop_text(screen, tmx_data, camera_x, camera_y):
    static_text_positions = {}  # Store text and position for static rendering

    for obj in tmx_data.objects:
        if obj.name == "Text" and obj.type == "Text":
            # Use a unique identifier for each object
            obj_key = (obj.id, obj.x, obj.y)

            if obj_key not in static_text_positions:
                # Fetch text properties or use a default
                text = "SHOP"

                color = pygame.Color(obj.properties.get("color", "#FFFFFF"))
                font_size = int(obj.properties.get("pixelsize", 44))
                text_font = pygame.font.Font(None, font_size)
                rendered_text = text_font.render(text, True, color)

                # Calculate and store the static position
                text_x = obj.x * SCALE + 3
                text_y = obj.y * SCALE + 10
                static_text_positions[obj_key] = (rendered_text, (text_x, text_y))
                # print(f"Calculated static position for text '{text}' at ({text_x}, {text_y})")

            # Retrieve the rendered text and position
            rendered_text, (static_x, static_y) = static_text_positions[obj_key]
            screen.blit(rendered_text, (static_x - camera_x, static_y - camera_y))

def transfer_items_calculate_score(player, warehouse_inv):
    total_cash = 0
    total_item_value = 0
    font = pygame.font.Font(None, 36)

    # Separate cash and non-cash items
    remaining_items = []

    for item in player.inventory.playerItems:
        if "Cash" in item["name"]:  # Check if the item is "Cash"
            # Extract the cash value using regex
            match = re.search(r"\$\d+", item["name"])
            if match:
                cash_value = int(match.group(0)[1:])  # Skip the '$' sign
                total_cash += cash_value
        else:
            # Add item value to total item value
            total_item_value += item.get("value", 0)  # Default value is 0 if not present
            remaining_items.append(item)

    # Update player's currency and score
    player.currency += total_cash
    player.score += total_cash + total_item_value  # Total score includes cash and item values

    # print(f"Total cash added to score: {total_cash}")
    # total_cash_text = font.render("")
    # print(f"Total item value added to score: {total_item_value}")
    # print(f"Player's total score: {player.score}")

    # Transfer remaining items to the warehouse
    warehouse_inv.warehouseItems.extend(remaining_items)

    # Clear the player's inventory
    player.inventory.playerItems = []

def show_tutorial_screen(screen):
    """
    Display a series of tutorial screens
    """
    global tutorial_played
    
    tutorial_played = True
    
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 48)

    # Tutorial text for each screen
    tutorial_pages = [
        "Welcome to Thief Escapist! Your goal is to loot valuables while avoiding detection.",
        "Use the 'A' and 'D' keys to move left and right. Interact with objects using 'E' to collect items.",
        "Items with a sparkle effect on them are considered Lootable. Find those and interact with them.",
        "Be careful of NPCs! If they catch you, it's game over.",
        "To hide from NPCs, press 'F' in an area with a circle animation.",
        "Press 'I' to open your inventory and view the items you've collected.",
        "To view these controls again, press ESCAPE, click Options, then Controls.",
        "Good luck, and happy looting!"
    ]

    page_index = 0
    run_tutorial = True

    while run_tutorial:
        screen.fill((17, 21, 56))

        # Display tutorial title
        title = title_font.render("Tutorial", True, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH // 2 + (title.get_width() // 2), 50))

        # Wrap and center current tutorial text
        margin = 20
        max_text_width = SCREEN_WIDTH - 2 * margin
        wrapped_text = menu_obj.wrap_text(tutorial_pages[page_index], font, max_text_width)

        # Calculate total height of wrapped text
        total_text_height = sum(font.size(line)[1] for line in wrapped_text) + (len(wrapped_text) - 1) * 5
        start_y = ((SCREEN_HEIGHT // 2) - 10) + (total_text_height // 2)  # Center vertically in paragraph box

        # Display each line of wrapped text
        text_y = start_y
        for line in wrapped_text:
            line_text = font.render(line, True, (255, 255, 255))
            line_text_rect = line_text.get_rect(center=((SCREEN_WIDTH // 2) + 125, text_y))
            screen.blit(line_text, line_text_rect)
            text_y += line_text.get_height() + 5  # Add spacing between lines

        # Draw "Next" button
        next_btn = pygame.Rect((SCREEN_WIDTH // 2) + 25, SCREEN_HEIGHT, 200, 50)
        pygame.draw.rect(screen, (44, 53, 130), next_btn)
        next_text = font.render("Next", True, (255, 255, 255))
        next_text_rect = next_text.get_rect(center=next_btn.center)
        screen.blit(next_text, next_text_rect)

        pygame.display.update()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if next_btn.collidepoint(event.pos):
                    # Move to the next page or exit tutorial if it's the last page
                    if page_index < len(tutorial_pages) - 1:
                        page_index += 1
                    else:
                        run_tutorial = False

def launch_game():
    global paused, lobby_loaded, current_map
    menu = menu_obj.start_menu(screen)
    while (menu != "quit"):
        if menu == "start":
            paused = False
            lobby_loaded = False
            current_map = "lobby"
            if tutorial_played == False:
                show_tutorial_screen(screen)
            game_loop(screen, sprite_group, player, camera_x, camera_y)
        elif menu == "options":
            menu = menu_obj.options_menu(screen)
        elif menu == "back":
            menu = menu_obj.start_menu(screen)
            
    if menu == "quit":
        pygame.quit()
        sys.exit()

#! GAME LAUNCHED !#
launch_game()

# Quit
pygame.quit()
sys.exit()