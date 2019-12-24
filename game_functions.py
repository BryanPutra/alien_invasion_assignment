import sys
from time import sleep
import pygame
from bullet import Bullet
from meteor import Meteor

def ship_hit(ai_settings, stats, screen, ship, meteors, bullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1
        # Empty the list of aliens and bullets.
        meteors.empty()
        bullets.empty()
        # Create a new shower and center the ship.
        create_shower(ai_settings, screen, ship, meteors)
        ship.center_ship()
        # Pause.
        sleep(0.5)
    else:
        stats.game_active = False
        print("GAME OVER")

def change_shower_direction(ai_settings, meteors):
    """Drop the entire fleet and change the fleet's direction."""
    for meteor in meteors.sprites():
        meteor.rect.y += ai_settings.shower_drop_speed
    ai_settings.shower_direction *= -1

def check_shower_edges(ai_settings, meteors):
    """Respond appropriately if any aliens have reached an edge."""
    for meteor in meteors.sprites():
        if meteor.check_edges():
            change_shower_direction(ai_settings, meteors)
            break

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def get_number_meteors_x(ai_settings, meteor_width):
    """Determine the number of meteors that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * meteor_width
    number_meteors_x = int(available_space_x / (2 * meteor_width))
    return number_meteors_x

def create_meteor(ai_settings, screen, meteors, meteor_number, row_number):
    """Create a meteor and place it in the row."""
    meteor = Meteor(ai_settings, screen)
    meteor_width = meteor.rect.width
    meteor.x = meteor_width + 2 * meteor_width * meteor_number
    meteor.rect.y = meteor.rect.height + 2 * meteor.rect.height * row_number
    meteor.rect.x = meteor.x
    meteors.add(meteor)

def create_shower(ai_settings, screen, ship, meteors):
    """Create a full shower of meteors."""
    # Create a meteor and find the number of meteors in a row.
    meteor = Meteor(ai_settings, screen)
    number_meteors_x = get_number_meteors_x(ai_settings, meteor.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, meteor.rect.height)

    # Create the first row of meteors.
    # Create meteor showers
    for row_number in range(number_rows):
        for meteor_number in range(number_meteors_x):
            create_meteor(ai_settings, screen, meteors, meteor_number, row_number)

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached  yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    # elif event.key == pygame.K_UP:
    #     ship.moving_up = True
    # elif event.key == pygame.K_DOWN:
    #     ship.moving_down = True

def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    # elif event.key == pygame.K_DOWN:
    #     ship.moving_down = False
    # elif event.key == pygame.K_UP:
    #     ship.moving_up = False

def check_events(ai_settings, screen, ship, bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def update_screen(ai_settings, screen, ship, bullets, meteors):
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    meteors.draw(screen)
    # Make the most recently drawn screen visible.
    pygame.display.flip()

def update_bullets(ai_settings, screen, ship, meteors, bullets):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()
    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # Check for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.
    check_bullet_meteor_collisions(ai_settings, screen, ship, meteors, bullets)

def check_bullet_meteor_collisions(ai_settings, screen, ship, meteors, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.4
    collisions = pygame.sprite.groupcollide(bullets, meteors, True, True)
    if len(meteors) == 0:
        # Destroy existing bullets and create new fleet.
        bullets.empty()
        create_shower(ai_settings, screen, ship, meteors)

def update_meteors(ai_settings, stats, screen, ship, meteors, bullets):
    """Update the postions of all aliens in the fleet."""
    check_shower_edges(ai_settings, meteors)
    meteors.update()
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, meteors):
        ship_hit(ai_settings, stats, screen, ship, meteors, bullets)
    # Look for aliens hitting the bottom of the screen.
    check_meteors_bottom(ai_settings, stats, screen, ship, meteors, bullets)

def check_meteors_bottom(ai_settings, stats, screen, ship, meteors, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for meteor in meteors.sprites():
        if meteor.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, stats, screen, ship, meteors, bullets)
            break