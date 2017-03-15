import pygame
from game.environment import get_new_piece, get_initial_board, can_fall, add_to_board, can_fit, check_lines
from game.agent import LearningAgent

SCREEN_SIZE = 10
SCREEN = pygame.display.set_mode((10 * SCREEN_SIZE, 20 * SCREEN_SIZE))

CLOCK = pygame.time.Clock()
FPS = 100

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

GAME_OVER = False

PIECE = None
BOARD = None

SCORE = 0

GAMMA = 0.9


def print_board(board):
    SCREEN.fill(WHITE)
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 1:
                print_block(row, col)

    pygame.display.update()
    CLOCK.tick(FPS)


def print_block(row, col):
    pygame.draw.rect(SCREEN, BLACK, (col * SCREEN_SIZE, row * SCREEN_SIZE, SCREEN_SIZE, SCREEN_SIZE))


def get_events():
    global GAME_OVER
    global FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_OVER = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if FPS > 0:
                    FPS -= 1
            if event.key == pygame.K_RIGHT:
                if FPS < 100:
                    FPS += 1


def get_action():
    global GAME_OVER
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_OVER = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                return 'left'
            if event.key == pygame.K_RIGHT:
                return 'right'
            if event.key == pygame.K_UP:
                return 'rotate'
    return ''


def take_action(action):
    if action == 'left':
        move_left()
    elif action == 'right':
        move_right()
    elif action == 'rotate':
        rotate()


def move_left():
    global PIECE
    global BOARD
    if can_fit(BOARD, PIECE, dx=-1, dy=1):
        if PIECE.x > 0:
            PIECE.x -= 1


def move_right():
    global PIECE
    global BOARD
    if can_fit(BOARD, PIECE, dx=1, dy=1):
        if PIECE.x < SCREEN_SIZE * 1:
            PIECE.x += 1


def rotate():
    global PIECE
    global BOARD

    rotated_piece = PIECE.get_next_rotation()
    if can_fit(BOARD, PIECE, rotated=True, dy=1):
        PIECE.shape = rotated_piece


def parse_moves(moves, reward):
    global GAMMA
    for i in reversed(range(len(moves))):
        moves[i]['reward'] = GAMMA ** i * reward

    return moves


def main():
    global PIECE
    global BOARD

    pygame.init()
    SCREEN.fill(WHITE)

    agent = LearningAgent(exploration_rate=.75)
    agent.load()

    while not GAME_OVER:
        BOARD = get_initial_board()
        PIECE = get_new_piece()

        while not GAME_OVER and can_fit(BOARD, PIECE):
            moves = []
            while can_fall(BOARD, PIECE) and not GAME_OVER:
                PIECE.y += 1

                temp_board = add_to_board(BOARD, PIECE)
                print_board(temp_board)
                #action = get_action()
                get_events()
                action = agent.get_action(temp_board)
                take_action(action)

                move = {'board': temp_board, 'action': action}
                moves.append(move)

            BOARD = add_to_board(BOARD, PIECE)
            BOARD, reward = check_lines(BOARD)
            PIECE = get_new_piece()

            parsed_moves = parse_moves(moves, reward)
            agent.learn(parsed_moves)

        print_board(BOARD)

        agent.save()

    pygame.quit()
    quit()



if __name__ == '__main__':
    main()
