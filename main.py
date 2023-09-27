from random import randint
from random import randrange
from globals import *

pygame.init()


class Snake:
    def __init__(self):
        self.head_col = COLUMNS // 2
        self.head_row = ROWS // 2
        self.body = [(ROWS // 2, COLUMNS // 2)]
        self.head_color = HEAD_COLOR
        self.body_color = BODY_COLOR
        self.length = 1
        self.speed = FPS * 3
        self.dir_x = 1
        self.dir_y = 0
        self.block_directions = [(1, 0)]
        self.dir_permissions = {"RIGHT": True, "LEFT": False, "UP": True, "DOWN": True}
        self.score = 0


def draw_block(screen, row, column, color):
    """
    This function draws a block on the playing field.
    :param screen: The game screen
    :param row: The row of the block on the playing field
    :param column:The column of the block on the playing field
    :param color:The color of the block
    :return:nothing
    """
    x1 = BLOCK_SIZE * column + BLOCK_INDENT * (column + 1)
    y1 = HEADER_INDENT + BLOCK_SIZE * row + BLOCK_INDENT * (row + 1)
    pygame.draw.rect(screen, color, (x1, y1, BLOCK_SIZE, BLOCK_SIZE))


def draw_map(screen, game_map):
    """
    This function draws the playing field according to a given game_map.
    :param screen: The game screen
    :param game_map: A two-dimensional list that contains information about each cell of the playing field.
    :return:nothing
    """
    screen.fill(FIELD_COLOR)
    pygame.draw.rect(screen, HEADER_COLOR, (0, 0, WIDTH, HEADER_INDENT))
    for i in range(1, ROWS - 1):
        for j in range(1, COLUMNS - 1):
            if game_map[i][j] == 1:
                draw_block(screen, i, j, OBSTACLE_COLOR)
            elif (i + j) % 2 == 0:
                draw_block(screen, i, j, FIRST_BLOCK_COLOR)
            else:
                draw_block(screen, i, j, SECOND_BLOCK_COLOR)
    for col in range(COLUMNS):
        draw_block(screen, 0, col, OBSTACLE_COLOR)
        draw_block(screen, ROWS - 1, col, OBSTACLE_COLOR)
    for row in range(1, ROWS):
        draw_block(screen, row, 0, OBSTACLE_COLOR)
        draw_block(screen, row, COLUMNS - 1, OBSTACLE_COLOR)


def reverse_direction(direction):
    """
    This function returns the reverse direction of movement
    according to the received direction of movement.
    :param direction: It contains two numbers. First is horizontal direction. Second is vertical direction.
    :return: It returns two numbers that are inverted numbers.
    """
    if direction == (1, 0):
        return (-1, 0)
    if direction == (-1, 0):
        return (1, 0)
    if direction == (0, 1):
        return (0, -1)
    if direction == (0, -1):
        return (0, 1)


def update_record(level, score):
    """
    This function checks if the current score is not less than record of current level.
    And if so, it updates the record.
    :param level: The current game level
    :param score: The current game score
    :return: nothing
    """
    file_name1 = f'record{level}.txt'
    file1 = open(file_name1, 'r')
    old_record = 0
    for line in file1:
        old_record = int(line)
    file1.close()
    if old_record <= score:
        file2 = open(file_name1, 'w')
        file2.write(str(score))
        file2.close()


def play_game(level):
    """
    This is a function that starts a new game session.
    It also handles all game events.
    :param level: The current game level
    :return: nothing
    """
    global game_map
    game_map = load_level(level)
    obstacles = []
    for i in range(ROWS):
        for j in range(COLUMNS):
            if game_map[i][j] == 1:
                obstacles.append((i, j))
    have_slower = False
    have_speeder = False
    have_reverser = False
    slower = [-1, -1]
    speeder = [-1, -1]
    reverser = [-1, -1]
    record = get_record(level)
    while True:
        apple = [randrange(1, ROWS - 1, 1), randrange(1, COLUMNS - 1, 1)]
        if tuple(apple) not in obstacles:
            break
    snake = Snake()
    running = True
    while running:
        is_pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                update_record(level, snake.score)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake.dir_permissions["LEFT"] and not is_pressed:
                    is_pressed = True
                    snake.dir_x = -1
                    snake.dir_y = 0
                    snake.dir_permissions = {"RIGHT": False, "LEFT": True, "UP": True, "DOWN": True}
                elif event.key == pygame.K_RIGHT and snake.dir_permissions["RIGHT"] and not is_pressed:
                    is_pressed = True
                    snake.dir_x = 1
                    snake.dir_y = 0
                    snake.dir_permissions = {"RIGHT": True, "LEFT": False, "UP": True, "DOWN": True}
                elif event.key == pygame.K_UP and snake.dir_permissions["UP"] and not is_pressed:
                    is_pressed = True
                    snake.dir_x = 0
                    snake.dir_y = -1
                    snake.dir_permissions = {"RIGHT": True, "LEFT": True, "UP": True, "DOWN": False}
                elif event.key == pygame.K_DOWN and snake.dir_permissions["DOWN"] and not is_pressed:
                    is_pressed = True
                    snake.dir_x = 0
                    snake.dir_y = 1
                    snake.dir_permissions = {"RIGHT": True, "LEFT": True, "UP": False, "DOWN": True}

        if snake.head_row < 1 or snake.head_col < 1 or snake.head_row >= ROWS - 1 or snake.head_col >= COLUMNS - 1:
            update_record(level, snake.score)
            running = False
            break
        if (snake.head_row, snake.head_col) in snake.body[:-1]:
            update_record(level, snake.score)
            running = False
            break
        if (snake.head_row, snake.head_col) in obstacles:
            update_record(level, snake.score)
            running = False
            break
        if not running:
            update_record(level, snake.score)
            break
        # отрисовка поля
        draw_map(screen, game_map)
        font = pygame.font.SysFont('liberationmono', 42)
        lvl_text = font.render(f'LVL {level}', True, TEXT_COLOR)
        screen.blit(lvl_text, (20, 20))
        score_text = font.render(f"Your score: {snake.score}", True, TEXT_COLOR)
        screen.blit(score_text, (WIDTH // 3, 0))
        record_text = font.render('Record: ' + record, True, TEXT_COLOR)
        screen.blit(record_text, (WIDTH // 3, 40))

        # отрисовка яблока и змейки
        draw_block(screen, apple[0], apple[1], pygame.Color("red"))
        draw_block(screen, snake.head_row, snake.head_col, snake.head_color)
        for row, col in snake.body[:-1]:
            draw_block(screen, row, col, snake.body_color)

        # отрисовка бонусов
        if have_speeder:
            draw_block(screen, speeder[0], speeder[1], SPEEDER_COLOR)
        if have_slower:
            draw_block(screen, slower[0], slower[1], SLOWER_COLOR)
        if have_reverser:
            draw_block(screen, reverser[0], reverser[1], REVERSER_COLOR)

        # расчет следующего положения
        snake.head_col += snake.dir_x
        snake.head_row += snake.dir_y
        snake.body.append((snake.head_row, snake.head_col))
        snake.block_directions.append((snake.dir_x, snake.dir_y))

        # поедание яблока
        if snake.body[-1] == tuple(apple):
            snake.length += 1
            snake.score += 1
            while True:
                apple = [randrange(1, ROWS - 1, 1), randrange(1, COLUMNS - 1, 1)]
                if tuple(apple) not in snake.body and tuple(apple) not in obstacles:
                    break
            snake.speed += FPS // 3

        snake.body = snake.body[-snake.length:]
        snake.block_directions = snake.block_directions[-snake.length:]

        # поедание бонусов
        if have_speeder and snake.body[-1] == tuple(speeder):
            have_speeder = False
            snake.speed += FPS
        if have_slower and snake.body[-1] == tuple(slower):
            have_slower = False
            snake.speed = max(FPS * 3, snake.speed - FPS * 2)
        if have_reverser and snake.body[-1] == tuple(reverser):
            have_reverser = False
            snake.body.reverse()
            snake.block_directions.reverse()
            snake.head_row, snake.head_col = snake.body[-1]
            if snake.block_directions[-1] == (1, 0):
                snake.dir_permissions = {"RIGHT": False, "LEFT": True, "UP": True, "DOWN": True}
                snake.dir_x = -1
                snake.dir_y = 0
            if snake.block_directions[-1] == (-1, 0):
                snake.dir_permissions = {"RIGHT": True, "LEFT": False, "UP": True, "DOWN": True}
                snake.dir_x = 1
                snake.dir_y = 0
            if snake.block_directions[-1] == (0, 1):
                snake.dir_permissions = {"RIGHT": True, "LEFT": True, "UP": True, "DOWN": False}
                snake.dir_x = 0
                snake.dir_y = -1
            if snake.block_directions[-1] == (0, -1):
                snake.dir_permissions = {"RIGHT": True, "LEFT": True, "UP": False, "DOWN": True}
                snake.dir_x = 0
                snake.dir_y = 1

            for i in range(len(snake.block_directions)):
                snake.block_directions[i] = reverse_direction(snake.block_directions[i])

        # появление бонусов
        if not have_speeder:
            if randint(1, 1000000) % 5000 > min(4850 + snake.speed // 5, 4990):
                have_speeder = True
                while True:
                    speeder = [randrange(1, ROWS - 1, 1), randrange(1, COLUMNS - 1, 1)]
                    if tuple(speeder) not in snake.body and tuple(speeder) not in obstacles and tuple(speeder) != tuple(
                            apple):
                        break
        if not have_slower:
            if randint(1, 1000000) % 5000 > min(4850 + snake.speed // 5, 4990):
                have_slower = True
                while True:
                    slower = [randrange(1, ROWS - 1, 1), randrange(1, COLUMNS - 1, 1)]
                    if tuple(slower) not in snake.body and tuple(slower) not in obstacles and tuple(slower) != tuple(
                            apple):
                        break
        if not have_reverser:
            if randint(1, 1000000) % 5000 > min(4850 + snake.speed // 5, 4920):
                have_reverser = True
                while True:
                    reverser = [randrange(1, ROWS - 1, 1), randrange(1, COLUMNS - 1, 1)]
                    if tuple(reverser) not in snake.body and tuple(reverser) not in obstacles and tuple(
                            reverser) != tuple(apple):
                        break

        pygame.display.update()
        clock.tick(snake.speed / FPS)


def create_btn(font, screen, btn_color, x, y, name, btn_text_color):
    """
    This function draws the corresponding button on the screen
    according to the specified font, button color, text and text color,
    and the location of the button.
    :param font: The font of the text on the button
    :param screen: The screen on which the button will be displayed
    :param btn_color: The color of the button
    :param x: The x-axis coordinate of the button
    :param y: The y-axis coordinate of the button
    :param name: The text on the button
    :param btn_text_color: The color of the text on the button
    :return: It returns rectangle object that is responsible for the button
    """
    btn = pygame.draw.rect(screen, btn_color, [x, y, 350, 60], 0, 7)
    text = font.render(f'{name}', True, btn_text_color)
    screen.blit(text, (x + 20, y + 10))
    return btn


def ch_color_menu():
    """
    This function is responsible for displaying the menu for selecting the color of the snake,
    which contains buttons.
    :return: nothing
    """
    global screen
    global HEAD_COLOR
    global BODY_COLOR
    font = pygame.font.SysFont('liberationmono', 45)
    running = True
    while running:
        screen.fill(MENU_COLOR)
        color_menu_timer.tick(MENU_FPS)

        green_btn = create_btn(font, screen, BTN_COLOR, WIDTH // 3 - 25, 250, 'GREEN', BTN_TEXT_COLOR)
        sand_btn = create_btn(font, screen, BTN_COLOR, WIDTH // 3 - 25, 350, 'SAND', BTN_TEXT_COLOR)
        white_btn = create_btn(font, screen, BTN_COLOR, WIDTH // 3 - 25, 450, 'WHITE', BTN_TEXT_COLOR)
        back_btn = create_btn(font, screen, BTN_COLOR, WIDTH // 3 - 25, 650, 'Back', BTN_TEXT_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_btn.collidepoint(pygame.mouse.get_pos()):
                    running = False
                    break
                elif green_btn.collidepoint(pygame.mouse.get_pos()):
                    HEAD_COLOR = GREEN_HEAD
                    BODY_COLOR = GREEN_BODY
                elif sand_btn.collidepoint(pygame.mouse.get_pos()):
                    HEAD_COLOR = SAND_HEAD
                    BODY_COLOR = SAND_BODY
                elif white_btn.collidepoint(pygame.mouse.get_pos()):
                    HEAD_COLOR = WHITE_HEAD
                    BODY_COLOR = WHITE_BODY
                running = False
                break
        pygame.display.update()


def load_level(number):
    """
    This function reads the information about it from the desired file by the level number
    and puts it in a two-dimensional list, after which it returns this list.
    :param number: The number of the desired level
    :return: It returns a two-dimensional list that contains information about the desired level
    """
    file_name = f'lvl{number}.txt'
    file = open(file_name, 'r')
    lvl_map = [[0 for i in range(COLUMNS)] for j in range(ROWS)]
    row = 0
    col = 0
    for line in file:
        for c in line:
            lvl_map[row][col] = int(c)
            col += 1
            if col >= COLUMNS:
                col = 0
                row += 1
    file.close()
    return lvl_map


def edit_level(number):
    """
    This function allows you to edit the level with the desired number using a computer mouse.
    :param number: The number of the desired level
    :return: nothing
    """
    global screen
    font = pygame.font.SysFont('liberationmono', 40)
    file_name = f'lvl{number}.txt'
    lvl_map = load_level(number)
    running = True
    while running:
        edit_level_timer.tick(MENU_FPS)
        draw_map(screen, lvl_map)
        text_1 = font.render('Press S to save', True, TEXT_COLOR)
        text_2 = font.render('Press Esc to cancel', True, TEXT_COLOR)
        screen.blit(text_1, (20, 0))
        screen.blit(text_2, (20, 45))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_col = mouse_x // (BLOCK_SIZE + BLOCK_INDENT)
                mouse_row = (mouse_y - HEADER_INDENT) // (BLOCK_SIZE + BLOCK_INDENT)
                if 0 < mouse_row < ROWS - 1:
                    if 0 < mouse_col < COLUMNS - 1:
                        if lvl_map[mouse_row][mouse_col] == 0:
                            lvl_map[mouse_row][mouse_col] = 1
                        else:
                            lvl_map[mouse_row][mouse_col] = 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    file = open(file_name, 'w')
                    for row in range(ROWS):
                        for col in range(COLUMNS):
                            file.write(str(lvl_map[row][col]))
                    file.close()
                    running = False
                    break
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
        pygame.display.update()


def lvl_edit_menu():
    """
    This function is responsible for displaying a menu
    in which you can select the desired level for editing by clicking on the buttons.
    :return: nothing
    """
    global screen
    font = pygame.font.SysFont('liberationmono', 45)
    running = True
    while running:
        screen.fill(MENU_COLOR)
        lvl_edit_menu_timer.tick(MENU_FPS)
        lvl1_btn = create_btn(font, screen, BTN_COLOR, WIDTH // 3 - 25, 150, '1 LVL', BTN_TEXT_COLOR)
        lvl2_btn = create_btn(font, screen, BTN_COLOR, WIDTH // 3 - 25, 250, '2 LVL', BTN_TEXT_COLOR)
        lvl3_btn = create_btn(font, screen, BTN_COLOR, WIDTH // 3 - 25, 350, '3 LVL', BTN_TEXT_COLOR)
        lvl4_btn = create_btn(font, screen, BTN_COLOR, WIDTH // 3 - 25, 450, '4 LVL', BTN_TEXT_COLOR)
        lvl5_btn = create_btn(font, screen, BTN_COLOR, WIDTH // 3 - 25, 550, '5 LVL', BTN_TEXT_COLOR)
        back_btn = create_btn(font, screen, BTN_COLOR, WIDTH // 3 - 25, 650, 'Back', BTN_TEXT_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_btn.collidepoint(pygame.mouse.get_pos()):
                    running = False
                    break
                elif lvl1_btn.collidepoint(pygame.mouse.get_pos()):
                    edit_level(1)
                elif lvl2_btn.collidepoint(pygame.mouse.get_pos()):
                    edit_level(2)
                elif lvl3_btn.collidepoint(pygame.mouse.get_pos()):
                    edit_level(3)
                elif lvl4_btn.collidepoint(pygame.mouse.get_pos()):
                    edit_level(4)
                elif lvl5_btn.collidepoint(pygame.mouse.get_pos()):
                    edit_level(5)
        pygame.display.update()


def select_lvl_menu():
    """
    This function is responsible for displaying a menu
    in which you can select the desired level by clicking on the buttons.
    :return: nothing
    """
    global screen
    global game_map
    global level
    font = pygame.font.SysFont('liberationmono', 45)
    running = True
    while running:
        screen.fill(MENU_COLOR)
        select_lvl_menu_timer.tick(MENU_FPS)
        lvl1_btn = create_btn(font, screen, BTN_COLOR, WIDTH // 3 - 25, 150, '1 LVL', BTN_TEXT_COLOR)
        lvl2_btn = create_btn(font, screen, BTN_COLOR, WIDTH // 3 - 25, 250, '2 LVL', BTN_TEXT_COLOR)
        lvl3_btn = create_btn(font, screen, BTN_COLOR, WIDTH // 3 - 25, 350, '3 LVL', BTN_TEXT_COLOR)
        lvl4_btn = create_btn(font, screen, BTN_COLOR, WIDTH // 3 - 25, 450, '4 LVL', BTN_TEXT_COLOR)
        lvl5_btn = create_btn(font, screen, BTN_COLOR, WIDTH // 3 - 25, 550, '5 LVL', BTN_TEXT_COLOR)
        back_btn = create_btn(font, screen, BTN_COLOR, WIDTH // 3 - 25, 650, 'Back', BTN_TEXT_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_btn.collidepoint(pygame.mouse.get_pos()):
                    running = False
                    break
                elif lvl1_btn.collidepoint(pygame.mouse.get_pos()):
                    game_map = load_level(1)
                    level = 1
                elif lvl2_btn.collidepoint(pygame.mouse.get_pos()):
                    game_map = load_level(2)
                    level = 2
                elif lvl3_btn.collidepoint(pygame.mouse.get_pos()):
                    game_map = load_level(3)
                    level = 3
                elif lvl4_btn.collidepoint(pygame.mouse.get_pos()):
                    game_map = load_level(4)
                    level = 4
                elif lvl5_btn.collidepoint(pygame.mouse.get_pos()):
                    game_map = load_level(5)
                    level = 5
                running = False
                break
        pygame.display.update()


def get_record(level):
    """
    This function reads the record value at this level from the corresponding file
    according to the specified level number and returns this value.
    :param level: The number of desired level
    :return: It returns the record value on the desired level
    """
    file_name = f'record{level}.txt'
    file = open(file_name, 'r')
    record = ''
    for line in file:
        record = line
    file.close()
    if record[-1] == '\n':
        record = record[:-1]
    return record


def records_menu():
    """
    This function displays on the screen the values of the records on each of the levels.
    :return: nothing
    """
    global screen
    font = pygame.font.SysFont('liberationmono', 45)
    records_color = (230, 225, 237)
    screen.fill(MENU_COLOR)
    text_1 = font.render('LVL1: ', True, records_color)
    text_2 = font.render('LVL2: ', True, records_color)
    text_3 = font.render('LVL3: ', True, records_color)
    text_4 = font.render('LVL4: ', True, records_color)
    text_5 = font.render('LVL5: ', True, records_color)
    screen.blit(text_1, (WIDTH // 3 - 25, 150))
    screen.blit(text_2, (WIDTH // 3 - 25, 250))
    screen.blit(text_3, (WIDTH // 3 - 25, 350))
    screen.blit(text_4, (WIDTH // 3 - 25, 450))
    screen.blit(text_5, (WIDTH // 3 - 25, 550))
    back_btn = create_btn(font, screen, BTN_COLOR, WIDTH // 3 - 25, 650, 'Back', BTN_TEXT_COLOR)
    record_1 = font.render(get_record(1), True, records_color)
    record_2 = font.render(get_record(2), True, records_color)
    record_3 = font.render(get_record(3), True, records_color)
    record_4 = font.render(get_record(4), True, records_color)
    record_5 = font.render(get_record(5), True, records_color)
    screen.blit(record_1, (WIDTH // 2 - 20, 150))
    screen.blit(record_2, (WIDTH // 2 - 20, 250))
    screen.blit(record_3, (WIDTH // 2 - 20, 350))
    screen.blit(record_4, (WIDTH // 2 - 20, 450))
    screen.blit(record_5, (WIDTH // 2 - 20, 550))

    running = True
    while running:
        records_menu_timer.tick(MENU_FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_btn.collidepoint(pygame.mouse.get_pos()):
                    running = False
                    break
        pygame.display.update()


def run_main_menu():
    """
    This function is responsible for displaying the main menu on the screen,
    as well as buttons with which you can go to the corresponding sections of the application.
    :return: nothing
    """
    global screen
    global level
    font = pygame.font.SysFont('liberationmono', 45)
    running = True
    while running:
        screen.fill(MENU_COLOR)
        main_menu_timer.tick(MENU_FPS)

        play_btn = create_btn(font, screen, BTN_COLOR, WIDTH // 3 - 25, 150, 'Play game', BTN_TEXT_COLOR)
        select_lvl_btn = create_btn(font, screen, BTN_COLOR, WIDTH // 3 - 25, 250, 'Select level', BTN_TEXT_COLOR)
        level_editor_btn = create_btn(font, screen, BTN_COLOR, WIDTH // 3 - 25, 350, 'Level editor', BTN_TEXT_COLOR)
        change_color_btn = create_btn(font, screen, BTN_COLOR, WIDTH // 3 - 25, 450, 'Snake color', BTN_TEXT_COLOR)
        record_btn = create_btn(font, screen, BTN_COLOR, WIDTH // 3 - 25, 550, 'Show records', BTN_TEXT_COLOR)
        exit_btn = create_btn(font, screen, BTN_COLOR, WIDTH // 3 - 25, 650, 'Exit', BTN_TEXT_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_btn.collidepoint(pygame.mouse.get_pos()):
                    play_game(level)
                elif select_lvl_btn.collidepoint(pygame.mouse.get_pos()):
                    select_lvl_menu()
                elif change_color_btn.collidepoint(pygame.mouse.get_pos()):
                    ch_color_menu()
                elif level_editor_btn.collidepoint(pygame.mouse.get_pos()):
                    lvl_edit_menu()
                elif record_btn.collidepoint(pygame.mouse.get_pos()):
                    records_menu()
                elif exit_btn.collidepoint(pygame.mouse.get_pos()):
                    exit()

        pygame.display.update()
    exit()


run_main_menu()

