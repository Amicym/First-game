from bullet import Bullet
from ship import Ship
from setting import Setting
from alien import Alien, AlineBullet

import pygame
import sys
from random import random, randrange

class AlienInvasion:
    def __init__(self, height: int, width: int, fps: int, bg_color: tuple, ship_speed: int, bullets_speed: int):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.setting = Setting(height, width, fps, bg_color, ship_speed, bullets_speed)

        self.running = True
        self.screen = pygame.display.set_mode(self.setting.get_screen_setting())

        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.setting.width = self.screen.get_rect().width - Полный экран
        # self.setting.height = self.screen.get_rect().height

        self.ship = Ship(self)
        self.aliens = []
        self.alien_x = []

        self.font = pygame.font.Font(None, 100)
        self.text = self.font.render("Поражение", True, (255, 255, 255))
        self.defeat = False

        self.ship_bullets = []
        self.alien_bullets = []

        self.last_alien_shot = 0

        self.bg = pygame.image.load("Images/bg.png")
        self.bg = pygame.transform.scale(self.bg, self.setting.get_screen_setting())
        self.bg_rect = self.bg.get_rect()

        pygame.display.set_caption("Alien Invasion")

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

        if event.key == pygame.K_SPACE:
            self.ship_bullets.append(Bullet(self, "left"))
            self.ship_bullets.append(Bullet(self, "right"))


    def _check_keyup_events(self, event):
        if event.key == pygame.K_w: self.ship.moving["up"] = False
        if event.key == pygame.K_s: self.ship.moving["down"] = False
        if event.key == pygame.K_a: self.ship.moving["left"] = False
        if event.key == pygame.K_d: self.ship.moving["right"] = False

    def _check_ship_hit(self):
        for bullet in self.alien_bullets[:]:
            if self.ship.rect.colliderect(bullet.rect):
                self.defeat = True
                self.alien_bullets.remove(bullet)

    def _check_alien_hit(self):
        for alien in self.aliens[:]:
            for bullet in self.ship_bullets[:]:
                if bullet.rect.colliderect(alien.rect):
                    self.ship_bullets.remove(bullet)

                    if alien in self.aliens:
                        self.aliens.remove(alien)

    def _create_alien(self):
        if pygame.time.get_ticks() - self.last_alien_shot < 1000:
            return

        for i in range(randrange(1, 10)):
            alien = Alien(self)
            alien.rect.x = randrange(200, self.setting.width - 200)

            # self.alien_x.append(alien.rect.x)
            self.aliens.append(alien)

    
    def _fire_bullets(self):
        for bullet in self.ship_bullets[:]:
            bullet.draw_bullet()
            if bullet.rect.y < 0:
                self.ship_bullets.remove(bullet)

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

    def _update_screen(self):
        self.screen.fill(self.setting.bg_color)
        self.screen.blit(self.bg)
        self._alien_fire_bullets()
        self._fire_bullets()
        self.ship.blitme()
        self._alien_draw_bullet()

        if self.defeat:
            self.screen.blit(self.text, (self.setting.width / 3, self.setting.height / 2))

        if self.aliens:
            for alien in self.aliens:
                alien.blit_alien()

        pygame.display.flip()

    def run(self):
        while self.running:
            self._update_screen()
            self._check_events()

            if not self.defeat:
                self._create_alien()
                self.ship.move()
                self._check_ship_hit()
                self._alien_fire_bullets()
                self._check_alien_hit()

            self.clock.tick(self.setting.fps)

if __name__ == "__main__":
    game = AlienInvasion(
        1000,
        1150,
        60,
        (75, 15, 25),
        10,
        15
    )

    game.run()
