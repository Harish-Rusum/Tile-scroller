from scripts.enemy import Enemy
from scripts.tilemap import Grid

from levels.level1 import matrix as level1
from levels.level2 import matrix as level2

from copy import deepcopy

class LevelManager:
    def __init__(self, screen):
        self.levels = {
            1: {
                "enemies": [Enemy((240, 520), (240, 360), 1, "right")],
                "matrix": level1,
                "goal": (760, 320),
            },
            2: {
                "enemies": [Enemy((440, 240), (440, 560), 1, "right")],
                "matrix": level2,
                "goal": (760, 400),
            },
        }
        self.currentLevel = 1
        self.tileSize = 40
        self.viewX, self.viewY = 20, 15
        self.tilesX, self.tilesY = 40, 40
        self.screenX, self.tilesY = self.tileSize * self.viewX, self.tileSize * self.viewY
        self.screen = screen
        self.grid = None
        self.enemies = []
        self.goal = None
        self.loadLevel(self.currentLevel)

    def resetLevel(self):
        self.loadLevel(self.currentLevel)

    def loadLevel(self, level):
        levelData = self.levels.get(level)
        if not levelData:
            return
        self.grid = Grid(self.tilesX, self.tilesY, self.tileSize, levelData["matrix"], self.screenX, self.tilesY)
        self.enemies = deepcopy(levelData["enemies"])
        self.goal = levelData["goal"]

    def nextLevel(self):
        if self.currentLevel+1 in self.levels:
            self.loadLevel(self.currentLevel+1)
            self.currentLevel += 1
        else:
            self.resetLevel()