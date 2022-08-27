import pygame
import os
import sys
pygame.font.init()
pygame.mixer.init()
pygame.init()
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
pygame.display.set_caption("niggas in space")
START_BTN = pygame.image.load(os.path.join('ass', 'start_btn.png')).convert_alpha()
EXIT_BTN = pygame.image.load(os.path.join('ass', 'exit_btn.png')).convert_alpha()
BORDER = pygame.Rect(445, 0, 10, 500)
BULLET_SOUND = pygame.mixer.Sound(os.path.join('ass', 'Gun+Silencer.mp3'))
BULLET_COLL_SOUND = pygame.mixer.Sound(os.path.join('ass', 'Grenade+1.mp3'))
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
YELLOW_HIT = pygame.USEREVENT+1
RED_HIT = pygame.USEREVENT+2
YELLOW_SPACESHIP_img = pygame.image.load(os.path.join('ass','spaceship_yellow.png'))
RED_SPACESHIP_img = pygame.image.load(os.path.join('ass','spaceship_red.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame .transform.scale(YELLOW_SPACESHIP_img,(55,55)),90)
RED_SPACESHIP = pygame.transform.rotate(pygame .transform.scale(RED_SPACESHIP_img,(55,55)),270)
VEL = 5
bullet_vel = 7
MAX_BULLETS = 4
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('ass','space.png')),(WIDTH, HEIGHT))


def draw_window(red,yellow, y_bullets, r_bullets, r_health, y_health):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, (0, 0, 0),BORDER)
    r_health_txt = HEALTH_FONT.render("Health: " + str(r_health), True, (255, 255, 255))
    y_health_txt = HEALTH_FONT.render("Health: " + str(y_health), True, (255, 255, 255))
    WIN.blit(r_health_txt, (WIDTH - r_health_txt.get_width() - 10, 10))
    WIN.blit(y_health_txt, (10, 10))
    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x,red.y))
    for bullet in r_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for bullet in y_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_move(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x-VEL > 0:  # yellow spaceship
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x+VEL < 400:
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y-VEL > 0:
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y+VEL < 450:
        yellow.y += VEL


def red_move(key_pressed, red):
    if key_pressed[pygame.K_LEFT] and red.x-VEL > 450:  # red spaceship
        red.x -= VEL
    if key_pressed[pygame.K_RIGHT] and red.x+VEL < 850:
        red.x += VEL
    if key_pressed[pygame.K_UP] and red.y-VEL > 0:
        red.y -= VEL
    if key_pressed[pygame.K_DOWN] and red.y+VEL < 445:
        red.y += VEL


def bullet_collision(y_bullets, r_bullets, yellow, red):
    for bullet in y_bullets:
        bullet.x += bullet_vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            y_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            y_bullets.remove(bullet)

    for bullet in r_bullets:
        bullet.x -= bullet_vel
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            r_bullets.remove(bullet)
        elif bullet.x < 0:
            r_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, True, (255, 255, 255))
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


def main_menu():
    class Button:
        def __init__(self, image, x_pos, y_pos, text_input):
            self.image = image
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
            self.text_input = text_input
            self.text = HEALTH_FONT.render(self.text_input, True, "white")
            self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

        def update(self):
            WIN.blit(self.image, self.rect)
            WIN.blit(self.text, self.text_rect)

        def checkForInput(self, position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                              self.rect.bottom):
                main()

        def changeColor(self, position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                              self.rect.bottom):
                self.text = HEALTH_FONT.render(self.text_input, True, "green")
            else:
                self.text = HEALTH_FONT.render(self.text_input, True, "white")

    button_surface = pygame.image.load(os.path.join('ass', 'start_btn.png'))
    button_surface = pygame.transform.scale(button_surface, (300, 150))

    button = Button(button_surface, 450, 250, " ")

    while True:
        pygame.display.set_caption("Main Menu")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                button.checkForInput(pygame.mouse.get_pos())

        WIN.blit(SPACE, (0,0))
        text2 = "Niggas in Space"
        d_text = WINNER_FONT.render(text2, True, (255, 0, 0))
        WIN.blit(d_text, (100, 0))
        button.update()
        button.changeColor(pygame.mouse.get_pos())

        pygame.display.update()


def main():
    red = pygame.Rect(700,300,55,55)
    yellow = pygame.Rect(100,300,55,55)
    y_bullets = []
    r_bullets = []
    r_health = 10
    y_health = 10
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LALT and len(y_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    y_bullets.append(bullet)

                    BULLET_SOUND.play()
                if event.key == pygame.K_RALT and len(r_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    r_bullets.append(bullet)
                    BULLET_SOUND.play()

            if event.type == RED_HIT:
                r_health -= 1
                BULLET_COLL_SOUND.play()
            if event.type == YELLOW_HIT:
                y_health -= 1
                BULLET_COLL_SOUND.play()
        winner = ""
        if r_health <= 0:
            winner = "Yellow wins!"
        if y_health <= 0:
            winner = "Red wins!"
        if winner != "":
            draw_winner(winner)
            main_menu()
        key_pressed = pygame.key.get_pressed()
        yellow_move(key_pressed, yellow)
        red_move(key_pressed, red)
        bullet_collision(y_bullets, r_bullets, yellow, red)
        draw_window(red, yellow, r_bullets, y_bullets, r_health, y_health)
    main()


if __name__ == "__main__":
    main_menu()
