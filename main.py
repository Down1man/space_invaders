import pygame
import os
import random

pygame.font.init()

WIDTH, HEIGHT = 750, 750
OKNO = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space invaders")

#zmiennea
FPS = 60
PLAYER_WIDTH, PLAYER_HEIGHT = 60, 60
ENEMY_WIDTH, ENEMY_HEIGHT = 50, 50
PLAYER_MS = 5
MAX_KUL = 5
KULE_MS = 7
YELLOW = (255, 255, 0)
wrogow = 5
ENEMY_MS = 1
ZYCIA = pygame.USEREVENT + 1
FONT = pygame.font.SysFont("comicsans", 30)
WHITE = (255, 255, 255)
ENEMY_HIT = pygame.USEREVENT + 2
ENEMY_KULE_MS = 5
GREEN = (0, 255, 0)
PLAYER_HIT = pygame.USEREVENT + 3
SHIP_DESTROYED = pygame.USEREVENT + 4

#grafiki
PLAYER_SHIP_IMAGE = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
RED_SHIP_IMAGE = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SHIP_IMAGE = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SHIP_IMAGE = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

PLAYER_SHIP = pygame.transform.scale(PLAYER_SHIP_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT))
RED_SHIP = pygame.transform.rotate(pygame.transform.scale(RED_SHIP_IMAGE, (ENEMY_WIDTH, ENEMY_HEIGHT)), 180)
GREEN_SHIP = pygame.transform.rotate(pygame.transform.scale(GREEN_SHIP_IMAGE, (ENEMY_WIDTH, ENEMY_HEIGHT)), 180)
BLUE_SHIP = pygame.transform.rotate(pygame.transform.scale(BLUE_SHIP_IMAGE, (ENEMY_WIDTH, ENEMY_HEIGHT)), 180)
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

def wypelnianie(player, player_kule, wrogowie, zycia, enemy_kule, player_zycia, ship_destroyed):
    OKNO.blit(BG, (0, 0))
    OKNO.blit(PLAYER_SHIP, (player.x, player.y))
    ZYCIA_TEXT = FONT.render("Zycia: " + str(zycia), True, WHITE)
    PLAYER_ZYCIA_TEXT = FONT.render("Zycia Gracza: " + str(player_zycia), True, WHITE)
    OKNO.blit(ZYCIA_TEXT, (WIDTH-ZYCIA_TEXT.get_width() - 10, 10))
    OKNO.blit(PLAYER_ZYCIA_TEXT, (10, 10))
    ENEMY_DESTROYED = FONT.render("Zniszczone statki: " + str(ship_destroyed), True, WHITE)
    OKNO.blit(ENEMY_DESTROYED, (WIDTH//2 - ENEMY_DESTROYED.get_width() + 200, 10))

    for kule in player_kule:
        pygame.draw.rect(OKNO, YELLOW, kule)

    for wrog in wrogowie:
        OKNO.blit(GREEN_SHIP, (wrog.x, wrog.y))

    for shot in enemy_kule:
        pygame.draw.rect(OKNO, GREEN, shot)

    pygame.display.update()

def player_movement(key_pressed, player):
    if key_pressed[pygame.K_a] and player.x - PLAYER_MS > 0:
        player.x -= PLAYER_MS
    if key_pressed[pygame.K_d] and player.x + PLAYER_MS + PLAYER_WIDTH < WIDTH:
        player.x += PLAYER_MS
    if key_pressed[pygame.K_w] and player.y - PLAYER_MS > 0:
        player.y -= PLAYER_MS
    if key_pressed[pygame.K_s] and player.y + PLAYER_MS + PLAYER_HEIGHT < HEIGHT:
        player.y += PLAYER_MS


def fizyka(player_kule, wrogowie, kula, enemy_kule, player):
    for kula in player_kule:
        kula.y -= KULE_MS
        if kula.y < 0:
            player_kule.remove(kula)

    for wrog in wrogowie:
        wrog.y += ENEMY_MS
        if kula.colliderect(wrog):
            wrogowie.remove(wrog)
            pygame.event.post(pygame.event.Event(SHIP_DESTROYED))
            #player_kule.remove(kula)
        if wrog.y > HEIGHT:
            pygame.event.post(pygame.event.Event(ZYCIA))
            wrogowie.remove(wrog)

    for shot in enemy_kule:
        shot.y += ENEMY_KULE_MS
        if shot.colliderect(player):
            pygame.event.post(pygame.event.Event(PLAYER_HIT))
            enemy_kule.remove(shot)
        if shot.y >= HEIGHT:
            enemy_kule.remove(shot)

def koniec(text):
    finito = FONT.render(text, True, GREEN)
    OKNO.blit(finito, (WIDTH//2 - finito.get_width()/2, HEIGHT//2 - finito.get_width()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    player = pygame.Rect(WIDTH//2, HEIGHT-PLAYER_HEIGHT - 20, PLAYER_WIDTH, PLAYER_HEIGHT)
    kula = pygame.Rect(player.x + player.width // 2, player.y + 2, 5, 10)

    wrogowie = []
    player_kule = []
    enemy_kule = []

    zycia = 10
    player_zycia = 5
    ship_destroyed = 0

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(player_kule) < MAX_KUL:
                    kula = pygame.Rect(player.x + player.width//2, player.y + 2, 5, 10)
                    player_kule.append(kula)

            for wrog in range(0, wrogow):
                if len(wrogowie) <= wrogow:
                    green = pygame.Rect(random.randint(0, WIDTH - ENEMY_WIDTH), -2, ENEMY_WIDTH, ENEMY_HEIGHT)
                    wrogowie.append(green)
                    for x in wrogowie:
                        shot = pygame.Rect(green.x, green.y, 5, 10)
                        enemy_kule.append(shot)


            if event.type == ZYCIA:
                zycia -= 1

            if event.type == PLAYER_HIT:
                player_zycia -= 1

            if event.type == SHIP_DESTROYED:
                ship_destroyed += 1

            end = ""
            if zycia <= 0:
                end = "Do Twojej bazy dostalo sie zbyt wielu wrogow"
            elif player_zycia <= 0:
                end = "Zostales zniszczony"
            elif ship_destroyed > 10:
                end = "Udalo Ci sie odeprzec atak!"
            if end != "":
                koniec(end)
                run = False

        key_pressed = pygame.key.get_pressed()

        #funkcje
        wypelnianie(player, player_kule, wrogowie, zycia, enemy_kule, player_zycia, ship_destroyed)
        player_movement(key_pressed, player)
        fizyka(player_kule, wrogowie, kula, enemy_kule, player)

    pygame.quit()

main()