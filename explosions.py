import pygame
from random import randrange


class Explosions:
    def __init__(self, game, x, y):
        self.screen = game.screen
        self.images = []

        for i in range(1, 7):
            image = pygame.image.load(f"Images/e_frame_{i}.png")
            image = pygame.transform.scale(image, (200, 200))
            self.images.append(image)
        
        self.frame = 0
        self.animation_speed = 50
        self.rect = self.images[0].get_rect()
        self.rect.center = (x + 85, y + 85)
        
        self.create_at = pygame.time.get_ticks()
        self.last_update = pygame.time.get_ticks()

    def draw(self):
        now = pygame.time.get_ticks()

        if now - self.last_update > self.animation_speed: 
            self.frame = (self.frame + 1) % len(self.images)
            self.last_update = now

        self.screen.blit(self.images[self.frame], self.rect)
        

    def is_expired(self):
        return pygame.time.get_ticks() - self.create_at < self.animation_speed * len(self.images)
    
# Переделать тут, сделать список из rect и тд