#PAGE 274 CONTINUE
import sys
import pygame
from gamesettings import Settings
from game_stats import GameStats
from Ship import Ship
from meteor import Meteor
import game_functions as gf
from pygame.sprite import Group

def run_game():
    # Initialize pygame,settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Create an instance to store game statistics.
    stats = GameStats(ai_settings)

    # Make a ship
    ship = Ship(ai_settings, screen)

    # Make a group to store bullets in.
    bullets = Group()

    # Make a meteor
    meteor = Meteor(ai_settings, screen)

    # Make a meteor shower
    meteors = Group()

    # Create the meteor shower
    gf.create_shower(ai_settings, screen, ship, meteors)

    # Set the background color
    bg_color = (230,230,230)

    # Start the main loop for the game
    while True:
        gf.check_events(ai_settings, screen, ship, bullets)
        if stats.game_active:
            ship.update()
            bullets.update()
            gf.update_bullets(ai_settings, screen, ship, meteors, bullets)
            gf.update_meteors(ai_settings, stats, screen, ship, meteors, bullets)
        gf.update_screen(ai_settings, screen, ship, bullets, meteors)


run_game()
