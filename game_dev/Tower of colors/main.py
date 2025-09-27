import pyray as rl
import raylib as rll
import pixels

class Game:
    def __init__(self):
        rl.init_window(1200, 850, "Tower Of colors")
        rl.set_target_fps(60)

        self.player = pixels.Player(
            rl.Vector2(50, 50),
            rl.Color(10, 200, 255, 255)
        )
    
    def main(self):
        
        while not rl.window_should_close():

            rl.begin_drawing()
            rl.clear_background(rl.BLACK)
            self.action()
            self.draw()
            rl.end_drawing()
            print(rl.get_fps(), self.enem.want)
        rl.close_window()
    
    def action(self):
        self.player.move()
        self.enem.behave(self.player.rect)


    def draw(self):
        self.player.draw()
        self.enem.draw()

Game().main()