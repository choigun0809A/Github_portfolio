import raylibpy as rl
from perlin_noise import PerlinNoise
import numpy as np


class Tile_r:
    def __init__(
            self,
            rect: rl.Rectangle = rl.Rectangle(0, 0, 1, 1),
            texture: rl.Texture = None,
        ):
        self.rect = rect
        self.img = texture
        

class Camera_r:
    def __init__(
            self,
            camera: rl.Camera2D
        ):
        self.camera = camera
        self.shake_active = False
        self.shake_range = 4
        self.shake_durration = 200
        


class Terrain_r:
    def __init__(self, size: int):
        self.Tile_maps: dict[int, list[int]] = {}
        self.size = size
        self.octi = 2
        self.zoom = 200
        self.block_size = 3
        # self.camera: rl.Camera2D = camera
        self.loaded = True

    def Load(self, target_level):
        if target_level > len(self.Tile_maps):
            self.loaded = False
            x, y = self.size*self.block_size/2, self.size*self.block_size/2
            # self.camera.target = rl.Vector2(x, y)
        
        if not self.loaded:
            self.Get_map(target_level)
    
    def Get_map(self, target_level):
        noise = PerlinNoise(self.octi, target_level)
        self.Tile_maps[target_level] = np.zeros((self.size, self.size))

        for y in range(self.size):
            for x in range(self.size):
                num = (noise([x / self.zoom, y / self.zoom]) + 1) / 2 * 255
                self.Tile_maps[target_level][y][x] = num

                rl.begin_drawing()
                # rl.begin_mode2d(self.camera)
                rl.draw_rectangle(
                    x * self.block_size,
                    y * self.block_size,
                    self.block_size,
                    self.block_size,
                    rl.Color(num, num, num, 255) 
                )
                # rl.end_mode2d()
                rl.end_drawing()
                


        



        