import pygame
import sys
import random

# configuration – size of each cell and number of cells
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 5  # frames per second (game speed)

# colors (RGB tuples)
WHITE = (255, 255, 255)
GRAY = ( 40, 40, 40)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

def draw_rect(surface, color, position):
    """
    Helper that draws a single cell-sized rectangle on the given surface.
    `position` is a (x,y) tuple in grid coordinates.
    """
    r = pygame.Rect(position[0] * CELL_SIZE,
                    position[1] * CELL_SIZE,
                    CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, r)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock  = pygame.time.Clock()

    # start with a snake of length 1 in the center
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (1, 0)       # moving right initially
    food = None              # will hold food position

    def place_food():
        # pick a random grid cell that is not occupied by the snake
        while True:
            p = (random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
            if p not in snake:
                return p

    food = place_food()  # drop the first food piece

    running = True
    while running:
        # --- event handling ------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False             # window closed
            elif event.type == pygame.KEYDOWN:
                # change direction, but prevent reversing into yourself
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)
                elif event.key in (pygame.K_w, pygame.K_UP) and direction != (0, 1): direction = (0, -1)
                elif event.key in (pygame.K_s, pygame.K_DOWN) and direction != (0, -1): direction = (0, 1)

        # --- game logic ----------------------------------------------------
        # compute new head position by adding direction vector
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # check wall collision
        if (head[0] < 0 or head[0] >= GRID_WIDTH or
            head[1] < 0 or head[1] >= GRID_HEIGHT):
            running = False
            continue

        # check self-collision
        if head in snake:
            running = False
            continue

        snake.insert(0, head)    # add new head to front of list

        if head == food:
            food = place_food()  # eaten; spawn another
        else:
            snake.pop()          # remove tail if we didn't grow

        # --- drawing -------------------------------------------------------
        screen.fill(GRAY)              # clear background
        draw_rect(screen, RED, food)   # draw the food
        for segment in snake:          # draw each snake segment
            draw_rect(screen, PURPLE, segment)
        pygame.display.flip()          # update the window

        clock.tick(FPS)                # cap the frame rate

    pygame.quit()    # clean up pygame
    sys.exit()       # exit the program

if __name__ == "__main__":
    main()