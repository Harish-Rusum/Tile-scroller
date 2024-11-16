
import pygame
class Menu:
    def __init__(self, surf):
        self.menuOpen = False
        self.surf = surf
        self.overlay = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 200))
        self.holdingEsc = False

        rawButtons = [
            "back.png", "exit.png", "mute.png", "unmute.png", "volUp.png", "volDown.png"
        ]
        self.buttons = [
            pygame.transform.smoothscale(
                pygame.image.load(f"assets/Buttons/{name}").convert_alpha(),
                (118 * 1.5, 16*1.5)
            ) for name in rawButtons
        ]

        self.exit = False
        self.mute = False
        self.buttonStates = [
            (self.buttons[:3] + self.buttons[4:]),
            (self.buttons[:2] + self.buttons[3:])
        ]

        self.muteHeld = False
        self.volUpHeld = False
        self.volDownHeld = False
        self.soundChange = 0

        self.directions = [(dx, dy) for dx in range(-2, 3) for dy in range(-2, 3) if (dx, dy) != (0, 0)]

    def outline(self, img, pos, color=(255, 255, 255)):
        mask = pygame.mask.from_surface(img)
        outline_points = mask.outline()
        for dx, dy in self.directions:
            for x, y in outline_points:
                self.overlay.set_at((pos[0] + x + dx, pos[1] + y + dy), color)

    def click(self, i):
        if i == 0:
            self.menuOpen = False
        elif i == 1:
            self.exit = True
        elif i == 2 and not self.muteHeld:
            self.mute = not self.mute
            self.muteHeld = True
        elif i == 3 and not self.volUpHeld:
            self.soundChange += 0.1
            self.volUpHeld = True
        elif i == 4 and not self.volDownHeld:
            self.soundChange -= 0.1
            self.volDownHeld = True

    def render(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            if not self.holdingEsc:
                self.menuOpen = not self.menuOpen
                self.holdingEsc = True
        else:
            self.holdingEsc = False

        if self.menuOpen:
            self.overlay.fill((0, 0, 0, 200))

            active_buttons = self.buttonStates[self.mute]
            for i, button in enumerate(active_buttons):
                button_x, button_y = 20, (i * 50 + 20)
                button_rect = pygame.Rect(button_x, button_y, button.get_width(), button.get_height())

                if button_rect.collidepoint(mouseX, mouseY):
                    self.outline(button, (button_x, button_y))
                    if pygame.mouse.get_pressed()[0]:
                        self.click(i)
                else:
                    self.outline(button, (button_x, button_y), color=(100, 100, 100))

                self.overlay.blit(button, (button_x, button_y))


            if not pygame.mouse.get_pressed()[0]:
                self.muteHeld = self.volUpHeld = self.volDownHeld = False

            self.surf.blit(self.overlay, (0, 0))
