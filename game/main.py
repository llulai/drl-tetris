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


def parse_moves(moves):
    global GAMMA
    for i in range(1, len(moves)):
        moves[i-1]['board_t1'] = moves[i]['board']

    return moves


def main():
    global PIECE
    global BOARD
    global SCORE

    counter = 0

    pygame.init()
    SCREEN.fill(WHITE)

    agent = LearningAgent(exploration_rate=.5)
    agent.load()

    while not GAME_OVER:
        BOARD = get_initial_board()
        PIECE = get_new_piece()
        moves = []

        while not GAME_OVER and can_fit(BOARD, PIECE):
            while can_fall(BOARD, PIECE) and not GAME_OVER:
                PIECE.y += 1

                temp_board = add_to_board(BOARD, PIECE)
                print_board(temp_board)
                #action = get_action()
                get_events()
                action = agent.get_action(temp_board)
                take_action(action)

                move = {'board': temp_board, 'action': action, 'reward': 10}
                moves.append(move)
                counter += 1
                if counter == 1000:
                    agent.learn()
                    counter = 0

            BOARD = add_to_board(BOARD, PIECE)
            BOARD, reward = check_lines(BOARD)
            moves[-1]['reward'] += reward
            PIECE = get_new_piece()

        parsed_moves = parse_moves(moves)
        agent.memorize(parsed_moves)
        #agent.learn()



        print_board(BOARD)

        agent.save()

    pygame.quit()
    quit()



if __name__ == '__main__':
    main()
