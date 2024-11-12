import pygame
import sys
from scripts.tilemap import Grid
from scripts.player import Player
from scripts.cursor import Cursor
from utils.fov import Overlay
from levels.asdas import matrix

pygame.init()

TileSize = 35
ViewX, ViewY = 20, 15
TilesX, TilesY = 40, 40
ScreenX, ScreenY = TileSize * ViewX, TileSize * ViewY
Fps = 60
Black = "#000000"

screen = pygame.display.set_mode((ScreenX, ScreenY))
pygame.display.set_caption("Tile Grid System")
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
grid = Grid(TilesX, TilesY, TileSize, matrix, ScreenX, ScreenY)
mousefov = Overlay(ScreenX, ScreenY, 250, [ScreenX // 2, ScreenY // 2])
player = Player(0, 0, TileSize, TileSize)
cursor = Cursor()

def main():
    running = True
    while running:
        screen.fill(Black)

        right = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        jump = False
        if keys[pygame.K_a]:
            right = -1
        elif keys[pygame.K_d]:
            right = 1
        else:
            right = 0

        if keys[pygame.K_w]:
            jump = True
        else:
            jump = False

        screen.fill("#000000")        
        grid.render(screen)

        player.update(right,grid,screen,jump=jump)

        mouseX,mouseY = pygame.mouse.get_pos()
        mousefov.render(screen,[mouseX,mouseY])

        cursor.render(screen)
        pygame.display.flip()
        clock.tick(Fps)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
