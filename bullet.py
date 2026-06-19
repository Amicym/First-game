import pygame

class Bullet:
    _image_cache = None
    
    def __init__(self, game, side):
        self.screen = game.screen
        self.ship_rect = game.ship.rect

        if Bullet._image_cache is None:
            image = pygame.image.load("Images/bullet.png")
            image = pygame.transform.scale(image, (20, 35))
            Bullet._image_cache = image
        
        self.image = Bullet._image_cache
            
        self.rect = self.image.get_rect()
        self.bullets_speed = game.setting.bullets_speed

        if side == "left":
            self.rect.midleft = self.ship_rect.midleft
        else:
            self.rect.midright = self.ship_rect.midright

    def draw_bullet(self):
        self.rect.y -= self.bullets_speed
        self.screen.blit(self.image, self.rect)