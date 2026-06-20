from bullet import Bullet
from ship import Ship
from setting import Setting
from alien import Alien, AlineBullet
from explosions import Explosions

import pygame
import sys
from random import random, randrange

class AlienInvasion:
    def __init__(self, height: int, width: int, fps: int, bg_color: tuple, ship_speed: int, bullets_speed: int):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.setting = Setting(height, width, fps, bg_color, ship_speed, bullets_speed)

        self.screen = pygame.display.set_mode(self.setting.get_screen_setting())
        self.screen_rect = self.screen.get_rect()

        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.setting.width = self.screen.get_rect().width - Полный экран
        # self.setting.height = self.screen.get_rect().height

        self.ship = Ship(self)
        self.aliens = []
        self.explosions = []

        self.score = 0
        self.font = pygame.font.Font("Font/TrueType (.ttf)/PixeloidMono.ttf", 200)
        self.font_s = pygame.font.Font("Font/TrueType (.ttf)/PixeloidMono.ttf", 36)
        self.font_start = pygame.font.Font("Font/TrueType (.ttf)/PixeloidMono.ttf", 150)

        self.start_text = self.font_start.render("TO START\nPRESS 'R'", True, (255, 255, 255))
        self.start_text_rect = self.start_text.get_rect()
        self.start_text_rect.center = self.screen_rect.center
    
        self.deafeat_text = self.font.render("game over\n   'r'".upper(), True, (255, 255, 255))
        self.deafeat_text_rect = self.deafeat_text.get_rect()
        self.deafeat_text_rect.center = self.screen_rect.center

        self.defeat = False
        self.start = False
        self.running = True

        self.ship_bullets = []
        self.alien_bullets = []

        self.last_alien_spawn = 0
        self.last_alien_shot = 0

        self.bg = pygame.image.load("Images/bg.png")
        self.bg = pygame.transform.scale(self.bg, self.setting.get_screen_setting())
        self.bg_rect = self.bg.get_rect()

        pygame.display.set_caption("Alien Invasion")
        pygame.display.set_icon(pygame.image.load("Images/alien.png"))

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            if event.type == pygame.KEYUP:
                self._check_keyup_events(event)


    def _check_keydown_events(self, event):
        if event.key == pygame.K_w: self.ship.moving["up"] = True
        if event.key == pygame.K_s: self.ship.moving["down"] = True
        if event.key == pygame.K_a: self.ship.moving["left"] = True
        if event.key == pygame.K_d: self.ship.moving["right"] = True

        if event.key == pygame.K_q: sys.exit()

        if event.key == pygame.K_r:
            self.start = True
            self.defeat = False
            self.score = 0
            self.aliens.clear()
            self.alien_bullets.clear()
            self.ship.rect.midbottom = self.screen_rect.midbottom


        if event.key == pygame.K_SPACE:
            self.ship_bullets.append(Bullet(self, "left"))
            self.ship_bullets.append(Bullet(self, "right"))


    def _check_keyup_events(self, event):
        if event.key == pygame.K_w: self.ship.moving["up"] = False
        if event.key == pygame.K_s: self.ship.moving["down"] = False
        if event.key == pygame.K_a: self.ship.moving["left"] = False
        if event.key == pygame.K_d: self.ship.moving["right"] = False

    def _check_ship_hit(self):
        for alien in self.aliens:
            if self.ship.rect.colliderect(alien):
                self._create_explosions(self.ship.rect.x, self.ship.rect.y)
                self.defeat = True
                break

        for bullet in self.alien_bullets[:]:
            if self.ship.rect.colliderect(bullet.rect):
                self._create_explosions(self.ship.rect.x, self.ship.rect.y)
                self.defeat = True
                self.alien_bullets.remove(bullet)
                break
    
    def check_aliens_bottom(self):
        for alien in self.aliens:
            if alien.rect.y == self.setting.height:
                self.defeat = True
                break
    
    def _check_alien_hit(self):
        for alien in self.aliens[:]:
            for bullet in self.ship_bullets[:]:
                if bullet.rect.colliderect(alien.rect):
                    self.ship_bullets.remove(bullet)

                    if alien in self.aliens:
                        x = alien.rect.x
                        y = alien.rect.y

                        self.score += alien.score_in_alien
                        self.aliens.remove(alien)
                        self._create_explosions(x, y)
    
    def _create_explosions(self, x, y):
        explosion = Explosions(self, x, y)
        self.explosions.append(explosion)

    def _update_explosions(self):
        for explosion in self.explosions[:]:
            if explosion.is_expired():
                explosion.draw()
            else:
                self.explosions.remove(explosion)
    
    def _create_alien(self):
        if pygame.time.get_ticks() - self.last_alien_spawn < 800:
            return

        for _ in range(randrange(5, 10)):
            alien = Alien(self)
            alien.rect.x = randrange(-50, self.setting.width - 150)

            if not any(alien.rect.colliderect(a) for a in self.aliens):
                self.aliens.append(alien)
        
        self.last_alien_spawn = pygame.time.get_ticks()
        
    def _fire_bullets(self):
        for bullet in self.ship_bullets[:]:
            bullet.draw_bullet()
            if bullet.rect.y < 0:
                self.ship_bullets.remove(bullet)

    def _update_alien(self):
        if self.aliens:
            for alien in self.aliens:
                alien.blit_alien()
    
    def _alien_fire_bullets(self):
        if pygame.time.get_ticks() - self.last_alien_shot < 1000:
            return

        for alien in self.aliens:
            if random() <= 0.33:
                self.alien_bullets.append(AlineBullet(alien))

            self.last_alien_shot = pygame.time.get_ticks()

    def _alien_draw_bullet(self):
        for bullet in self.alien_bullets[:]:
            bullet.draw_bullet()

            if bullet.rect.y > self.setting.height:
                self.alien_bullets.remove(bullet)
   
    def _check_defeat(self):
        self._check_ship_hit()
        self.check_aliens_bottom()


    def _draw_text(self):
        if not self.start:
            self.screen.blit(self.start_text, self.start_text_rect)

        else:
            self.score_text = self.font_s.render(f"SCORE: {self.score}", False, (255, 255, 255))
            self.score_text_rect = self.score_text.get_rect()
            self.score_text_rect.topleft = self.screen_rect.topleft
            
            self.screen.blit(self.score_text, self.score_text_rect)

            if self.defeat:
                self.screen.blit(self.deafeat_text, self.deafeat_text_rect)
        
        
        
        
    def _update_screen(self):
        # self.screen.fill(self.setting.bg_color)
        self.screen.blit(self.bg)
        self._draw_text()

        if self.start:
            self._fire_bullets()

            self._alien_fire_bullets()
            self._alien_draw_bullet()
            self._update_alien()

            self._update_explosions()

            if not self.defeat:
                self.ship.blitme()
            else:
                self.screen.blit(self.deafeat_text, self.deafeat_text_rect)

        pygame.display.flip()

    def run(self):
        while self.running:
            self._update_screen()
            self._check_events()

            if self.start:
                self._create_alien()

                if not self.defeat:
                    self.ship.move()
                    self._check_defeat()
                    self._alien_fire_bullets()
                    self._check_alien_hit()

            self.clock.tick(self.setting.fps)

if __name__ == "__main__":
    game = AlienInvasion(
        1900,           # Ширена
        1150,           # Высота
        60,             # FPS
        (75, 15, 25),   # bg(Не нужен, может стоять любой)
        12,             # Скорость коробля
        20              # Скорость Пуль для коробля
    )

    game.run()