import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 400, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Set up colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Set up font
font = pygame.font.SysFont(None, 36)

# Load images
bird_img = pygame.image.load("bird.png")  # Load your bird image
bird_img = pygame.transform.scale(bird_img, (40, 40))  # Resize the image to 40x40

# Bird class
class Bird:
    def __init__(self):
        self.x = 60
        self.y = HEIGHT // 2
        self.gravity = 0.5
        self.lift = -10
        self.velocity = 0
        self.size = 40  # This should match the size of the bird image
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)  # Bird hitbox

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        self.rect.topleft = (self.x - self.size // 2, self.y - self.size // 2)

        if self.y > HEIGHT:
            self.y = HEIGHT
            self.velocity = 0

        if self.y < 0:
            self.y = 0
            self.velocity = 0

    def flap(self):
        self.velocity = self.lift

    def draw(self):
        win.blit(bird_img, (self.x - self.size // 2, self.y - self.size // 2))

# Pipe class
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.width = 60  # Increased pipe width to make it thicker
        self.gap = 200  # Keep the larger gap between pipes
        self.height_top = random.randint(50, HEIGHT - self.gap - 50)
        self.speed = 3
        self.top_rect = pygame.Rect(self.x, 0, self.width, self.height_top)  # Top pipe hitbox
        self.bottom_rect = pygame.Rect(self.x, self.height_top + self.gap, self.width, HEIGHT - (self.height_top + self.gap))  # Bottom pipe hitbox

    def update(self):
        self.x -= self.speed
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self):
        # Draw top pipe (rectangle)
        pygame.draw.rect(win, GREEN, self.top_rect)
        # Draw bottom pipe (rectangle)
        pygame.draw.rect(win, GREEN, self.bottom_rect)

    def offscreen(self):
        return self.x < -self.width

# Main game function
def game():
    bird = Bird()
    pipes = [Pipe()]
    clock = pygame.time.Clock()
    run = True
    score = 0

    while run:
        clock.tick(30)
        win.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        # Update bird
        bird.update()
        bird.draw()

        # Update pipes
        if pipes[-1].x < WIDTH - 200:
            pipes.append(Pipe())

        for pipe in pipes:
            pipe.update()
            pipe.draw()
            if pipe.offscreen():
                pipes.remove(pipe)
                score += 1

        # Collision detection
        for pipe in pipes:
            if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
                run = False  # End game on collision

        # Display score
        score_text = font.render(f"Score: {score}", True, BLACK)
        win.blit(score_text, (10, 10))

        # Update display
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    game()
