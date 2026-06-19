import pygame


class AlineBullet:
    _image_cache = None

    def __init__(self, alien):
        self.alien = alien
        self.screen = alien.screen

        if AlineBullet._image_cache is None:
            image = pygame.image.load("Images/donat.png")
            image = pygame.transform.scale(image, (20, 20))
            AlineBullet._image_cache = image
    
        self.image = AlineBullet._image_cache        
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.alien.rect.midbottom
        self.bullet_speed = 10

    def draw_bullet(self):
        self.rect.y += self.bullet_speed
        self.screen.blit(self.image, self.rect)

class Alien:
    _image_cache = None
    
    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        if Alien._image_cache is None:
            image = pygame.image.load("Images/alien.png")
            Alien._image_cache = pygame.transform.scale(image, (200, 200))

        self.image = Alien._image_cache
        self.rect = self.image.get_rect()
        self.rect.y = -200

    def blit_alien(self):      
        self.rect.y += 2.5
        self.screen.blit(self.image, self.rect)

