import pygame


class AlineBullet:
    def __init__(self, alien):
        self.alien = alien
        self.screen = alien.screen

        self.image = pygame.image.load("Images/donat.png")
        self.image = pygame.transform.scale(self.image, (20, 20))

        self.rect = self.image.get_rect()
        self.rect.midbottom = self.alien.rect.midbottom
        self.bullet_speed = 5

    def draw_bullet(self):
        self.rect.y += self.bullet_speed
        self.screen.blit(self.image, self.rect)

class Alien:
    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.image = pygame.image.load("Images/pshin.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()

    def blit_alien(self):
        self.screen.blit(self.image, self.rect)

