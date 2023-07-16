import pygame, sys
from pygame.locals import *
import random

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Computer Science: College Overload")
s_height = 768
s_width = 1024
screen = pygame.display.set_mode((s_width, s_height))
background = pygame.image.load("background.png")

font_name = 'alagard.ttf'

menu_pic = pygame.image.load("menu.png")

door_sound = pygame.mixer.music.load("door.mp3")

def draw_text(text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, False, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

############################### TILES ######################################

block_img = pygame.image.load("block.png")
TILE_SIZE = block_img.get_width()

################################ MAIN MENU #################################

def mainMenu():
    click = False
    while True:
        screen.blit(menu_pic, (0,0))
        start_button = pygame.Rect(s_width / 2 - 100, s_height / 2 - 120, 200, 40,)
        credits_button = pygame.Rect(s_width / 2 - 100, s_height / 2 - 70, 200, 40)
        pygame.draw.rect(screen, (242,222,217), start_button)
        pygame.draw.rect(screen, (242,222,217), credits_button)

        draw_text("Main menu", 70, s_width / 2, 100)
        draw_text("Start", 50, s_width / 2, s_height / 2 - 100)
        draw_text("Credits", 50, s_width / 2, s_height / 2 - 50)


        mouse_x, mouse_y = pygame.mouse.get_pos()

        if start_button.collidepoint((mouse_x, mouse_y)):
            if click:
                game_loop()

        if credits_button.collidepoint((mouse_x, mouse_y)):
            if click:
                credits()

        #click = False

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == KEYDOWN:

                if event.key ==  pygame.K_ESCAPE:
                    exit_esc()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


        pygame.display.update()
        clock.tick(60)


############################### EXIT MENU #################################

def exit_esc():
    escape = True
    while escape:
        screen.fill((255, 255, 255))
        draw_text("Are you sure you want to quit?", 60, s_width / 2, 320)
        draw_text("Press 'Y' if yes, press 'N' if not", 40, s_width / 2, s_height / 2 + 50)
        event = pygame.event.wait()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == pygame.K_n:
                escape = False
            if event.key == pygame.K_y:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)

############################### CREDITS MENU ###############################

def credits():
    cr = True
    while cr:
        screen.fill((255, 255, 255))
        draw_text("Credits", 60, s_width / 2, 270)
        draw_text("MADE BY GROUP 8", 40, s_width / 2, s_height / 2 )
        draw_text("Meng Zhang", 40, s_width / 2, s_height / 2 + 40)
        draw_text("Mehmet Talha Kocaer", 40, s_width / 2, s_height / 2 + 80)
        draw_text("Elizaveta Khamzina", 40, s_width / 2, s_height / 2 + 120)
        draw_text("Anton Okruzhnov", 40, s_width / 2, s_height / 2 + 160)
        event = pygame.event.wait()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainMenu()

        pygame.display.update()
        clock.tick(60)

############################### PLAYER ################################

left1 = pygame.transform.flip(pygame.image.load("right1.png"), True, False)
left2 = pygame.transform.flip(pygame.image.load("right2.png"), True, False)
left3 = pygame.transform.flip(pygame.image.load("right3.png"), True, False)

left = [pygame.transform.scale(left1, (51, 174)), pygame.transform.scale(left2, (60, 175)),
        pygame.transform.scale(left1, (51, 174)), pygame.transform.scale(left3, (49, 174))]


right1 = pygame.image.load("right1.png")
right2 = pygame.image.load("right2.png")
right3 = pygame.image.load("right3.png")

right = [pygame.transform.scale(right1, (51, 174)), pygame.transform.scale(right2, (60, 174)),
         pygame.transform.scale(right1, (51, 174)), pygame.transform.scale(right3, (49, 174))]

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.image = pygame.image.load("player.png")
        #self.image = pygame.transform.scale(self.image, (25, 87))
        self.image2 = pygame.image.load("right1.png")
        #self.image2 = pygame.transform.scale(self.image, (25, 87))
        self.image3 = pygame.transform.flip(pygame.image.load("right1.png"), True, False)
        #self.image3 = pygame.transform.scale(self.image, (25, 87))
        self.rect = self.image2.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.movex = 0
        self.movey = 0
        self.vely = 0

        self.jump = False
        self.ground = False
        self.stepIndex = 0
        self.face_z = False
        self.face_right = True
        self.face_left = False
        ###d
        self.powerup_speed = False
        self.powerup_speed_timer = 0
        self.powerup_count = 0
        #
        self.bullets = []
        self.cool_down_count = 0
        # Health
        self.hitbox = (self.rect.x, self.rect.y, 64, 180)
        self.health = 30
        self.lives = 1
        self.alive = True

    def update(self):
        self.dx = 0
        self.dx1 = 0

        self.hitbox = (self.rect.x, self.rect.y, 64, 180)

        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x + 15, self.rect.y - 15, 30, 7))
        if self.health >= 0:
            pygame.draw.rect(screen, (153, 250, 0), (self.rect.x + 15, self.rect.y - 15, self.health, 7))

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
            if self.powerup_speed:
                self.dx1 -= 13
                self.face_z = False
                self.face_right = False
                self.face_left = True
            else:
                self.dx1 -= 7
                self.face_z = False
                self.face_right = False
                self.face_left = True
        elif pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
            if self.powerup_speed:
                self.dx += 13
                self.face_z = False
                self.face_right = True
                self.face_left = False
            else:
                self.dx += 7
                self.face_z = False
                self.face_right = True
                self.face_left = False
        else:
            self.stepIndex = 0
            if pressed [pygame.K_s]:
                self.face_z = True
                self.face_right = False
                self.face_left = False


        self.rect.x += self.dx
        self.rect.x += self.dx1

        if self.rect.x <= 1:
            self.rect.x = 0
        if self.rect.x >= 961:
            self.rect.x = 960

        if self.stepIndex >= 16:
            self.stepIndex = 0
        if self.face_z:
            screen.blit(self.image, self.rect)
        if self.face_right:
            screen.blit(right[self.stepIndex//4], (self.rect.x, self.rect.y))
            self.stepIndex += 1
        if self.face_left:
            screen.blit(left[self.stepIndex//4], (self.rect.x, self.rect.y))
            self.stepIndex += 1

    def jump_move(self):
        self.movey += self.vely
        self.vely += 10
        if self.vely > 30:
            self.vely = 30
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE] or pressed[pygame.K_UP]:
            if self.jump == False:
                print(self.jump)
                self.vely = -40
                #self.jump = True
        if self.rect.y < -150:
            self.vely = 0
            self.rect.y += 5

    def powerup_use(self):
        self.powerup_speed = True
        self.powerup_speed_timer = 300
        self.powerup_count = 1

    def get_hits(self, tiles):
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits

    def checkCollisionsx(self, tiles):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.face_right:  # moving right
                self.rect.right  = tile.left - 10
                collision_types['right'] = True
            elif self.face_left:  # moving left
                self.rect.left = tile.right + 10
                collision_types['left'] = True

    def checkCollisiony(self, tiles):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.rect.y += self.movey
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.movey > 0:
                self.rect.bottom = tile.top
                collision_types['bottom'] = True
                self.vely = 0
            elif self.movey < 0:
                self.jump = False
                print(self.jump)
                self.rect.top = tile.bottom
                collision_types['top'] = True
                self.ground = True

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
        self.hit1()
        self.hit2()
        self.cooldown()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_q] and self.cool_down_count == 0 and not self.face_z:
            bullet = Bullet(self.rect.x, self.rect.y, self.direction())
            self.bullets.append(bullet)
            self.cool_down_count = 1
        for bullet in self.bullets:
            bullet.move()
            if bullet.off_screen():
                self.bullets.remove(bullet)

    def hit1(self):
        for enemy in enemies:
            for bullet in self.bullets:
                if enemy.hitbox[0] < bullet.x < enemy.hitbox[0] + enemy.hitbox[2] and enemy.hitbox[1] < bullet.y < enemy.hitbox[1] + enemy.hitbox[3]:
                    enemy.health -= 5
                    player.bullets.remove(bullet)

    def hit2(self):
        if player.hitbox[0] < enemy.x + 32 < player.hitbox[0] + player.hitbox[2] and player.hitbox[1] < enemy.y + 32 < player.hitbox[1] + player.hitbox[3]:
            if player.health > 0:
                player.health -= 1
                if player.health == 0 and player.lives > 0:
                    player.lives -= 1
                    player.health = 30
                elif player.health == 0 and player.lives == 0:
                    player.alive = False


player = Player(50,465)

################################ ENEMY ####################################

c1 = pygame.image.load("corona1.png")
c1 = pygame.transform.scale(c1, (91, 149))

c2 = pygame.image.load("corona2.png")
c2 = pygame.transform.scale(c2, (91, 149))

c3 = pygame.image.load("corona3.png")
c3 = pygame.transform.scale(c3, (91, 149))

###########klausur#############

right_enemy = [pygame.transform.scale(pygame.image.load("klausur11.png"), (91, 149)), pygame.transform.scale(pygame.image.load("klausur12.png"), (91, 149))]

left_enemy = [pygame.transform.scale(pygame.image.load("klausur21.png"), (91, 149)), pygame.transform.scale(pygame.image.load("klausur22.png"), (91, 149))]

###############################

#left_enemy = [c2, c3]

#right_enemy = [pygame.transform.flip(c2, True, False), pygame.transform.flip(c3, True, False)]

class Enemy:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.schrittindex = 0
        #Health
        self.hitbox = (self.x, self.y, 64, 180)
        self.health = 30
        self.steps_left = 200
        self.steps_right = 200


    def step(self):
        if self.schrittindex >= 16:
            self.schrittindex = 0

    def draw(self, screen):
        self.hitbox = (self.x, self.y, 64, 180)
        pygame.draw.rect(screen, (255, 0, 0), (self.x + 15, self.y - 15, 30, 7))
        if self.health >= 0:
            pygame.draw.rect(screen, (153, 250, 0), (self.x + 15, self.y - 15, self.health, 7))
        if self.health <= 0:
            self.x = 2000

    def move(self):
        self.hit()
        self.step()
        if self.direction == left and self.steps_left > 0:
            self.x -= 2
            self.steps_left  -= 1
            screen.blit(left_enemy[self.schrittindex // 8], (self.x, self.y))
        else:
             if self.direction == left:
                 self.steps_right = 200
                 self.direction = right
        if self.direction == right and self.steps_right > 0:
            self.x += 2
            self.steps_right -= 1
            screen.blit(right_enemy[self.schrittindex // 8], (self.x, self.y))
        else:
            if self.direction == right:
                self.steps_left = 200
                self.direction = left
        self.schrittindex += 1


    def hit(self):
        if player.hitbox[0] < enemy.x + 32 < player.hitbox[0] + player.hitbox[2] and player.hitbox[1] < enemy.y + 32 < player.hitbox[1] + player.hitbox[3]:
            if player.health > 0:
                player.health -= 1
                if player.health == 0 and player.lives > 0:
                    player.lives -= 1
                    player.health = 30
                elif player.health == 0 and player.lives == 0:
                    player.alive = False

    def off_screen(self):
        return not (self.x >= -50 and self.x <= s_width)

################################ POWER UP #################################

cup3 = pygame.image.load("cup3.png")
cup2 = pygame.image.load("cup2.png")
cup1 = pygame.image.load("cup1.png")
coffee_animation = [pygame.transform.scale(cup1, (44, 56)), pygame.transform.scale(cup2, (44, 56)), pygame.transform.scale(cup3, (44, 56)), pygame.transform.scale(cup2, (44, 56))]

class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.image = pygame.image.load("cup1.png")
        self.image = pygame.transform.scale(self.image, (44, 56))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animation = 0
        self.running = True

    def update(self):
        #screen.blit(self.image, self.rect)
        screen.blit(coffee_animation[self.animation // 9], (self.rect.x, self.rect.y))
        if self.animation >= 32:
            self.animation = 0
        self.animation += 1


powerup = Powerup(300, 580)

################################ COLLECTIBLES ##################################

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.image = pygame.image.load("book.png")
        self.image = pygame.transform.scale(self.image, (80, 57))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.count_up = 0
        self.count_down = 0


    def update(self):
        screen.blit(self.image, self.rect)
        #if self.count_up <= 60:
            #self.rect.y -= 0.1
            #self.count_up += 1
        #if self.count_up > 60:
            #if self.count_down <= 60:
            #self.rect.y += 60





collectible1 = Collectible(400, 320)
collectible2 = Collectible(600, 120)
collectible3 = Collectible(800, 570)

############################## EXIT DOOR ####################################

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.image = pygame.image.load("door.jpg")
        self.image = pygame.transform.scale(self.image, (96, 192))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        screen.blit(self.image, self.rect)


door = Door(900, 450)

########################### BULLET ###########################################

bullet0 = pygame.transform.scale(pygame.image.load("one.png"), (20, 20))
bullet1 = pygame.transform.scale(pygame.image.load("zero.png"), (20, 20))
bullet_list = [bullet0, bullet1]

class Bullet:
    def __init__(self, x, y, direction):
        self.x = x + 15
        self.y = y + 40
        self.direction = direction
        self.image = bullet_list[random.randint(0,1)]

    def draw_bullet(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        if self.direction == 1:
            self.x += 20
        if self.direction == -1:
            self.x -= 20

    def off_screen(self):
        return not (self.x >= 0 and self.x <= s_width)

    def hit(selfs):
        if player.hitbox[0] < enemy.x + 32 < player.hitbox[0] + player.hitbox[2] and player.hitbox[1] < enemy.y + 32 < \
                player.hitbox[1] + player.hitbox[3]:
            player.health -= 5

########################### CONTROLS MENU ####################################

def controls():
    con = True
    while con:
        screen.fill((255, 255, 255))
        draw_text("Controls", 60, s_width / 2, 100)
        draw_text("E to interact with the doors", 40, s_width / 2, s_height / 2 - 80)
        draw_text("Q to shoot enemies", 40, s_width / 2, s_height / 2 - 40)
        draw_text("A or left arrow to go left", 40, s_width / 2, s_height / 2)
        draw_text("D or right arrow to go right", 40, s_width / 2, s_height / 2 + 40)
        draw_text("Space or up arrow to jump", 40, s_width / 2, s_height / 2 + 80)
        draw_text("Esc to go back to main menu", 40, s_width / 2, s_height / 2 + 120)
        draw_text("Press any key to continue", 30, s_width / 2, s_height / 2 + 180)
        event = pygame.event.wait()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            con = False

        pygame.display.update()
        clock.tick(60)

################################# WINNING ##########################

def winning():
    win = True
    endA = pygame.image.load("endA.png")
    endB = pygame.image.load("endB.png")
    endC = pygame.image.load("endC.png")
    endD = pygame.image.load("endD.png")
    endF = pygame.image.load("endF.png")
    while win:
        if collected < 9:
            pygame.mixer.music.load("bad end.mp3")
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play()
            screen.blit(endF, (0, 0))
        if 9 == collected < 12:
            screen.blit(endD, (0, 0))
        if 12 <= collected <= 14:
            screen.blit(endC, (0, 0))
        if 15 <= collected <= 17:
            screen.blit(endB, (0, 0))
        if collected > 17:
            screen.blit(endA, (0, 0))
        event = pygame.event.wait()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainMenu()

        pygame.display.update()
        clock.tick(60)


############################## LOSING ################################

def gameover():
    pygame.mixer.music.load("bad end.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play()
    lost = True
    while lost:
        screen.fill((255, 255, 255))
        draw_text("GAME OVER", 60, s_width / 2, 320)
        draw_text("Press Esc to go back to main menu", 40, s_width / 2, 400)
        event = pygame.event.wait()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainMenu()

        pygame.display.update()
        clock.tick(60)

############################## GAME LOOP ##############################

enemies = []

def game_loop():
    level_time = 5400
    block_img = pygame.image.load("block.png")

    TILE_SIZE = block_img.get_width()
    level1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
           [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]

    level2 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0],
              [0, 0, 2, 2, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0, 0],
              [0, 0, 0, 2, 0, 2, 0, 2, 0, 2, 0, 0, 2, 0, 0, 0],
              [0, 0, 2, 0, 0, 2, 0, 2, 0, 2, 2, 0, 2, 2, 2, 2],
              [0, 2, 2, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
              [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]

    level3 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
              [0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 2, 0, 0, 2],
              [0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0],
              [0, 0, 2, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 2, 0],
              [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
              [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]

    level4 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 2, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0],
              [0, 0, 0, 2, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 2, 2, 2, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0],
              [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0],
              [0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
              [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]

    level5 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 2, 2, 2, 2, 0],
              [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
              [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]

    level6 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
            [2, 2, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]

    controls()
    running = True
    player.rect.x = 150
    #player.rect.y = 400
    player.health = 30
    player.alive = True
    player.lives = 1
    enemy.health = 30
    enemy.x = 700
    powerup.rect.x = 400
    collectible1.rect.x = 250
    collectible2.rect.x = 800
    collectible3.rect.x = 600
    global collected
    collected = 0

    map = [level1, level2, level3, level4, level5, level6]

    level_number = 0

    while running:

        screen.blit(background, (0, 0))

        ###
        tiles = []
        ty = 0
        for row in map[level_number]:
            tx = 0
            for tile in row:
                if tile == 2:
                    screen.blit(block_img, (tx * TILE_SIZE, ty * TILE_SIZE))
                if tile != 0:
                    tiles.append(pygame.Rect(tx * TILE_SIZE, ty *TILE_SIZE, TILE_SIZE, TILE_SIZE))
                tx +=1
            ty += 1

        ###
        door.update()
        powerup.update()
        player.update()
        player.jump_move()
        player.get_hits(tiles)
        player.checkCollisionsx(tiles)
        player.checkCollisiony(tiles)
        player.direction()
        player.movey = 0

        collectible1.update()
        collectible2.update()
        collectible3.update()

        for bullet in player.bullets:
            bullet.draw_bullet()


        enemy.draw(screen)
        enemy.move()
        ####### Player Health ######
        if player.lives == 1:
            screen.blit(pygame.transform.scale(pygame.image.load("heart.png"), (40, 40)), (940, 0))
            screen.blit(pygame.transform.scale(pygame.image.load("heart.png"), (40, 40)), (980, 0))
        elif player.lives == 0:
            screen.blit(pygame.transform.scale(pygame.image.load("heart.png"), (40, 40)), (940, 0))

        if player.alive == False:
            gameover()

        player.shoot()

        #### draw in-game interface ####
        powerup_rect = pygame.Rect(0, 0, 200, 40)
        collected_rect = pygame.Rect(0, 40, 220, 40)
        timer_rect = pygame.Rect(440, 5, 120, 60)
        pygame.draw.rect(screen, (174, 133, 255), powerup_rect)
        pygame.draw.rect(screen, (180, 153, 255), collected_rect)
        pygame.draw.rect(screen, (180, 153, 255), timer_rect)
        draw_text("Powerups: " + str(player.powerup_count), 30, 100, 20)
        draw_text("Collected: " + str(collected) + "/18", 30, 110, 60)
        draw_text(str(level_time // 3600) + ":" + str((level_time - 3600*(level_time//3600))//60), 60, 500, 40)

        # timer for level
        if level_time >= 0:
            level_time -= 1
        if level_time < 0:
            gameover()
            mainMenu()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu = True
                    while menu:
                        screen.fill((255, 255, 255))
                        draw_text("Want to quit to main menu?", 60, s_width / 2, 320)
                        draw_text("Press 'Y' if yes, press 'N' if not", 40, s_width / 2, s_height / 2 + 50)
                        event = pygame.event.wait()
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == KEYDOWN:
                            if event.key == pygame.K_n:
                                menu = False
                            if event.key == pygame.K_y:
                                mainMenu()

                        pygame.display.update()
                        clock.tick(60)

        if pygame.Rect.colliderect(player.rect, powerup.rect):
            powerup.rect.x = 2000
            pygame.mixer.music.load("powerup.wav")
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play()
            powerup.running = False
            player.powerup_use()

        if pygame.Rect.colliderect(player.rect, collectible1.rect):
            collectible1.rect.x = 2000
            collected = collected + 1
            pygame.mixer.music.load("book.wav")
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play()
            print(collected)
        if pygame.Rect.colliderect(player.rect, collectible2.rect):
            collectible2.rect.x = 2000
            collected = collected + 1
            pygame.mixer.music.load("book.wav")
            pygame.mixer.music.play()
            print(collected)
        if pygame.Rect.colliderect(player.rect, collectible3.rect):
            collectible3.rect.x = 2000
            collected = collected + 1
            pygame.mixer.music.load("book.wav")
            pygame.mixer.music.play()
            print(collected)

        if pygame.Rect.colliderect(player.rect, door.rect):
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_e]:
                pygame.mixer.music.load("door.mp3")
                pygame.mixer.music.play()
                level_number += 1
                player.rect.x = 50
                enemy.health = 30
                enemy.x = 700
                if level_number == 1:
                    collectible1.rect.y = 120
                    collectible1.rect.x = 180
                    collectible2.rect.x = 510
                    collectible2.rect.y = 200
                    collectible3.rect.x = 920
                    collectible3.rect.y = 220
                    powerup.rect.x = 300
                    enemy.x = 400
                if level_number == 2:
                    collectible1.rect.y = 60
                    collectible1.rect.x = 300
                    collectible2.rect.x = 430
                    collectible2.rect.y = 230
                    collectible3.rect.x = 760
                    collectible3.rect.y = 60
                    powerup.rect.x = 300
                    enemy.x = 400
                if level_number == 3:
                    collectible1.rect.y = 250
                    collectible1.rect.x = 100
                    collectible2.rect.x = 620
                    collectible2.rect.y = 320
                    collectible3.rect.x = 820
                    collectible3.rect.y = 60
                    powerup.rect.x = 600
                if level_number == 4:
                    collectible1.rect.y = 10
                    collectible1.rect.x = 60
                    collectible2.rect.x = 250
                    collectible2.rect.y = 190
                    collectible3.rect.x = 820
                    collectible3.rect.y = 120
                    powerup.rect.x = 500
                if level_number == 5:
                    collectible1.rect.y = 70
                    collectible1.rect.x = 0
                    collectible2.rect.x = 620
                    collectible2.rect.y = 260
                    collectible3.rect.x = 330
                    collectible3.rect.y = 580
                    powerup.rect.x = 450
                    enemy.x = 900
                if level_number == 6:
                    winning()

        pygame.display.update()
        clock.tick(60)

        #timer for power-up
        if player.powerup_speed_timer >=0:
            player.powerup_speed_timer -= 1
        if player.powerup_speed_timer <= 0:
            player.powerup_speed = False
            player.powerup_count = 0


    #if you exit to main menu from game loop, it will show winning screen!!!! changes are needed
    mainMenu()

enemy = Enemy(600, 490, left)
enemies.append(enemy)
enemy.move()
if enemy.health <= 0:
    pygame.mixer.music.load("enemy.wav")
    pygame.mixer.music.play()
    enemy.x = 2000
    enemies.remove(enemy)


mainMenu()
