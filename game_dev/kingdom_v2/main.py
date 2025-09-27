import raylibpy as rl
from blocks import *


class Game:
    def __init__(self):
        size = (1200, 850)
        rl.init_window(size[0], size[1], "DW-World")
        rl.set_target_fps(60)
        
        # self.camera = Camera_r(
        #     rl.Camera2D(
        #         rl.Vector2(
        #             size[0]/2,
        #             size[1]/2,
        #         ),
        #         rl.Vector2(0, 0),
        #         0,
        #         1,
        #     )
        # )
        
        self.level = 1

        self.terrain = Terrain_r(150)
        

    def run(self):


        while not rl.window_should_close():
            self.terrain.Load(self.level)
            
            rl.begin_drawing()

            rl.end_drawing()

        rl.close_window()
    

game = Game()
game.run()