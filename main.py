import pygame
import random
import sys
from scripts.levelManager import LevelManager
from scripts.player import Player
from scripts.cursor import Cursor
from utils.fov import Overlay
from utils.menu import Menu
from utils.timer import Timer

pygame.init()
pygame.mixer.init()

TileSize = 40
ViewX, ViewY = 20, 15
ScreenX, ScreenY = TileSize * ViewX, TileSize * ViewY
Fps = 60
Black = "#000000"

display = pygame.display.set_mode((ScreenX, ScreenY))
screen = pygame.surface.Surface((ScreenX,ScreenY))
pygame.display.set_caption("Tile Grid System")
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

lManager = LevelManager(screen)
player = Player(TileSize, TileSize, 1, 0, 360)
cursor = Cursor()
fov = Overlay(ScreenX, ScreenY, 200, [ScreenX // 2, ScreenY // 2])
timer = Timer(ScreenX, ScreenY)
pygame.mixer.music.load("assets/Music/bgm.mp3")
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.2)


def main():
    running = True
    pauseMenu = False
    holdingEsc = False
    menu = Menu(screen)
    renderOffset = [0,0]
    screenShake = False
    screenShakeTimer = 0.5
    global lManager
    while running:
        screen.fill(Black)
        right = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        jump = keys[pygame.K_w] or keys[pygame.K_k] or keys[pygame.K_UP]

        if keys[pygame.K_a] or keys[pygame.K_h] or keys[pygame.K_LEFT]:
            right = -1
        elif keys[pygame.K_d] or keys[pygame.K_l] or keys[pygame.K_RIGHT]:
            right = 1

        if keys[pygame.K_ESCAPE]:
            if not holdingEsc:
                holdingEsc = True
                pauseMenu = not pauseMenu
        else:
            holdingEsc = False

        screen.fill(Black)
        lManager.grid.render(screen)
        player.render(screen)

        if menu.exit:
            running = False
        if not menu.menuOpen:
            player.update(right, lManager.grid, screen, lManager.enemies, jump=jump)
            for enemy in lManager.enemies:
                if enemy.deadTime <  0.5:
                    if enemy.deadTime != 0:
                        screenShake = True
                enemy.update(screen)

            timer.tick(screen)

            if not menu.mute:
                pygame.mixer.music.set_volume(0.2 + menu.soundChange)
            else:
                pygame.mixer.music.set_volume(0.0 + menu.soundChange)

            if lManager.goal[0] <= player.x <= lManager.goal[1] and lManager.goal[2] <= player.y <= lManager.goal[3]:
                lManager.nextLevel()
                player.reset()
                menu.reset = True
        else:
            if not menu.mute:
                pygame.mixer.music.set_volume(0.5 + menu.soundChange)
            else:
                pygame.mixer.music.set_volume(0.0)

        if menu.reset:
            player.reset()
            lManager.resetLevel()
            timer.reset()
            menu.reset = False

        fov.render(screen, [player.x + player.img.get_width() // 2, player.y + player.img.get_height() // 2])
        timer.render(screen)
        menu.render()
        cursor.render(screen)

        if screenShake:
            renderOffset[0] = random.randint(0,8) - 4
            renderOffset[1] = random.randint(0,8) - 4
            screenShakeTimer -= 0.5

        if screenShakeTimer <= 0:
            screenShake = False
            screenShakeTimer = 2
            renderOffset = [0,0]

        display.blit(screen,renderOffset)
        pygame.display.flip()
        clock.tick(Fps)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
