import pygame
import random

class Sprite:
    def __init__(self, x, y, filename, speed, w, h):
        self.image = pygame.transform.scale(pygame.image.load(filename), (w, h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(Sprite):
    def update(self):
        self.rect.y += self.speed
class Patron(Sprite):
    def update(self):
        self.rect.y -= self.speed

class Player(Sprite):
    def __init__(self, x, y, filename, speed, w, h):
        super().__init__(x, y, filename, speed, w, h)
        self.patrons = []

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_SPACE]:
            self.patrons.append(Patron(self.rect.centerx, self.rect.y, 'bullet.png', 5, 2, 5))
        for i in range(len(self.patrons)):
            self.patrons[i].update()
    def draw(self, window):
        super(Player, self).draw(window)
        for i in range(len(self.patrons)):
            self.patrons[i].draw(window)


pygame.init()

window = pygame.display.set_mode((700, 500))
fps = pygame.time.Clock()

enemies = []
y = 0
for i in range(5):
    enemies.append(Enemy(0, y, "ufo.png", 5, 50, 50))
    y -= 100
rocket = Player(200, 400, "rocket.png", 5,100, 100)

while True:
    #обробка подій
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
    #оновлення
    for i in range(len(enemies)):
        enemies[i].update()
        if enemies[i].rect.y >500:
            enemies[i].rect.y =-50
            enemies[i].rect.x =random.randint(0, 500)
    rocket.update()


    for enemy in enemies:
        for patron in rocket.patrons:
            if patron.rect.colliderect(enemy.rect):
                rocket.patrons.remove(patron)
                enemy.rect.y =-50
                break

    #відмалювання
    window.fill((123, 123, 123))
    for i in range( len(enemies) ):
        enemies[i].draw(window)
    rocket.draw(window)
    pygame.display.flip()
    fps.tick(60)
