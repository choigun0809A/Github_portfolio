import pygame
import player as pl

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((850, 850))
        pygame.display.set_caption("Project Tower")
        self.clock = pygame.time.Clock()
        self.load()

    def main(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.action()
            self.screen.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
    
    def load(self):
        self.player = pl.Player()

    def action(self):
        self.player.Move()

    def draw(self):
        self.player.Draw(self.screen)

Game().main()
