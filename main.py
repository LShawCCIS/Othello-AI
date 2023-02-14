import copy
import random
import resource

FOUR_BY_FOUR = [
                [+1000, +2, +2, +1000],
                [-10,  +0, +0,  -10],
                [-10,  +0, +0,  -10],
                [+1000, +2, +2, +1000]
            ]

SIX_BY_SIX = [
                [+1000,-15, +7, +7, -15, +1000],
                [-15, -25, +2, +2, -25,  -15],
                [+6,   +2, +0, +0,  +2,   +6],
                [+6,   +2, +0, +0,  +2,   +6],
                [-15, -25, +2, +2, -25,  -15],
                [+1000,-15, +7, +7, -15, +1000],
            ]

EIGHT_BY_EIGHT = [
                [+1000, -10, +11, +6, +6, +11, -10, +1000],
                [-10,  -20,  +1, +2, +2, +1,  -20,  -10],
                [+10,   +1,  +5, +4, +4, +5,   +1,  +10],
                [+6,    +2,  +4, +0, +0, +4,   +2,   +6],
                [+6,    +2,  +4, +0, +0, +4,   +2,   +6],
                [+10,   +1,  +5, +4, +4, +5,   +1,  +10],
                [-10,  -20,  +1, +2, +2, +1,  -20,  -10],
                [+1000, -10, +11, +6, +6, +11, -10, +1000],
            ]
TEN_BY_TEN = [
                [+1000, -15, +17, +10, +6, +6, +10, +17, -15, +1000],
                [-15,  -20,  +1,  +2, +2, +2, +2,   +1, -20,  -15],
                [+15,   +1,  +5,  +4, +4, +4, +4,   +5,  +1,  +10],
                [+10,   +2,  +4,  +8, +6, +6, +8,   +4,  +2,  +10],
                [+6,    +2,  +4,  +6, +0, +0, +6,   +4,  +2,   +6],
                [+6,    +2,  +4,  +6, +0, +0, +6,   +4,  +2,   +6],
                [+10,   +2,  +4,  +8, +6, +6, +8,   +4,  +2,  +10],
                [+15,   +1,  +5,  +4, +4, +4, +4,   +5,  +1,  +10],
                [-15,  -20,  +1,  +2, +2, +2, +2,   +1, -20,  -15],
                [+1000, -15, +17, +10, +6, +6, +10, +17, -15, +1000]
            ]
 
def gettime():
    rs = resource.getrusage(resource.RUSAGE_SELF)
    return rs[0] + rs[1]

def print_board(board_size, board):
    print("  ", sep="", end="")
    for i in range(board_size):
        print(i, sep="", end="")
    print()
        
    print(" +", sep="", end="")
    for i in range(board_size):
        print('-', sep="", end="")
    print('+')
    
    for i in range(board_size):
        print(str(i) + "|", sep="", end="")
        for j in range(board_size):
            print(board[i][j], sep="", end="")
        print("|" + str(i))
    print(" +", sep="", end="")
    
    for i in range(board_size):
        print('-', sep="", end="")
    print('+')
    
    print("  ", sep="", end="")
    for i in range(board_size):
        print(i, sep="", end="")
    print()
    
def opponent(turn):
    if turn == 'W':
        return 'B'
    return 'W'

def check_directions(row_change, col_change, move, board_size, board, \
                     turn, opp):
    found_self = False
    r,c = move
    r += row_change
    c += col_change
    if r >= 0 and r < board_size and c >= 0 and c < board_size:
        if board[r][c] != opp:
            return False

    while (r >= 0 and r < board_size and c >= 0 and c < board_size) \
          or (found_self and found_opp):
        r += row_change
        c += col_change
        if r < 0 or r >= board_size or c < 0 or c >= board_size: break
        if board[r][c] == ' ':
            return False
        if board[r][c] == turn:
            found_self = True
            return True
    return False

def validate(move, board_size, board, turn, opp):
    direction = []
    valid = check_directions(-1, 0, move, board_size, board, turn, opp)
    if valid: direction.append('N')
    valid = check_directions(1, 0, move, board_size, board, turn, opp)
    if valid: direction.append('S')
    valid = check_directions(0, 1, move, board_size, board, turn, opp)
    if valid: direction.append('E')
    valid = check_directions(0, -1, move, board_size, board, turn, opp)
    if valid: direction.append('W')
    valid = check_directions(-1, -1, move, board_size, board, turn, opp)
    if valid: direction.append('NW')
    valid = check_directions(-1, 1, move, board_size, board, turn, opp)
    if valid: direction.append('NE')
    valid = check_directions(1, 1, move, board_size, board, turn, opp)
    if valid: direction.append('SE')
    valid = check_directions(1, -1, move, board_size, board, turn, opp)
    if valid: direction.append('SW')
    
    if len(direction) > 0: valid = True
    return valid, direction
    
def create_possible_moves(board_size, board, turn, opp):
    moves = [] # will be a list of tuples consisting of valid moves and their
               #   respective directions for flipping
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == ' ':
                move = (i, j)
                is_valid, direction = validate(move, board_size, board, \
                                                turn, opp)
                if is_valid: moves.append((move, direction))

    return moves

def flip(board_size, board, turn, row_change, col_change, move):
    r,c = move
    r += row_change
    c += col_change
    while r >= 0 and r < board_size and c >= 0 and c < board_size \
          and board[r][c] != turn:
        board[r][c] = turn
        r += row_change
        c += col_change

def flip_dir(board_size, board, turn, dirs, move):
    for d in dirs:
        if d == 'N':
            flip(board_size, board, turn, -1, 0, move)
        elif d == 'S':
            flip(board_size, board, turn, 1, 0, move)
        elif d == 'E':
            flip(board_size, board, turn, 0, 1, move)
        elif d == 'W':
            flip(board_size, board, turn, 0, -1, move)
        elif d == 'NW':
            flip(board_size, board, turn, -1, -1, move)
        elif d == 'NE':
            flip(board_size, board, turn, -1, 1, move)
        elif d == 'SE':
            flip(board_size, board, turn, 1, 1, move)
        elif d == 'SW':
            flip(board_size, board, turn, 1, -1, move)
            
def play_move(board_size, board, turn, move, dirs):
    #print("move:", move)
    r,c = move
    board[r][c] = turn
    flip_dir(board_size, board, turn, dirs, move)

def get_random_move(board_size, board, turn):
    # finds possible moves for turn and chooses one
    opp = 'W'
    if turn == 'W': opp = 'B'
    move_list = create_possible_moves(board_size, board, turn, opp)
    random_move = random.randint(0, len(move_list) - 1)
    move, dirs = move_list[random_move]
    return move, dirs

def generate_successors(board, moves, turn, opp):
    successors = []
    #print(moves)
    for m,d in moves:

        changed_board = copy.deepcopy(board)
        #print(m, d)
        play_move(len(board), changed_board, turn, m, d)
        successors.append((changed_board, m))
    return successors

def heuristic(board, turn, max_, move):
    opp = 'W'
    if turn == 'W': opp = 'B'
    turn = opp
    count = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == turn:
                if max_:
                    count -= 1
                else:
                    count += 1
    #print(move)
    r,c = move
    #print(move)
    if len(board) == 4:
        if max_:        
            count -= FOUR_BY_FOUR[r][c]
        else:
            count += FOUR_BY_FOUR[r][c]

    elif len(board) == 6:
        if max_:
            count -= SIX_BY_SIX[r][c]
        else:
            count += SIX_BY_SIX[r][c]
    elif len(board) == 8:
        if max_:
            count -= EIGHT_BY_EIGHT[r][c]
        else:
            count += EIGHT_BY_EIGHT[r][c]
    elif len(board) == 10:
        if max_:
            count -= TEN_BY_TEN[r][c]
        else:
            count += TEN_BY_TEN[r][c]
    return count
                    
        
def minimax(board_size, board, turn, best_MAX, best_MIN, depth, max_, move, first):
    opp = opponent(turn)
    moves = create_possible_moves(board_size, board, turn, opp)
    if depth >= 5 or len(moves) == 0:
        #print(heuristic(board, turn, max_, move))
        return (heuristic(board, turn, max_, move), None)
    else:
        depth += 1
        ret = -999
        s = generate_successors(board, moves, turn, opp)
        index = -1
        move = 0
        if max_:
            ret = -1000
            count = 0
            for successor,action in s:
                count += 1
                index += 1
                v,m = minimax(board_size, successor, opp, ret, best_MIN, \
                              depth, False, action, False)
                #if first:
                    #print("MAX V:", v)
                #    print("CONSIDERED MOVE:", action)
                if v > ret:
                    ret = v
                    move = index
                    #if first:
                        #print("MAX MOVE:", move, moves[move])
                    if ret > best_MIN:
                        return best_MIN, moves[move]
                        
        else:
            ret = 1000
            count = 1
            for successor,action in s:
                count += 1
                index += 1
                v,m = minimax(board_size, successor, opp, best_MAX, ret, \
                              depth, True, action, False)
                if v < ret:
                    ret = v
                    move = index
                    if ret < best_MAX:
                        return best_MAX, moves[move]

        if move == None:
            return ret, None
        return ret, moves[move]

def get_AI_move(board_size, board, turn):
    n = board_size - 1
    corners = [(0,0), (0, n), (n, 0), (n, n)]
    opp = 'W'
    if turn == 'W': opp = 'B'
    moves = create_possible_moves(board_size, board, turn, opp)
    if moves == []:
        return (None, 0)
    for v,r in moves:
        if v in corners:
            return(v, r)
    move = minimax(board_size, board, turn, -1000, 1000, 0, True, (board_size//2, board_size//2), True)
    d,move = move
    move,d = move
    print("RET:", d, move)
    return move,d

def get_move(board_size, board, turn, time_left, opp_time_left):
    move, dirs = get_AI_move(board_size, board, turn)
    #print("RET:", move)
    return move, dirs

def score(board_size, board):
    b_score = 0
    w_score = 0
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == 'W': w_score += 1
            if board[i][j] == 'B': b_score += 1
    print("Player 1 scored:", b_score, "pieces.")
    print("Player 2 scored:", w_score, "pieces.")
    if b_score > w_score: print("Player 1 Wins!")
    elif w_score > b_score: print("Player 2 Wins!")
    else: print("It was a draw!!!")

N = int(input()) # Board size
board = [[' ' for x in range(N)] for x in range(N)] # Create board
board[(N-1)//2][(N-1)//2] = 'W'
board[(N)//2][(N)//2] = 'W'
board[(N-1)//2][(N)//2] = 'B'
board[(N)//2][(N-1)//2] = 'B'

#print_board(N, board) # Print board
#m, d = get_move(6, board, 'B', 100, 100)
#print(m, d)
#print(None)

c = 0
while 1:
    t0 = gettime()
    w_moves = create_possible_moves(N, board, 'B', 'W')
    b_moves = create_possible_moves(N, board, 'W', 'B')
    if len(w_moves) == 0 and len(b_moves) == 0: break
    else:
        if c % 2 == 0 and len(w_moves) > 0:
            print("Player 1's Turn")
            move, dirs = get_move(N, board, 'B', 0, 0)
            #print(move, dirs)
            
            play_move(N, board, 'B', move, dirs)
        elif len(b_moves) > 0:
            print("Player 2's Turn")
            move, dirs = get_random_move(N, board, 'W')
            play_move(N, board, 'W', move, dirs)
        print_board(N, board)
        c += 1
        
score(N, board)
t1 = gettime()
print("Time Taken: ", ((t1 - t0) / 1000) % 60)

