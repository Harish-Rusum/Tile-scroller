import pygame
from utils.spritesheet import SpriteSheet

class Player:
    def __init__(self, x, y, playerX, playerY):
        self.rotation = -1
        self.x = x
        self.y = y
        self.state = 0
        self.spriteSheet = SpriteSheet()
        self.sheet = self.spriteSheet.split("assets/Characters/sheet.png", 1, 4, 24, 24)
        self.frame = 0
        self.animationFrames = 4
        self.direction = 0
        self.counter = 0
        self.playerX = playerX
        self.playerY = playerY
        self.img = self.sheet[self.frame]
        self.img = pygame.transform.smoothscale(self.img, (self.playerX, self.playerY))
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.acc = 0.4
        self.decc = 0.2
        self.maxspeed = 4
        self.xVel = 0
        self.yVel = 0
        self.gravityAcc = 0.45
        self.terminalVel = 8
        self.jumpStrength = -8
        self.jumping = False
        self.coyoteTime = 0.15
        self.coyoteTimer = 0

    def render(self, surf):
        img = self.sheet[self.frame]
        img = pygame.transform.smoothscale(img, (self.playerX, self.playerY))
        if self.direction == -1:
            img = pygame.transform.rotate(img, -180)
            img = pygame.transform.flip(img, False, True)
        surf.blit(img, (self.x, self.y))

    def gravity(self, grid):
        if not self.jumping:
            self.yVel = min(self.yVel + self.gravityAcc, self.terminalVel)
        
        self.rect.y += self.yVel
        self.jumping = False

        surrounding = grid.getSurroundingTiles(self.x, self.y)
        for element in surrounding:
            tileRect = pygame.Rect(element[2][0], element[2][1], grid.tileSize, grid.tileSize)
            if element[0][0] != -1 and self.rect.colliderect(tileRect):
                if self.yVel > 0:
                    self.rect.bottom = tileRect.top
                    self.jumping = True
                    self.coyoteTimer = self.coyoteTime
                elif self.yVel < 0:
                    self.rect.top = tileRect.bottom
                self.yVel = 0
                break

        self.y = self.rect.y
        if not self.jumping:
            self.coyoteTimer = max(0, self.coyoteTimer - 1 / 60)  # Decrease timer if in air

    def jump(self):
        if self.jumping or self.coyoteTimer > 0:
            self.yVel = self.jumpStrength
            self.jumping = False
            self.coyoteTimer = 0

    def moveX(self, dx, grid):
        if dx != 0:
            self.xVel += self.acc * dx
            self.xVel = max(-self.maxspeed, min(self.xVel, self.maxspeed))
        else:
            if self.xVel > 0:
                self.xVel = max(self.xVel - self.decc, 0)
            elif self.xVel < 0:
                self.xVel = min(self.xVel + self.decc, 0)

        if dx > 0:
            self.direction = 0
        elif dx < 0:
            self.direction = -1

        if self.counter % 10 == 0:
            self.frame = (self.frame + 1) % self.animationFrames
        self.counter += 1

        newX = self.x + self.xVel
        self.rect.x = newX
        surrounding = grid.getSurroundingTiles(self.x, self.y)
        for element in surrounding:
            tileRect = pygame.Rect(element[2][0], element[2][1], grid.tileSize, grid.tileSize)
            if element[0][0] != -1 and self.rect.colliderect(tileRect):
                if self.xVel > 0:
                    self.rect.right = tileRect.left
                elif self.xVel < 0:
                    self.rect.left = tileRect.right
                self.xVel = 0
                break
        self.x = self.rect.x

    def update(self, dx, grid, screen, jump=False):
        self.render(screen)
        self.moveX(dx, grid)
        self.gravity(grid)
        if jump:
            self.jump()
