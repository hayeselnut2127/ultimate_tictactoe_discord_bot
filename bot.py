import discord
import config

TOKEN = config.DISCORD_TOKEN

SUB_BOARD_SIZE = 3
SUB_BOARD_ROW_COUNT = 3
SUB_BOARD_COLUMN_COUNT = 3
BORDER_SIZE = 1
BOARD_SIZE = SUB_BOARD_ROW_COUNT * SUB_BOARD_SIZE + (SUB_BOARD_ROW_COUNT - BORDER_SIZE)

DISPLAY_EMPTY = "⬜️"
DISPLAY_BORDER = "⬛️"
DISPLAY_MINE = "🟥" # :red_square:
DISPLAY_MINE_NEW = "🔴" # :red_circle:
DISPLAY_OPPONENT = "🟦" # :blue_square:
DISPLAY_OPPONENT_NEW = "🔵" # :blue_circle:
DISPLAY_INVALID = "❌"

ANNOYING_WHITE_SPACE = 65039

SQUARE_EMPTY = 0
SQUARE_MINE = 1
SQUARE_MINE_NEW = 2
SQUARE_OPPONENT = -1
SQUARE_OPPONENT_NEW = -2

BOARD_ONGOING = 0
BOARD_WIN = 1
BOARD_LOSS = -1

BOARD = []

# Board / Sub-board layout:
#    0   1   2
# 0 [ ] [ ] [ ]
# 1 [ ] [ ] [ ]
# 2 [ ] [ ] [ ]

def convert_to_list(text):
    board_in_list = []
    for c in text:
        if ord(c) == ANNOYING_WHITE_SPACE:
            continue
        if ord(c) == 11035: # DISPLAY_BORDER
            continue
        if c == "\n":
            continue
        board_in_list.append(c)

    return board_in_list

def init_sub_board():
    sub_board = []
    for i in range(0, SUB_BOARD_SIZE):
        sub_board.append([SQUARE_EMPTY, SQUARE_EMPTY, SQUARE_EMPTY])

    return sub_board

def init_board():
    board = [[], [], []]
    for i in range(0, SUB_BOARD_ROW_COUNT):
        for j in range(0, SUB_BOARD_COLUMN_COUNT):
            board[i].append(init_sub_board())

    return board

def display_square(square):
    if square == SQUARE_EMPTY:
        return DISPLAY_EMPTY
    
    if square == SQUARE_MINE:
        return DISPLAY_MINE

    if square == SQUARE_MINE_NEW:
        return DISPLAY_MINE_NEW

    if square == SQUARE_OPPONENT:
        return DISPLAY_OPPONENT

    if square == SQUARE_OPPONENT_NEW:
        return DISPLAY_OPPONENT_NEW

    return DISPLAY_INVALID

def display_board(board):
    # Have to display in rows

    text = "$ultimate-tic-tac-toe\n"

    for i in range(0, SUB_BOARD_ROW_COUNT):
        for j in range(0, SUB_BOARD_COLUMN_COUNT):
            for k in range(0, SUB_BOARD_SIZE):
                for l in range (0, SUB_BOARD_SIZE):
                    text += display_square(board[i][j][k][l])
                if k < 2:
                    text += DISPLAY_BORDER
            text += "\n"

        if i < 2:    
            for b in range (0, BOARD_SIZE):
                text += DISPLAY_BORDER
            text += "\n"

    return text

def read_square(display_square):

    if display_square == DISPLAY_EMPTY:
        return SQUARE_EMPTY

    if display_square == DISPLAY_BORDER:
        return SQUARE_BORDER
    
    if display_square == DISPLAY_MINE:
        return SQUARE_MINE
    
    if display_square == DISPLAY_MINE_NEW:
        return SQUARE_MINE_NEW

    if display_square == DISPLAY_OPPONENT:
        return SQUARE_OPPONENT

    if display_square == DISPLAY_OPPONENT_NEW:
        return SQUARE_OPPONENT_NEW

def read_sub_board(b, board_in_list, i, j):
    index = 27 * i + 3 * j

    for x in range(0, SUB_BOARD_SIZE):
        for y in range(0, SUB_BOARD_SIZE):
            b[i][j][x][y] = read_square(board_in_list[index + 9 * x + y])

    return b

def read_board(board_in_list):
    b = init_board()

    for i in range(0, SUB_BOARD_ROW_COUNT):
        for j in range(0, SUB_BOARD_COLUMN_COUNT):
            b = read_sub_board(b, board_in_list, i, j)
    
    return b

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global BOARD
    if message.author == client.user:
        return

    if message.content.startswith('$ultimate-tic-tac-toe'):
        # MY MOVE
        BOARD = init_board()
        if message.content == "$ultimate-tic-tac-toe":
            # START:
            print("initiating new board")
        else:
            # CHAR BY CHAR
            board_in_list = convert_to_list(message.content.split("$ultimate-tic-tac-toe\n")[1])

            # import list into board
            BOARD = read_board(board_in_list)
            print(BOARD)

        await message.channel.send(display_board(BOARD))

client.run(TOKEN)