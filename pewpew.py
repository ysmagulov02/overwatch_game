import pygame
import os
pygame.font.init()
pygame.mixer.init() # for sound-effects

#window
WIDTH, HEIGHT = 900, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting game")

WHITE = (255, 255, 255) # colors are in RGB
GREY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT) # (x, y, width, height)

HEALTH_FONT = pygame.font.SysFont('public sans', 50)
WINNER_FONT = pygame.font.SysFont('public sans', 120)

FPS = 60
VEL = 5
BULLET_VEL = 9
MAX_BULLETS = 4
PLAYER_WIDTH, PLAYER_HEIGHT = 75, 75

BLUE_HIT = pygame.USEREVENT + 1
GREEN_HIT = pygame.USEREVENT + 2

# images
BLUE_PLAYER_IMAGE = pygame.image.load(
    os.path.join('Game_assets', 'p1.png'))
BLUE_PLAYER = pygame.transform.rotate(
    pygame.transform.scale(BLUE_PLAYER_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT)), 360)
    
GREEN_PLAYER_IMAGE = pygame.image.load(
    os.path.join('Game_assets', 'p2.png'))
GREEN_PLAYER = pygame.transform.rotate(
    pygame.transform.scale(GREEN_PLAYER_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT)), 360)

SPACE = pygame.transform.scale(
    pygame.image.load(os.path.join('Game_assets', 'space.png')), (WIDTH, HEIGHT))
    
# sound - effects
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Game_assets', 'shooting.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Game_assets', 'getting_hit.mp3'))


def draw_window(green, blue, green_bullets, blue_bullets, green_health, blue_health):
    WINDOW.blit(SPACE, (0,0)) # to put the images/text onto the screen
    
    # the drawing starts from top left corner
    pygame.draw.rect(WINDOW, GREY, BORDER)
    
    green_health_text = HEALTH_FONT.render(
        "HP: " + str(green_health), 1, WHITE)
    blue_health_text = HEALTH_FONT.render(
        "HP: " + str(blue_health), 1, WHITE)
        
    WINDOW.blit(green_health_text, (WIDTH - green_health_text.get_width() - 10, 10))
    WINDOW.blit(blue_health_text, (10, 10))
    
    WINDOW.blit(BLUE_PLAYER, (blue.x, blue.y))
    
    WINDOW.blit(GREEN_PLAYER, (green.x, green.y))
    
    
    for bullet in green_bullets:
        pygame.draw.rect(WINDOW, GREEN, bullet)
        
    for bullet in blue_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)
    
    pygame.display.update()


def blue_handle_movement(keys_pressed, blue):
    if keys_pressed[pygame.K_a] and blue.x - VEL > 0: # LEFT
        blue.x -= VEL
    if keys_pressed[pygame.K_d] and blue.x + VEL + blue.height  < BORDER.x: # RIGHT
        blue.x += VEL
    if keys_pressed[pygame.K_w] and blue.y - VEL > 0: # UP
        blue.y -= VEL
    if keys_pressed[pygame.K_s] and blue.y + VEL + blue.width < HEIGHT: # DOWN
        blue.y += VEL
        
def green_handle_movement(keys_pressed, green):
    if keys_pressed[pygame.K_LEFT] and green.x - VEL > BORDER.x + BORDER.width: # LEFT
        green.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and green.x + VEL + green.height  < WIDTH: # RIGHT
        green.x += VEL
    if keys_pressed[pygame.K_UP] and green.y - VEL > 0: # UP
        green.y -= VEL
    if keys_pressed[pygame.K_DOWN] and green.y + VEL + green.width < HEIGHT: # DOWN
        green.y += VEL


def handle_bullets(blue_bullets, green_bullets, blue, green): # move the bulets,
    #handle the collision of the bullets, handle removing of the bullets when off screen or hit
    
    for bullet in blue_bullets: # handles solder bullets
        bullet.x += BULLET_VEL
        if green.colliderect(bullet): # true or false value (only works with rectangles)
            pygame.event.post(pygame.event.Event(GREEN_HIT))
            blue_bullets.remove(bullet)
            
        elif bullet.x > WIDTH:
            blue_bullets.remove(bullet)
            
            
    for bullet in green_bullets: # handles lucio bullets
        bullet.x -= BULLET_VEL
        if blue.colliderect(bullet): # true or false value (only works with rectangles)
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            green_bullets.remove(bullet)
    
        elif bullet.x < 0:
            green_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WINDOW.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    
    pygame.display.update()
    pygame.time.delay(5000) # 5 seconds


def main():
    green = pygame.Rect(700, 300, PLAYER_WIDTH, PLAYER_HEIGHT)
    blue = pygame.Rect(100, 300, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    green_bullets = []
    blue_bullets = []
    
    green_health = 10
    blue_health = 10
    
        
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS) # controls the speed of the while loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # lets me close the game
                run = False
                pygame.quit()
                exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(blue_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        blue.x + blue.width, blue.y + blue.height//2 - 2, 10, 5)
                    # last two are height and width of the bullet
                    blue_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                
                if event.key == pygame.K_RSHIFT and len(green_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        green.x, green.y + green.height//2 - 2, 10, 5)
                    green_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            
            # health
            if event.type == GREEN_HIT:
                green_health -= 1
                BULLET_HIT_SOUND.play()
                
            if event.type == BLUE_HIT:
                blue_health -= 1
                BULLET_HIT_SOUND.play()
        
        winner_text = ""
        if green_health == 0:
            winner_text = "Soldier Wins!"
        
        if blue_health == 0:
            winner_text = "Lucio Wins!"
        
        if winner_text != "":
            draw_winner(winner_text)
            break
        
                
        #print(green_bullets, blue_bullets)
        keys_pressed = pygame.key.get_pressed() # registering pressed keys
        blue_handle_movement(keys_pressed, blue)
        green_handle_movement(keys_pressed, green)
        
        handle_bullets(blue_bullets, green_bullets, blue, green)
        
        
        draw_window(green, blue, green_bullets, blue_bullets, green_health, blue_health)
                
    main()
    

if __name__ == "__main__":
    main()
