import pygame

class Bullet:
    def __init__(self, game, side):
        self.screen = game.screen
        self.ship_rect = game.ship.rect

        self.image = pygame.image.load("Images/bullet.png")
        # self.image = pygame.image.load("Images/donat.png")
        self.image = pygame.transform.scale(self.image, (20, 35))

        self.rect = self.image.get_rect()
        self.bullets_speed = game.setting.bullets_speed

        if side == "left":
            self.rect.midleft = self.ship_rect.midleft
        else:
            self.rect.midright = self.ship_rect.midright

    def draw_bullet(self):
        self.rect.y -= self.bullets_speed
        self.screen.blit(self.image, self.rect)