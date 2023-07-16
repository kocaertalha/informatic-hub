import pygame
import os
import random

# Init and Create Window (win)
pygame.init()
win_height = 768
win_width = 1024
win = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()

# Laden und Größe von Bildern
# Held (Spieler)

stationary = pygame.image.load(os.path.join("player.png"))
left = [pygame.transform.flip(pygame.image.load("right2.png"), True, False),
        pygame.transform.flip(pygame.image.load("right2.png"), True, False),pygame.transform.flip(pygame.image.load("right2.png"), True, False),
        pygame.transform.flip(pygame.image.load("right2.png"), True, False),
        pygame.transform.flip(pygame.image.load("right2.png"), True, False),
        pygame.transform.flip(pygame.image.load("right2.png"), True, False),pygame.transform.flip(pygame.image.load("right2.png"), True, False),
        pygame.transform.flip(pygame.image.load("right2.png"), True, False),
        pygame.transform.flip(pygame.image.load("right3.png"), True, False),
        pygame.transform.flip(pygame.image.load("right3.png"), True, False), pygame.transform.flip(pygame.image.load("right3.png"), True, False),
        pygame.transform.flip(pygame.image.load("right3.png"), True, False),
        pygame.transform.flip(pygame.image.load("right3.png"), True, False),
        pygame.transform.flip(pygame.image.load("right3.png"), True, False),
        pygame.transform.flip(pygame.image.load("right3.png"), True, False),
        pygame.transform.flip(pygame.image.load("right3.png"), True, False)]

right = [pygame.image.load("right2.png"),pygame.image.load("right2.png"), pygame.image.load("right2.png"),pygame.image.load("right2.png"),
         pygame.image.load("right2.png"),pygame.image.load("right2.png"), pygame.image.load("right2.png"),pygame.image.load("right2.png"),
         pygame.image.load("right3.png"),pygame.image.load("right3.png"), pygame.image.load("right3.png"),pygame.image.load("right3.png"),
         pygame.image.load("right3.png"), pygame.image.load("right3.png"), pygame.image.load("right3.png"),
         pygame.image.load("right3.png")]


# Feind


bullet_img = pygame.transform.scale(pygame.image.load(os.path.join("bullet.png")), (35, 35))
background = pygame.transform.scale(pygame.image.load(os.path.join("background.png")), (win_width, win_height))

class Hero:
    def __init__(self, x, y):
        # Walk
        self.x = x
        self.y = y
        self.velx = 10
        self.vely = 10
        self.face_right = True
        self.face_left = False
        self.stepIndex = 0
        # Jump
        self.jump = False
        # Bullet
        self.bullets = []
        self.cool_down_count = 0
        #Health
        self.hitbox = (self.x, self.y, 64, 180)
        self.health = 30
        self.lives = 1
        self.alive = True
        #Scrolling
        self.viewpoint = [0,0]

    def move_hero(self, userInput):
        if userInput[pygame.K_RIGHT] and self.x <= win_width - 62:
            self.x += self.velx
            self.face_right = True
            self.face_left = False
        elif userInput[pygame.K_LEFT] and self.x >= 0:
            self.x -= self.velx
            self.face_right = False
            self.face_left = True
        else:
            self.stepIndex = 0

    def draw(self, win):
        self.hitbox = (self.x, self.y, 64, 180)

        pygame.draw.rect(win, (255, 0, 0), (self.x + 15, self.y - 15, 30, 7))
        if self.health >= 0:
            pygame.draw.rect(win, (153, 250, 0), (self.x + 15, self.y - 15, self.health, 7))
        if self.stepIndex >= 9:
            self.stepIndex = 0
        if self.face_left:
            win.blit(left[self.stepIndex], (self.x, self.y))
            self.stepIndex += 1
        if self.face_right:
            win.blit(right[self.stepIndex], (self.x, self.y))
            self.stepIndex += 1

    def jump_motion(self, userInput):
        if userInput[pygame.K_SPACE] and self.jump is False:
            self.jump = True
        if self.jump:
            self.y -= self.vely*4
            self.vely -= 1
        if self.vely < -10:
            self.jump = False
            self.vely = 10

    def direction(self):
        if self.face_right:
            return 1
        if self.face_left:
            return -1

    def cooldown(self):
        if self.cool_down_count >= 10: #more time between shots
            self.cool_down_count = 0
        elif self.cool_down_count > 0:
            self.cool_down_count += 1

    def shoot(self):
        self.hit()
        self.cooldown()
        if (userInput[pygame.K_f] and self.cool_down_count == 0):
            bullet = Bullet(self.x, self.y, self.direction())
            self.bullets.append(bullet)
            self.cool_down_count = 1
        for bullet in self.bullets:
            bullet.move()
            if bullet.off_screen():
                self.bullets.remove(bullet)

    def hit(self):
        for enemy in enemies:
            for bullet in self.bullets:
                if enemy.hitbox[0] < bullet.x < enemy.hitbox[0] + enemy.hitbox[2] and enemy.hitbox[1] < bullet.y < enemy.hitbox[1] + enemy.hitbox[3]:
                    enemy.health -= 10
                    player.bullets.remove(bullet)

# controll character´s speed and change the background photos)

    def walk(self, facing):
        if self.stepIndex == 0:
            self.stepIndex += 1
            # time punkt
            self.walking_timer = pygame.time.get_ticks()
        else:
            # Compare time changes and current character's speed
            if (pygame.time.get_ticks() - self.walking_timer >
                    self.calculate_animation_speed()):
                self.stepIndex += 1
                self.walking_timer = pygame.time.get_ticks()
        if facing == 'right':
            if self.stepIndex > 3:
                self.stepIndex = 0
        if facing == 'left':
            if self.stepIndex > 8:
                self.stepIndex = 5
            if self.stepIndex < 5:
                self.stepIndex = 5

        # calculate speed

    def calculate_animation_speed(self):
        if self.velx == 0:
            animation_speed = 130
        elif self.velx > 0:
            animation_speed = 130 - (self.velx * 12)
        else:
            animation_speed = 130 - (self.velx * 12 * -1)

        # First define the position movement rules of the camera, namely self.viewpoint
        if self.x < self.viewpoint[0]+ 15:
            self.x -= self.velx
        if self.velx > 0:
            if self.x > 1024 * 0.55 + self.viewpoint[0]:
                # 1.1 This coefficient is added for the smoothness of the screen later
                self.viewpoint[0] += int(self.velx * 1.1)
        # self.viewpoint is a rectangle whose parameters change based on character's movement
        win.blit(background, (0, 0), (self.viewpoint[0], self.viewpoint[1]))

class Bullet:
    def __init__(self, x, y, direction):
        self.x = x + 15
        self.y = y + 25
        self.direction = direction

    def draw_bullet(self):
        win.blit(bullet_img, (self.x, self.y))

    def move(self):
        if self.direction == 1:
            self.x += 20
        if self.direction == -1:
            self.x -= 20

    def off_screen(self):
        return not (self.x >= 0 and self.x <= win_width)

    def hit(selfs):
        if player.hitbox[0] < enemy.x + 32 < player.hitbox[0] + player.hitbox[2] and player.hitbox[1] < enemy.y + 32 <player.hitbox[1] + player.hitbox[3]:
            player.health -= 5



c1 = pygame.image.load("corona1.png")
c1 = pygame.transform.scale(c1, (91, 149))

c2 = pygame.image.load("corona2.png")
c2 = pygame.transform.scale(c2, (91, 149))

c3 = pygame.image.load("corona3.png")
c3 = pygame.transform.scale(c3, (91, 149))

###########klausur#############

#right_enemy = [pygame.transform.scale(pygame.image.load("klausur11.png"), (91, 149)), pygame.transform.scale(pygame.image.load("klausur12.png"), (91, 149))]

#left_enemy = [pygame.transform.scale(pygame.image.load("klausur21.png"), (91, 149)), pygame.transform.scale(pygame.image.load("klausur22.png"), (91, 149))]

###############################

left_enemy = [c2, c3]

right_enemy = [pygame.transform.flip(c2, True, False), pygame.transform.flip(c3, True, False)]

class Enemy:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.schrittindex = 0
        #Health
        self.hitbox = (self.x, self.y, 64, 180)
        self.health = 30
        self.steps = 0


    def step(self):
        if self.schrittindex >= 16:
            self.schrittindex = 0

    def draw(self, win):
        self.hitbox = (self.x, self.y, 64, 180)
        pygame.draw.rect(win, (255, 0, 0), (self.x + 15, self.y - 15, 30, 7))
        if self.health >= 0:
            pygame.draw.rect(win, (153, 250, 0), (self.x + 15, self.y - 15, self.health, 7))

        self.step()
        if self.direction == left:
            win.blit(left_enemy[self.schrittindex//8], (self.x, self.y))
        if self.direction == right:
            win.blit(right_enemy[self.schrittindex//8], (self.x, self.y))
        self.schrittindex += 1

    def move(self):
        self.hit()
        if self.direction == left:
            self.x -= 1
        if self.direction == right:
            self.x += 1

    def hit(self):
        if player.hitbox[0] < enemy.x + 32 < player.hitbox[0] + player.hitbox[2] and player.hitbox[1] < enemy.y + 32 < player.hitbox[1] + player.hitbox[3]:
            if player.health >0:
                player.health -= 1
                if player.health == 0 and player.lives > 0:
                    player.lives -= 1
                    player.health = 30
                elif player.health == 0 and player.lives == 0:
                    player.alive = False

    def off_screen(self):
        return not (self.x >= -50 and self.x <= win_width)
# Draw Game
def draw_game():
    win.fill((255, 255, 255))
    win.blit(background, (0,0))
    # Draw Player
    player.draw(win)
    #Draw Bullet
    for bullet in player.bullets:
        bullet.draw_bullet()
    #Draw Enemies
    for enemy in enemies:
        enemy.draw(win)
        # Player Health
        if player.alive == False:
            win.fill((0, 0, 0))
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render('You Died! Press R to restart', True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (win_width // 2, win_height // 2)
            win.blit(text, textRect)
            if userInput[pygame.K_r]:
                player.alive = True
                player.lives = 1
                player.health = 30

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Lives: ' + str(player.lives), True, (0, 0, 0))
    win.blit(text, (650, 20))
    #Delay and Update
    clock.tick(60)
    pygame.display.update()

# Instance of Hero-Class
player = Hero(250, 280)

#Instance of Enemy-Class
enemies = []

# Mainloop
run = True
while run:

    # Quit Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Input
    userInput = pygame.key.get_pressed()

    # Shoot
    player.shoot()

    # Movement
    player.move_hero(userInput)
    player.jump_motion(userInput)

    #####scrolling
    player.walk(left)
    player.calculate_animation_speed()
    ######


    #Enemy
    if len(enemies) == 0:
        rand_nm = random.randint(0 ,1)
        if rand_nm == 1:
            enemy = Enemy(700, 300, left)
            enemies.append(enemy)
        if rand_nm == 0:
            enemy = Enemy(50, 300, right)
            enemies.append(enemy)
    for enemy in enemies:
        enemy.move()
        if enemy.off_screen() or enemy.health == 0:
            enemies.remove(enemy)


    # Draw Game in Window
    draw_game()