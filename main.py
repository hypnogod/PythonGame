import pygame
import os
import random

# MAIN FUNCTION: main()
# INITIAL MENU: menu()
# FUNCTION FOR Drawing TEXT: drawText()
# FUNCTION FOR health bar: drawHealthBar()
# FUNCTION WHEN game ends: gameEnd()

# LIST OF CLASS:
#       1) Player
#       2) Explosion
#       3) Missile

# SETTINGS
# THE HEIGHT AND WIDTH OF THE SCREEN/APPLICATION
WIDTH, HEIGHT = 500, 600

# FPS (frames per second) controller
FPS = 60


# colors
# Add Color Variable Here (R, G, B)
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
YELLOW = pygame.Color(255, 255, 0)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)

# INITALIZE
pygame.init()

# set up display window
# (width, height)
# NOTE: NEEDS TO BE A VARIABLE
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

# optional (name of the window)
# LOOK AT THE TOP BAR TO SEE THE CHANGE
pygame.display.set_caption("GAME")

# FPS (frames per second) controller
timer = pygame.time.Clock()

# TYPE OF FONT
fontName = pygame.font.match_font('dejavuserif')

# DEF DRAW SOME TEXT


def drawText(screen, TXT_String, TXTsize, x, y):
    font = pygame.font.Font(fontName, TXTsize)
    TXTWindow = font.render(TXT_String, True, WHITE)
    # render(text, antialias, color)
    # The antialias argument is a boolean: if true the characters will have smooth edges.
    # This creates a new Surface with the specified text rendered on it.
    text_rect = TXTWindow.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(TXTWindow, text_rect)
    # draw one image onto another

# DRAW HEALTH BAR


def drawHealthBar(surface, x, y, health):
    BAR_LENGTH, BAR_HEIGHT = 100, 10
    pct = max(health, 0)
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)

# WHEN GAME ENDS


def gameEnd():
    waiting = True
    # WHILE LOOP TO MAKE SURE TEXT DOES NOT CLOSE INSTANTLY
    while waiting:
        eventPoll = pygame.event.poll()
        # Returns a single event from the queue.
        if eventPoll.type == pygame.KEYDOWN:
            if eventPoll.key == pygame.K_q:
                pygame.quit()
                quit()  # Does not give you error when you quit
        elif eventPoll.type == pygame.QUIT:
            pygame.quit()
            # WHEN YOU CLOSE THE WINDOW IT WILL CLOSE
            # IF YOU DON'T HAVE THIS IT MIGHT NOT CLOSE
            quit()
        else:
            WINDOW.fill(BLACK)
            # SET BACKGROUND COLOR

            # INSTRUCTIONS
            drawText(WINDOW, "GAME ENDED", 30, WIDTH/2, (HEIGHT/2)-20)
            drawText(WINDOW, "Press [Q] To Quit", 30, WIDTH/2, (HEIGHT/2)+40)

            # YOU WILL NEED TO UPDATE TO SEE THE CHANGES
            pygame.display.update()

# Menu


def menu():
    while True:
        eventPoll = pygame.event.poll()
        if eventPoll.type == pygame.KEYDOWN:
            if eventPoll.key == pygame.K_RETURN:
                # BREAKS THE WHILE LOOP
                break
            elif eventPoll.key == pygame.K_q:
                pygame.quit()
                quit()
        elif eventPoll.type == pygame.QUIT:
            pygame.quit()
            quit()
        else:
            WINDOW.fill(BLACK)
            drawText(WINDOW, "Press [ENTER] To Begin",
                     30, WIDTH/2, (HEIGHT/2)-20)
            drawText(WINDOW, "or [Q] To Quit", 30, WIDTH/2, (HEIGHT/2)+40)
            pygame.display.update()
    WINDOW.fill(BLACK)  # TO HIDE THE PREVIOUS TEXTS
    drawText(WINDOW, "GET READY!", 40, WIDTH/2, HEIGHT/2)
    pygame.display.update()


# IMAGES

# IMAGE OF A SPACESHIP
PLAYER_IMG = pygame.image.load(os.path.join('Assets', 'spaceship.png'))
# IMAGE OF THE MISSILES THAT IS DROPPING DOWN
MISSLE_IMG = pygame.image.load(os.path.join('Assets', 'missile.png'))

# GIVES YOU ARRAY OF IMAGES INSIDE OF EXPLOSION FOLDER
EXPLOSION_IMGS = [pygame.image.load(os.path.join('Explosions', images)).convert_alpha()
                  for images in os.listdir('Explosions')]

# EXPLOSION SOUND
EXPLOSION_SOUND = pygame.mixer.Sound(
    os.path.join('Assets', 'explosionSOUND.wav'))


class Player(pygame.sprite.Sprite):
    # Simple base class for visible game objects.
    # def __init__(self) IS IMPORTANT WHEN USING CLASS
    def __init__(self):
        # pygame.sprite.Sprite.__init__(self) is required by Pygame - it runs the built-in Sprite classes initializer.
        pygame.sprite.Sprite.__init__(self)

        # SCALE DOWN THE SIZE OF THE SPACESHIP/PLAYER
        self.image = pygame.transform.scale(PLAYER_IMG, (50, 38))

        #
        self.rect = self.image.get_rect()
        #  to create a rectangle USING THAT SURFACE.
        self.rect.bottom = HEIGHT - 10
        self.rect.centerx = WIDTH / 2

        self.speedx = 0
        # CHARACTER SPEED

        self.health = 100
        # HEALTH BAR
        # IF YOU CHANGE THE HEALTH, ALSO CHANGE THE HEALTH DAR FUNCTION

        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        # Pygame creates a new rect with the size of the image and the x, y coordinates (0, 0).

    def update(self):
        # unhide
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 30

        keys_pressed = pygame.key.get_pressed()
        # Sprite Movement
        if keys_pressed[pygame.K_LEFT]:
            self.speedx = -5
        elif keys_pressed[pygame.K_RIGHT]:
            self.speedx = 5

        # check for the borders
        # WE DO NOT WANT TO LET THE PLAYER GO OUTSIDE THE WINDOW
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        self.rect.x += self.speedx

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


class Missile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(
            pygame.transform.scale(MISSLE_IMG, (30, 50)), 180)
        # scale(Surface/IMAGE, (width, height))
        self.image.set_colorkey(BLACK)
        # pixels that have the same color as the colorkey will be transparent.
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedY = random.randrange(7, 20)
        self.speedx = random.randrange(-3, 3)  # make it more random
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedY
        if (self.rect.top > HEIGHT + 10) or (self.rect.left < -25) or (self.rect.right > WIDTH + 20):
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedY = random.randrange(2, 8)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = EXPLOSION_IMGS[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.fpsExp = 60
        self.frame = 0
        self.LstUpdt = pygame.time.get_ticks()

    def update(self):
        currentT = pygame.time.get_ticks()
        if currentT - self.LstUpdt > self.fpsExp:
            self.LstUpdt = currentT
            self.frame += 1

        if self.frame == len(EXPLOSION_IMGS):
            self.kill()
        else:
            center = self.rect.center
            self.image = EXPLOSION_IMGS[self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = center

        # Return the number of milliseconds since pygame.init() was called. Before pygame is initialized this will always be 0.


def main():
    running = True
    displayMenu = True
    while running:
        if displayMenu:
            menu()
            pygame.time.wait(2000)
            displayMenu = False

            all_sprites = pygame.sprite.Group()
            # A container class to hold and manage multiple Sprite objects.
            player = Player()
            all_sprites.add(player)

            missles = pygame.sprite.Group()

            def newMissile():
                missleElement = Missile()
                all_sprites.add(missleElement)
                missles.add(missleElement)

            for i in range(8):
                newMissile()

            # Initalize the score
            scoreBoard = 0

        timer.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # stops the while loop;

            if event.type == pygame.KEYDOWN:
                # At ESC close the window
                if event.key == pygame.K_ESCAPE:
                    running = False
                    # stops the while loop;

        # Collision Detection and actions
        hitCollision = pygame.sprite.spritecollide(
            player, missles, True, pygame.sprite.collide_circle)
        # spritecollide = Return a list containing all Sprites in a Group that intersect with another Sprite.
        # spritecollide(sprite, group, dokill, collided = None)
        # NOTE The dokill argument is a bool. If set to True, all Sprites that collide will be removed from the Group.
        # collide_circle = Collision detection between two sprites, using circles.

        for hits in hitCollision:
            # NOTE need to lower the health
            player.health -= 20
            EXPLOSION_SOUND.play()
            explosion = Explosion(hits.rect.center)
            all_sprites.add(explosion)
            newMissile()
            if player.health <= 0:
                running = False
                # stops the while loop;
        # screen change
        all_sprites.update()  # use update function for class in all_sprites
        WINDOW.fill(BLACK)
        # change color using RGB value (search up RGB if you do not know what it is)
        all_sprites.draw(WINDOW)
        drawHealthBar(WINDOW, 5, 5, player.health)
        scoreBoard += 1
        drawText(WINDOW, 'Score: ' + str(scoreBoard), 18, WIDTH / 2, 10)
        pygame.display.update()
    all_sprites.draw(WINDOW)


if __name__ == "__main__":
    # only run the file when the file is called
    main()

    # remember this code will not execute until the MAIN while loop is completed:
    gameEnd()
    # never forget this:
    pygame.quit()
