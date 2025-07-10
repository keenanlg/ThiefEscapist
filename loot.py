import random, pygame
from globals import *

# Loot table for the "Safe" object
safe_loot_table = {
    "Cash": {"chance": 30, "image": "../assets/UI/Icons/Currency.png"},
    "Trophy": {"chance": 5, "image": "../assets/Individual Assets/Objects/Bedroom/Trophy.png", "value": 50},
    "Crown": {"chance": 4, "image": "../assets/Expansions/Archaeology/Individual Assets/Crown.png", "value": 150},
    "Jewelry": {"chance": 15, "image": "../assets/Expansions/Archaeology/Individual Assets/Jewelry_red.png", "value": 100},
    "Megalodon Tooth": {"chance": 2, "image": "../assets/Expansions/Archaeology/Individual Assets/MegalodonTooth.png", "value": 200},
    "Pottery": {"chance": 4, "image": "../assets/Expansions/Archaeology/Individual Assets/Pottery_ancient_5.png", "value": 70},
    "Stone Tablet": {"chance": 2, "image": "../assets/Expansions/Archaeology/Individual Assets/StoneTablet_grey.png", "value": 120},
    "Buried Sword": {"chance": 1, "image": "../assets/Expansions/Archaeology/Individual Assets/Sword_buried.png", "value": 300},
    "Neolithic Mask": {"chance": 1, "image": "../assets/Expansions/Archaeology/Individual Assets/NeolithicMask.png", "value": 250},
    "Framed Certificate": {"chance": 8, "image": "../assets/Expansions/Fire Station/Individual Assets/FramedCertification.png", "value": 40},
    "Mona Lisa": {"chance": 1, "image": "../assets/Expansions/Museum/Individual Assets/Painting_mona_pixa.png", "value": 500},
    "Blurry Nights": {"chance": 2, "image": "../assets/Expansions/Museum/Individual Assets/Painting_blocky_night.png", "value": 150},
    "Framed Award": {"chance": 10, "image": "../assets/Expansions/Police Station/Individual Assets/Framed_award.png", "value": 35},
    "No Loot": {"chance": 15, "image": None},
}

fireplace_loot_table = {
    "Cash": {"chance": 40, "image": "../assets/UI/Icons/Currency.png"},
    "Jewelry": {"chance": 20, "image": "../assets/Expansions/Archaeology/Individual Assets/Jewelry_red.png", "value": 100},
    "Buried Sword": {"chance": 10, "image": "../assets/Expansions/Archaeology/Individual Assets/Sword_buried.png", "value": 300},
    "No Loot": {"chance": 30, "image": None},
}

table_loot_table = {
    "Laptop": {"chance": 10, "image": "../assets/Individual Assets/Objects/Bedroom/Laptop.png", "value": 150},
    "Rum": {"chance": 5, "image": "../assets/Individual Assets/Objects/Kitchen/Bottle_green.png", "value": 25},
    "Beer": {"chance": 5, "image": "../assets/Individual Assets/Objects/Kitchen/Bottle_red.png", "value": 20},
    "Water": {"chance": 10, "image": "../assets/Individual Assets/Objects/Kitchen/Glass_water.png", "value": 10},
    "Glass Cup": {"chance": 10, "image": "../assets/Individual Assets/Objects/Kitchen/Glass.png", "value": 15},
    "Glass Pitcher": {"chance": 5, "image": "../assets/Individual Assets/Objects/Kitchen/Glass_pitcher.png", "value": 25},
    "Knife": {"chance": 8, "image": "../assets/Individual Assets/Objects/Kitchen/Knife_1.png", "value": 30},
    "Mug": {"chance": 10, "image": "../assets/Individual Assets/Objects/Kitchen/Mug.png", "value": 10},
    "Radio": {"chance": 5, "image": "../assets/Individual Assets/Objects/Living Room/Radio.png", "value": 40},
    "Bananas": {"chance": 7, "image": "../assets/Individual Assets/Objects/Kitchen/Bananas.png", "value": 5},
    "Apple": {"chance": 7, "image": "../assets/Individual Assets/Objects/Kitchen/Apple.png", "value": 5},
    "Orange": {"chance": 7, "image": "../assets/Individual Assets/Objects/Kitchen/Orange.png", "value": 5},
    "Pineapple": {"chance": 3, "image": "../assets/Individual Assets/Objects/Kitchen/Pineapple.png", "value": 15},
    "Cash": {"chance": 8, "image": "../assets/UI/Icons/Currency.png"},
}

kitchen_sink_loot_table = {
    "Windex": {"chance": 30, "image": "../assets/Individual Assets/Objects/Bathroom/Shampoo_1.png", "value": 15},
    "Cleaning Soap": {"chance": 20, "image": "../assets/Individual Assets/Objects/Bathroom/Shampoo_3.png", "value": 10},
    "Fire Extinguisher": {"chance": 5, "image": "../assets/Expansions/Fire Station/Individual Assets/FireExtinguisher.png", "value": 60},
    "Rubber Ducky": {"chance": 10, "image": "../assets/Individual Assets/Objects/Bathroom/Rubberducky.png", "value": 20},
    "No Loot": {"chance": 35, "image": None},
}

refrigerator_loot_table = {
    "Apple": {"chance": 20, "image": "../assets/Individual Assets/Objects/Kitchen/Apple.png", "value": 5},
    "Bananas": {"chance": 20, "image": "../assets/Individual Assets/Objects/Kitchen/Bananas.png", "value": 5},
    "Orange": {"chance": 20, "image": "../assets/Individual Assets/Objects/Kitchen/Orange.png", "value": 5},
    "Pineapple": {"chance": 10, "image": "../assets/Individual Assets/Objects/Kitchen/Pineapple.png", "value": 15},
    "Ketchup": {"chance": 10, "image": "../assets/Individual Assets/Objects/Kitchen/Bottle_red.png", "value": 10},
    "Mug": {"chance": 5, "image": "../assets/Individual Assets/Objects/Kitchen/Mug.png", "value": 10},
    "No Loot": {"chance": 15, "image": None},
}

wardrobe_loot_table = {
    "Game Controller": {"chance": 12, "image": "../assets/UI/Icons/Game_controller.png", "value": 50},
    "Hammer": {"chance": 5, "image": "../assets/UI/Icons/Hammer.png", "value": 30},
    "Alarm Clock": {"chance": 10, "image": "../assets/Individual Assets/Objects/Bedroom/Alarm_clock_blue.png", "value": 20},
    "Baseball": {"chance": 5, "image": "../assets/Individual Assets/Objects/Bedroom/Baseball.png", "value": 10},
    "Baseball Bat": {"chance": 5, "image": "../assets/Individual Assets/Objects/Bedroom/Baseball_bat.png", "value": 30},
    "Game Console": {"chance": 3, "image": "../assets/Individual Assets/Objects/Bedroom/Game_console.png", "value": 100},
    "PC": {"chance": 5, "image": "../assets/Individual Assets/Objects/Bedroom/PC.png", "value": 200},
    "Poster": {"chance": 5, "image": "../assets/Individual Assets/Objects/Bedroom/Poster_6.png", "value": 15},
    "Skateboard": {"chance": 10, "image": "../assets/Individual Assets/Objects/Bedroom/Skateboard_orange.png", "value": 50},
    "Tennis Racket": {"chance": 4, "image": "../assets/Individual Assets/Objects/Bedroom/Tennis_racket.png", "value": 40},
    "Trophy": {"chance": 3, "image": "../assets/Individual Assets/Objects/Bedroom/Trophy.png", "value": 50},
    "Radio": {"chance": 4, "image": "../assets/Individual Assets/Objects/Living Room/Radio.png", "value": 40},
    "Backpack": {"chance": 14, "image": "../assets/Expansions/Archaeology/Individual Assets/Backpack_large_green.png", "value": 70},
    "Cash": {"chance": 15, "image": "../assets/UI/Icons/Currency.png"},
}

washer_dryer_loot_table = {
    "Santa Hat": {"chance": 30, "image": "../assets/Expansions/Winter 2023/Individual Assets/SantaHat.png", "value": 50},
    "Witch Hat": {"chance": 25, "image": "../assets/Expansions/Halloween/Individual Assets/WitchHat.png", "value": 60},
    "Rubber Ducky": {"chance": 10, "image": "../assets/Individual Assets/Objects/Bathroom/Rubberducky.png", "value": 20},
    "Gear": {"chance": 15, "image": "../assets/UI/Icons/Gear.png", "value": 35},
    "No Loot": {"chance": 20, "image": None},
}

arcade_game_loot_table = {
    "Game Controller": {"chance": 20, "image": "../assets/UI/Icons/Game_controller.png", "value": 50},
    "Cash": {"chance": 30, "image": "../assets/UI/Icons/Currency.png"},
    "Gaming Headset": {"chance": 20, "image": "../assets/Expansions/Gamer Room/Individual Assets/Headset_gaming_green.png", "value": 100},
    "Master Chief Helmet": {"chance": 10, "image": "../assets/Expansions/Gamer Room/Individual Assets/Helmet_gaming.png", "value": 150},
    "No Loot": {"chance": 20, "image": None},
}

bathroom_sink_loot_table = {
    "Rubber Ducky": {"chance": 30, "image": "../assets/Individual Assets/Objects/Bathroom/Rubberducky.png", "value": 20},
    "Shampoo": {"chance": 40, "image": "../assets/Individual Assets/Objects/Bathroom/Shampoo_1.png", "value": 15},
    "Cleaning Soap": {"chance": 20, "image": "../assets/Individual Assets/Objects/Bathroom/Shampoo_2.png", "value": 10},
    "No Loot": {"chance": 10, "image": None},
}

attic_boxes_small_loot_table = {
    "Pottery": {"chance": 25, "image": "../assets/Expansions/Archaeology/Individual Assets/Pottery_ancient_5.png", "value": 70},
    "Stone Tablet": {"chance": 15, "image": "../assets/Expansions/Archaeology/Individual Assets/StoneTablet_black.png", "value": 120},
    "Megalodon Tooth": {"chance": 10, "image": "../assets/Expansions/Archaeology/Individual Assets/MegalodonTooth.png", "value": 200},
    "Neolithic Mask": {"chance": 5, "image": "../assets/Expansions/Archaeology/Individual Assets/NeolithicMask.png", "value": 250},
    "Cash": {"chance": 20, "image": "../assets/UI/Icons/Currency.png"},
    "No Loot": {"chance": 25, "image": None},
}

attic_boxes_large_loot_table = {
    "Backpack": {"chance": 20, "image": "../assets/Expansions/Archaeology/Individual Assets/Backpack_large_green.png", "value": 70},
    "Bucket": {"chance": 15, "image": "../assets/Expansions/Archaeology/Individual Assets/Bucket.png", "value": 20},
    "Blurry Nights": {"chance": 10, "image": "../assets/Expansions/Museum/Individual Assets/Painting_blocky_night.png", "value": 150},
    "Meteorite Piece": {"chance": 10, "image": "../assets/Expansions/Museum/Individual Assets/Meteorite_2.png", "value": 300},
    "Cash": {"chance": 25, "image": "../assets/UI/Icons/Currency.png"},
    "No Loot": {"chance": 20, "image": None},
}

attic_wardrobe_loot_table = {
    "Santa Hat": {"chance": 30, "image": "../assets/Expansions/Winter 2023/Individual Assets/SantaHat.png", "value": 50},
    "Trophy": {"chance": 20, "image": "../assets/Individual Assets/Objects/Bedroom/Trophy.png", "value": 50},
    "Game Console": {"chance": 10, "image": "../assets/Individual Assets/Objects/Bedroom/Game_console.png", "value": 100},
    "Poster": {"chance": 20, "image": "../assets/Individual Assets/Objects/Bedroom/Poster_3.png", "value": 15},
    "No Loot": {"chance": 20, "image": None},
}

desk_loot_table = {
    "Laptop": {"chance": 25, "image": "../assets/Individual Assets/Objects/Bedroom/Laptop.png", "value": 150},
    "Desk Lamp": {"chance": 20, "image": "../assets/Individual Assets/Objects/Bedroom/Desk_lamp.png", "value": 40},
    "Monitor": {"chance": 15, "image": "../assets/Individual Assets/Objects/Bedroom/Monitor.png", "value": 80},
    "Small Monitor": {"chance": 10, "image": "../assets/Individual Assets/Objects/Bedroom/Monitor_small.png", "value": 50},
    "Game Controller": {"chance": 10, "image": "../assets/UI/Icons/Game_controller.png", "value": 50},
    "No Loot": {"chance": 20, "image": None},
}

sidetable_loot_table = {
    "Alarm Clock": {"chance": 20, "image": "../assets/Individual Assets/Objects/Bedroom/Alarm_clock_orange.png", "value": 20},
    "Alarm Clock": {"chance": 15, "image": "../assets/Individual Assets/Objects/Bedroom/Alarm_clock_green.png", "value": 20},
    "Mug": {"chance": 15, "image": "../assets/Individual Assets/Objects/Kitchen/Mug.png", "value": 10},
    "Vase": {"chance": 15, "image": "../assets/Individual Assets/Objects/Living Room/Vase_yellow.png", "value": 30},
    "Cash": {"chance": 20, "image": "../assets/UI/Icons/Currency.png"},
    "No Loot": {"chance": 15, "image": None},
}

door_dresser_loot_table = {
    "Desk Lamp": {"chance": 25, "image": "../assets/Individual Assets/Objects/Bedroom/Desk_lamp.png", "value": 40},
    "Jewelry": {"chance": 20, "image": "../assets/Expansions/Archaeology/Individual Assets/Jewelry_blue.png", "value": 80},
    "Framed Certificate": {"chance": 15, "image": "../assets/Expansions/Fire Station/Individual Assets/FramedCertification.png", "value": 40},
    "Trophy": {"chance": 15, "image": "../assets/Individual Assets/Objects/Bedroom/Trophy.png", "value": 50},
    "Cash": {"chance": 15, "image": "../assets/UI/Icons/Currency.png"},
    "No Loot": {"chance": 10, "image": None},
}

kitchen_cabinet_loot_table = {
    "Cooking Pan": {"chance": 20, "image": "../assets/Individual Assets/Objects/Kitchen/Cooking_pan_2.png", "value": 30},
    "Cooking Pot": {"chance": 15, "image": "../assets/Individual Assets/Objects/Kitchen/Cooking_pot_2.png", "value": 40},
    "Cooking Wok": {"chance": 10, "image": "../assets/Individual Assets/Objects/Kitchen/Cooking_wok.png", "value": 50},
    "Blender": {"chance": 10, "image": "../assets/Individual Assets/Objects/Kitchen/Blender_red.png", "value": 60},
    "Standmixer": {"chance": 15, "image": "../assets/Individual Assets/Objects/Kitchen/Standmixer_red.png", "value": 70},
    "No Loot": {"chance": 30, "image": None},
}

attic_safe_loot_table = {
    "Crown": {"chance": 15, "image": "../assets/Expansions/Archaeology/Individual Assets/Crown.png", "value": 150},
    "Stone Tablet": {"chance": 15, "image": "../assets/Expansions/Archaeology/Individual Assets/StoneTablet_black.png", "value": 120},
    "Jewelry": {"chance": 20, "image": "../assets/Expansions/Archaeology/Individual Assets/Jewelry_purple.png", "value": 100},
    "Cash": {"chance": 25, "image": "../assets/UI/Icons/Currency.png"},
    "No Loot": {"chance": 25, "image": None},
}

shower_loot_table = {
    "Rubber Ducky": {"chance": 30, "image": "../assets/Individual Assets/Objects/Bathroom/Rubberducky.png", "value": 20},
    "Shampoo": {"chance": 40, "image": "../assets/Individual Assets/Objects/Bathroom/Shampoo_1.png", "value": 15},
    "No Loot": {"chance": 30, "image": None},
}

def get_random_loot(loot_table, rolls=1):
    """
    Randomly selects loot based on chances in the loot table.
    Performs the specified number of rolls via chance (1 or 2).
    Default amount of rolls is set to 1.
    """
    
    items = []
    for _ in range(rolls):
        roll = random.randint(1, 100)
        cumulative_chance = 0
        for item, data in loot_table.items():
            cumulative_chance += data["chance"]
            if roll <= cumulative_chance:
                if item != "No Loot":  # Ignore "No Loot" entries
                    # Handle Cash differently since it doesn't have a value
                    if item == "Cash":
                        items.append({"name": item, "image": data["image"], "value": 0})
                    else:
                        items.append({"name": item, "image": data["image"], "value": data["value"]})
                else:
                    print("No loot found.")
                break
    return items

def loot_tables(obj, player, loot_table):
    global looted_objects, looted_objects_id

    object_id = (obj.id, obj.x, obj.y)

    # Prevents an item from being looted twice
    if looted_objects.get(object_id, False):
        print(f"{obj.name} at ({obj.x}, {obj.y}) has already been looted.")
        return

    item_rect = pygame.Rect(obj.x * SCALE, obj.y * SCALE, obj.width * SCALE, obj.height * SCALE)
    if player.rect.colliderect(item_rect):
        rolls = random.choice([1, 2])  # Randomize between 1 and 2 rolls
        if len(player.inventory.playerItems) >= 19: 
            rolls = 1
        
        loot_items = get_random_loot(loot_table, rolls=rolls)
        total_cash = 0  # Track total cash found in this looting session

        for loot in loot_items:
            item_name = loot["name"]
            image_path = loot["image"]
            value = loot["value"]

            if item_name == "Cash":
                if obj.name == "StairSafe":
                    currency_amount = random.randint(150, 250)
                elif obj.name == "Fireplace":
                    currency_amount = random.randint(0, 100)
                else:
                    currency_amount = random.randint(0, 20)

                if currency_amount > 0:
                    total_cash += currency_amount
            else:
                player.inventory.add_item(item_name, image_path, value)
                print(f"Found: {item_name} with value ${value}")

        # Add total cash to the player's inventory
        if total_cash > 0:
            cash_entry = next((entry for entry in player.inventory.playerItems if entry["name"].startswith("Cash")), None)
            if cash_entry:
                # Update existing cash entry
                current_amount_str = cash_entry["name"].split("$")[1].strip(")")
                current_amount = int(current_amount_str)  # Extract current cash amount as an integer
                new_amount = current_amount + total_cash
                cash_entry["name"] = f"Cash (${new_amount})"
                print(f"Updated Cash: ${new_amount}")
            else:
                # Add a new cash entry
                player.inventory.add_item(f"Cash (${total_cash})", "../assets/UI/Icons/Currency.png", value=0)
                print(f"Found Cash: ${total_cash}")

        # Mark the object as looted
        looted_objects_id.append(obj.id)
        looted_objects[object_id] = True
        print(f"{obj.name} marked as looted.")