import math
import pygame


def rayCasting(screen, px, py, pa):
    for ray in range(MAX_RAYS):
        angle = (pa - FOV / 2.0) + (ray / MAX_RAYS) * FOV
        ci, si = math.cos(angle), math.sin(angle)
        resD = MAX_DISTANCE
        hitWall = False
        for dist in range(0, MAX_DISTANCE, 2):
            x, y = px + dist * ci, py + dist * si
            if (round(x // TILE), round(y // TILE)) in worldMap:
                resD = dist
                hitWall = True
                break
            elif 0 > x // TILE < mapW or 0 > y // TILE < mapH:
                break
        if hitWall:
            nCeiling = (HEIGHT / 2) - HEIGHT / (resD + 0.1) * 4
            nFloor = HEIGHT - nCeiling
            wallX = ray * (WIDTH // MAX_RAYS)
            clr = 255 - min(round(255 * ((resD // 2) / 100)), 255)

            pygame.draw.line(screen, (clr, clr, clr), (wallX, nCeiling),
                             (wallX, nFloor), (WIDTH // MAX_RAYS))


def drawMap(screen):
    for line in worldMap:
        x, y = line
        pygame.draw.rect(screen, (255, 255, 255), (x * TILE, y * TILE, TILE, TILE))


def createMap():
    global worldMap, mapW, mapH
    MAP = [
        "########################",
        "#......................#",
        "#.....#######..........#",
        "#...##.................#",
        "#...........###........#",
        "#...........#######....#",
        "#..###.................#",
        "#......................#",
        "#..##########..####....#",
        "#......................#",
        "#......########........#",
        "#................###...#",
        "#....#####.............#",
        "########################",
    ]

    for x, i in enumerate(MAP):
        for y, j in enumerate(i):
            if j != ".":
                worldMap[x, y] = (x, y, j)
            mapW, mapH = x, y


WIDTH, HEIGHT = 1000, 650
PX, PY, PA, PSPEED, RSPEED = 30, 30, 0, 2, 0.07
MAX_RAYS, FOV, MAX_DISTANCE = 200, math.pi / 3, 120
TILE = 20
worldMap, mapW, mapH = {}, 0, 0

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
createMap()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
    pressed = pygame.key.get_pressed()
    cx, sy = math.cos(PA) * PSPEED, math.sin(PA) * PSPEED
    if pressed[pygame.K_w]:
        PX += cx
        PY += sy
    if pressed[pygame.K_a]:
        PX += sy
        PY -= cx
    if pressed[pygame.K_s]:
        PX -= cx
        PY -= sy
    if pressed[pygame.K_d]:
        PX -= sy
        PY += cx
    if pressed[pygame.K_LEFT]:
        PA -= RSPEED
    if pressed[pygame.K_RIGHT]:
        PA += RSPEED
    win.fill((104, 104, 104))
    rayCasting(win, PX, PY, PA)

    drawMap(win)
    pygame.draw.circle(win, (0, 255, 255), (PX, PY), 10)

    pygame.display.flip()
    clock.tick(100)
