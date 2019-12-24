import pygame
from pygame.sprite import Sprite

class Meteor(Sprite):
    """A class to represent a single meteor in the shower."""

    def __init__(self, ai_settings, screen):
        """Initialize the meteor and set its starting position."""

        super(Meteor, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the meteor image and set its rect attribute.
        self.image = pygame.image.load('meteor2.png')
        self.rect = self.image.get_rect()

        # Start each new meteor near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the meteor's exact position.
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the meteor at its current location."""

        self.screen.blit(self.image, self.rect)

    def update(self):
        """Move the alien right or left."""
        self.x += (self.ai_settings.meteor_speed_factor * self.ai_settings.shower_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True