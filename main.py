import pygame
import random as rand
import time

def ball_start(atrums):
    lenkis = random.uniform(-0.25, 0.25) if random.choice([True, False]) else random.uniform(0.75, 1.25)
    lenkis *= math.pi  #pārvērš uz radiāniem
    vx = atrums*pygame.math.Vector2.normalize(pygame.Vector2(math.cos(lenkis), math.sin(lenkis))).x
    vy = atrums*pygame.math.Vector2.normalize(pygame.Vector2(math.cos(lenkis), math.sin(lenkis))).y
    return (-vx, -vy)
def create_text(text, font, text_color, x, y):
    temp = font.render(text, True, text_color)
    screen.blit(temp, (x, y))

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
score1 = 0
score2 = 0
scored = False
player1_pos = pygame.Vector2(30, screen.get_height() / 2)
player2_pos = pygame.Vector2(screen.get_width() - 50, screen.get_height() / 2)
ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
ball_velo = pygame.Vector2(ball_start(375))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if scored:
        time.sleep(0.5)
        dt -= 0.5
        if ball_pos.x < 100:
            ball_velo = pygame.Vector2(ball_start(375))
        elif ball_pos.x >= 100:
            ball_velo = pygame.Vector2(ball_start(375))
            ball_velo.x *= (-1)
            ball_velo.y *= (-1)
        ball_pos.x = screen.get_width() / 2
        ball_pos.y = screen.get_height() / 2
        scored = False
        
    scored - False
    ball_pos.x += ball_velo.x * dt
    ball_pos.y += ball_velo.y * dt

    if (ball_pos.y >= screen.get_height() - 10) or (ball_pos.y <= 10):
        ball_velo.y *= -1
    if (ball_pos.x <= player1_pos.x+30 and ball_pos.x >= player1_pos.x+20 and player1_pos.y <= ball_pos.y and player1_pos.y+200 >= ball_pos.y) or (ball_pos.x >= player2_pos.x-10 and ball_pos.x <= player2_pos.x and player2_pos.y <= ball_pos.y and player2_pos.y+200 >= ball_pos.y):
        ball_velo.x *= -1
    if ball_pos.x < player1_pos.x+20:
        scored = True
        score2 += 1
    elif ball_pos.x > player2_pos.x:
        scored = True
        score1 += 1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        if player1_pos.y>0:
            player1_pos.y -= 800 * dt
    if keys[pygame.K_s]:
        if player1_pos.y<screen.get_height()-200:
            player1_pos.y += 800 * dt
    if keys[pygame.K_UP]:
        if player2_pos.y>0:
            player2_pos.y -= 800 * dt
    if keys[pygame.K_DOWN]:
        if player2_pos.y<screen.get_height()-200:
            player2_pos.y += 800 * dt

    screen.fill("black")
    pygame.draw.rect(screen, "white", (player1_pos.x, player1_pos.y, 20, 200))
    pygame.draw.rect(screen, "white", (player2_pos.x, player2_pos.y, 20, 200))
    pygame.draw.circle(screen, "white", ball_pos, 10)
    create_text(str(score1), pygame.font.SysFont("Impact", 30), "red", 20, 20)
    create_text(str(score2), pygame.font.SysFont("Impact", 30), "blue", screen.get_width()-40, 20)
    pygame.display.flip()
    dt = clock.tick(120) / 1000

pygame.quit()
