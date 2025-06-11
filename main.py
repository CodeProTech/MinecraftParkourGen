from mcpi.minecraft import Minecraft
from mcpi import block
from random import randint, choice
import time


class ParkourGenerator:
    def __init__(self, length=15, level=1):
        self.mc = Minecraft.create()
        self.blocks = [
            block.STONE.id,
            block.WOOD.id,
            block.WOOL.id,
            block.SANDSTONE.id
        ]
        self.level = level
        self.length = length
        self.spawn_x = 0
        self.spawn_y = 100
        self.spawn_z = 0
        self.max_jump_height = 1
        self.goal_x = 0
        self.goal_y = 0
        self.goal_z = 0

        # Level-specific configurations
        self.level_config = {
            1: {"gap": 2, "height": 1, "side_step": 1},  # Easiest
            2: {"gap": 2, "height": 1, "side_step": 2},
            3: {"gap": 3, "height": 1, "side_step": 2},
            4: {"gap": 3, "height": 1, "side_step": 3},
            5: {"gap": 3, "height": 1, "side_step": 3, "special": "ladder"},
            6: {"gap": 3, "height": 1, "side_step": 4, "special": "ladder"},
            7: {"gap": 4, "height": 1, "side_step": 3, "special": "all"},
            8: {"gap": 4, "height": 1, "side_step": 4, "special": "all"},
            9: {"gap": 4, "height": 1, "side_step": 4, "special": "all"},
            10: {"gap": 4, "height": 1, "side_step": 5, "special": "all"}  # Hardest
        }

    def set_spawnpoint(self, x, y, z):
        self.spawn_x = x
        self.spawn_y = y
        self.spawn_z = z
        self.mc.setBlock(x, y - 1, z, block.GOLD_BLOCK.id)
        for dx, dz in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            self.mc.setBlock(x + dx, y - 1, z + dz, block.GLOWSTONE_BLOCK.id)

    def create_ladder(self, x, y, z):
        # Create a ladder block pattern
        self.mc.setBlock(x, y, z, block.LADDER.id, 2)  # 2 is the data value for ladder facing north
        self.mc.setBlock(x, y + 1, z, block.LADDER.id, 2)
        self.mc.setBlock(x, y + 2, z + 1, block.STONE.id)  # Platform at top of ladder

    def create_thin_bridge(self, x, y, z, length):
        # Create a thin bridge using fence blocks
        for i in range(length):
            self.mc.setBlock(x + i, y, z, block.FENCE.id)

    def teleport_to_spawn(self):
        self.mc.player.setPos(self.spawn_x + 0.5, self.spawn_y, self.spawn_z + 0.5)

    def clear_area(self):
        x, y, z = self.spawn_x, self.spawn_y, self.spawn_z
        self.mc.setBlocks(x - 20, y - 10, z - 20,
                          x + 100, y + 20, z + 20,
                          block.AIR.id)

    def generate(self, length, width, height, level):
        self.set_spawnpoint(0, 100, 0)

        # Start platform
        for dx in range(-1, 2):
            for dz in range(-1, 2):
                self.mc.setBlock(self.spawn_x + dx, self.spawn_y - 1, self.spawn_z + dz, block.STONE.id)

        current_x = self.spawn_x
        current_y = self.spawn_y - 1
        current_z = self.spawn_z

        config = self.level_config[level]
        x_step = config["gap"]
        max_side_step = config["side_step"]

        for i in range(length):
            next_x = current_x + x_step
            side_range = min(max_side_step, i + 1)
            next_z = current_z + randint(-side_range, side_range)

            height_change = randint(-1, config["height"])
            next_y = current_y + height_change
            next_y = max(self.spawn_y - 4, min(next_y, self.spawn_y + 2))

            # Special features based on level
            if "special" in config:
                if config["special"] == "ladder" or (config["special"] == "all" and randint(1, 10) == 1):
                    self.create_ladder(next_x, next_y, next_z)
                    current_y = next_y + 2  # Adjust height for ladder top
                elif config["special"] == "all" and randint(1, 10) == 2:
                    self.create_thin_bridge(next_x, next_y, next_z, 2)
                else:
                    block_type = choice(self.blocks)
                    self.mc.setBlock(next_x, next_y, next_z, block_type)
                    self.mc.setBlock(next_x, next_y - 1, next_z, block.GLOWSTONE_BLOCK.id)
            else:
                block_type = choice(self.blocks)
                self.mc.setBlock(next_x, next_y, next_z, block_type)
                self.mc.setBlock(next_x, next_y - 1, next_z, block.GLOWSTONE_BLOCK.id)

            current_x = next_x
            current_y = next_y
            current_z = next_z

        # Goal platform
        self.goal_x = current_x
        self.goal_y = current_y
        self.goal_z = current_z

        for dx in range(-1, 2):
            for dz in range(-1, 2):
                if dx == 0 and dz == 0:
                    self.mc.setBlock(current_x + dx, current_y, current_z + dz, block.GOLD_BLOCK.id)
                else:
                    self.mc.setBlock(current_x + dx, current_y, current_z + dz, block.DIAMOND_BLOCK.id)
                self.mc.setBlock(current_x + dx, current_y - 1, current_z + dz, block.GLOWSTONE_BLOCK.id)

    def check_goal(self, pos):
        x_match = self.goal_x - 1.3 <= pos.x <= self.goal_x + 1.3
        y_match = self.goal_y - 0.5 <= pos.y <= self.goal_y + 1
        z_match = self.goal_z - 1.3 <= pos.z <= self.goal_z + 1.3
        return x_match and y_match and z_match

    def setup(self):
        self.clear_area()
        time.sleep(0.5)
        self.generate(self.length, 3, 1, self.level)
        time.sleep(0.5)
        self.teleport_to_spawn()


def main():
    mc = Minecraft.create()
    current_level = 1
    generator = ParkourGenerator(length=15, level=current_level)

    def check_chat():
        for chat in mc.events.pollChatPosts():
            try:
                level = int(chat.message)
                if 1 <= level <= 10:
                    return level
            except ValueError:
                pass
        return None

    mc.postToChat("§6Welcome to Parkour Generator!")
    mc.postToChat("§eType a number 1-10 in chat to select difficulty level")
    generator.setup()

    falls = 0
    last_fall_time = 0
    goal_reached = False
    last_goal_check = 0

    while True:
        time.sleep(0.1)

        # Check for level change requests
        new_level = check_chat()
        if new_level and new_level != current_level:
            current_level = new_level
            generator = ParkourGenerator(length=15, level=current_level)
            mc.postToChat(f"§aChanging to difficulty level {current_level}")
            generator.setup()
            falls = 0
            goal_reached = False

        pos = generator.mc.player.getPos()
        current_time = time.time()

        if pos.y < 85 and (current_time - last_fall_time) > 2:
            falls += 1
            last_fall_time = current_time
            goal_reached = False

            generator.mc.postToChat(f"§cFall #{falls}! Regenerating parkour...")
            generator.setup()
            time.sleep(1)

        if not goal_reached and (current_time - last_goal_check) > 0.5:
            last_goal_check = current_time
            if generator.check_goal(pos):
                goal_reached = True
                generator.mc.postToChat("§6§l⭐ CONGRATULATIONS! ⭐")
                generator.mc.postToChat("§a§lYou reached the goal!")
                generator.mc.postToChat(f"§e§lTotal falls: {falls}")
                time.sleep(2)
                generator.mc.postToChat("Generating new parkour...")
                generator.setup()
                goal_reached = False


if __name__ == "__main__":
    main()
