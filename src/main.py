import pygame
import sys
from const import *
from game import *

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.game = Game()

    def mainloop(self):
        # Main loop logic here
        game = self.game
        screen = self.screen

        while True:
            game.show_bg(screen)    
            game.show_pieces(screen)

            for event in pygame.event.get():
                #CLICK
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass
                #MOUSE MOVEMENT    
                elif event.type == pygame.MOUSEMOTION:
                    pass
                #CLICK RELEASE
                elif event.type == pygame.MOUSEBUTTONUP:
                    pass
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()

main = Main()
main.mainloop()