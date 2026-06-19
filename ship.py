import pygame

from setting import Setting


class Ship:
    _image_cache = None

    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.setting = game.setting

        if Ship._image_cache is None:
            images = []
            for i in range(1, 5):
                image = pygame.image.load(f"Images/ship_{i}.png")
                image = pygame.transform.scale(image, (125, 125)) # Изменяет размер
                images.append(image)
            
            Ship._image_cache = images

        self.images = Ship._image_cache
        
        self.rect = self.images[0].get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

        self.moving = {
            "up": False,
            "down": False,
            "left": False,
            "right": False
        }

        self.ship_speed = self.setting.ship_speed

        self.frame = 0
        self.animation_speed = 100
        self.last_update = pygame.time.get_ticks()

    def move(self):
        if self.moving["up"]:
            if self.rect.y - self.ship_speed > 0:
                self.rect.y -= self.ship_speed

        if self.moving["down"]:
            if self.rect.y + self.ship_speed < self.setting.height - 100:
                self.rect.y += self.ship_speed

        if self.moving["left"]:
            if self.rect.x - self.ship_speed > -10:
                self.rect.x -= self.ship_speed

        if self.moving["right"]:
            if self.rect.x + self.ship_speed < self.setting.width - 110:
                self.rect.x += self.ship_speed


    def _update(self):
        now = pygame.time.get_ticks()

        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame = (self.frame + 1) % len(self.images)

    def blitme(self):
        self.screen.blit(self.images[self.frame], self.rect)
        self._update()