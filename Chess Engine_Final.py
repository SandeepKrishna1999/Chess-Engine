import chess
import chess.svg
import chess.polyglot
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import graphics
from graphics import *


# -------------------------------------------------------------------------------------------------
#                               Evaluation function
# -------------------------------------------------------------------------------------------------

def evaluate(board, depth): # Returns advantage of a particular player(scaled by 100 units)
    # Initialize scores and other parameters
    white_score = black_score = 0
    # Check if in checkmate or stalemate
    if board.is_checkmate():
        return 1e9 + depth if board.turn == chess.WHITE else -1e9 - depth
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0
    
    piece_value_white = {'K': 60000,
                        'Q': 900,
                        'R': 490,
                        'B': 320,
                        'N': 290,
                        'P': 100}
    
    piece_value_black = {'k': 60000,
                        'q': 900,
                        'r': 490,
                        'b': 320,
                        'n': 290,
                        'p': 100}

    pos = str(board.fen)
    piecedict = {}
    for i in pos:
        if i in piecedict:
            piecedict[i] += 1
        else:
            piecedict[i] = 1
    
    white_score += piecedict['K']*piece_value_white['K'] + piecedict['Q']*piece_value_white['Q'] + piecedict['B']*piece_value_white['B'] + piecedict['N']*piece_value_white['N'] + piecedict['R']*piece_value_white['R'] + piecedict['P']*piece_value_white['P']
    black_score += piecedict['k']*piece_value_black['k'] + piecedict['q']*piece_value_black['q'] + piecedict['b']*piece_value_black['b'] + piecedict['n']*piece_value_black['n'] + piecedict['r']*piece_value_black['r'] + piecedict['p']*piece_value_black['p']

    bishop_pair_bonus = 15 #Bonus for having a bishop pair
    mobility_factor = 5 #Value yet to be incorporated and optimised

    castling_bonus = 50 #Castling implies a safer king and hence this bonus is given(value to be optimised)

    double_pawn_punishment = -40  # Give punishment if there are 2 pawns on the same column, maybe increase if late in game. Calibrate value
    isolated_pawn_punishment = -40  # If the pawn has no allies on the columns next to it, calibrate value later

    knight_endgame_punishment = -10  # Punishment for knights in endgame, per piece
    bishop_endgame_bonus = 10  # Bonus for bishops in endgame, per piece

    rook_on_semi_open_file_bonus = 20  # Give rook a bonus for being on an open file without any own pawns, right now it is per rook
    rook_on_open_file_bonus = 20  # Give rook a bonus for being on an open file without any pawns, right now it is per rook

    blocking_d_e_pawn_punishment = -40  # Punishment for blocking unmoved pawns on d and e file 

    knight_pawn_bonus = 2  # Knights better with lots of pawns
    bishop_pawn_punishment = -2  # Bishops worse with lots of pawns
    rook_pawn_punishment = -2  # Rooks worse with lots of pawns

    center_attack_bonus_factor = 1  # Factor to multiply with how many center squares are attacked by own pieces(yet to incorporate)
    king_attack_bonus_factor = 5  # Factor to multiply with how many squares around enemy king that are attacked by own pieces(yet to incorporate)

    real_board_squares = [21, 22, 23, 24, 25, 26, 27, 28,
                          31, 32, 33, 34, 35, 36, 37, 38,
                          41, 42, 43, 44, 45, 46, 47, 48,
                          51, 52, 53, 54, 55, 56, 57, 58,
                          61, 62, 63, 64, 65, 66, 67, 68,
                          71, 72, 73, 74, 75, 76, 77, 78,
                          81, 82, 83, 84, 85, 86, 87, 88,
                          91, 92, 93, 94, 95, 96, 97, 98]
    
    manhattan_distance = [6, 5, 4, 3, 3, 4, 5, 6,
                          5, 4, 3, 2, 2, 3, 4, 5,
                          4, 3, 2, 1, 1, 2, 3, 4,
                          3, 2, 1, 0, 0, 1, 2, 3,
                          3, 2, 1, 0, 0, 1, 2, 3,
                          4, 3, 2, 1, 1, 2, 3, 4,
                          5, 4, 3, 2, 2, 3, 4, 5,
                          6, 5, 4, 3, 3, 4, 5, 6]
    
    directions = [-10, -1, 10, 1, -11, -9, 9, 11]
    
# -------------------------------------------------------------------------------------------------
#                          Up until endgame evaluation
# -------------------------------------------------------------------------------------------------

    # Opening related bonuses/punishment
    if board.fullmove_number <= 50 and white_score > 62280:

        lines = bookeva(board)
        
        if (lines):
            print("The popular continuations to this sequence are:")
            for key,value in lines.items():
                print(key, ":", value)
        else:
            evalboard(board, depth)
        
        # Castling bonus
        if board.has_castling_rights(chess.WHITE) == 0:
            white_score += castling_bonus
        if board.has_castling_rights(chess.BLACK) == 0:
            black_score += castling_bonus

        pm = board.piece_map()

        # Punishment for pieces in front of undeveloped d and e pawns
        if pm.get(chess.D2) == 'P' and pm.get(chess.D3) != 'None':
            white_score += blocking_d_e_pawn_punishment
        if pm.get(chess.E2) == 'P' and pm.get(chess.E3) != 'None':
            white_score += blocking_d_e_pawn_punishment

        if pm.get(chess.D7) == 'p' and pm.get(chess.D6) != 'None':
            black_score += blocking_d_e_pawn_punishment
        if pm.get(chess.E7) == 'p' and pm.get(chess.E6) != 'None':
            black_score += blocking_d_e_pawn_punishment

        # Bishop pair bonus
        if piecedict['B'] == 2:
            white_score += bishop_pair_bonus
        if piecedict['b'] == 2:
            black_score += bishop_pair_bonus

        # Double pawn punishment
        wsquares = list(board.pieces(chess.PAWN ,chess.WHITE))
        bsquares = list(board.pieces(chess.PAWN ,chess.BLACK))
        for i in range(len(wsquares)):
            for j in range(1,len(wsquares)):
                if (wsquares[j]-wsquares[i])%8 == 0:
                    if wsquares[j]!=wsquares[i]:
                        white_score += double_pawn_punishment

        for i in range(len(bsquares)):
            for j in range(1,len(bsquares)):
                if (bsquares[j]-bsquares[i])%8 == 0:
                    if bsquares[j]!=bsquares[i]:
                        black_score += double_pawn_punishment

        # Isolated pawn punishment
        for i in range(len(wsquares)):
            if wsquares[i]+1 not in wsquares and wsquares[i]-1 not in wsquares and wsquares[i]+7 not in wsquares and wsquares[i]+9 not in wsquares and wsquares[i]-7 not in wsquares and wsquares[i]-9 not in wsquares:
                if wsquares[i]+41 not in wsquares and wsquares[i]+39 not in wsquares and wsquares[i]+33 not in wsquares and wsquares[i]+31 not in wsquares and wsquares[i]+25 not in wsquares and wsquares[i]+23 not in wsquares and wsquares[i]+17 not in wsquares and wsquares[i]+15 not in wsquares:
                    if wsquares[i]-41 not in wsquares and wsquares[i]-39 not in wsquares and wsquares[i]-33 not in wsquares and wsquares[i]-31 not in wsquares and wsquares[i]-25 not in wsquares and wsquares[i]-23 not in wsquares and wsquares[i]-17 not in wsquares and wsquares[i]-15 not in wsquares:
                        white_score += isolated_pawn_punishment

        for i in range(len(bsquares)):
            if bsquares[i]+1 not in bsquares and bsquares[i]-1 not in bsquares and bsquares[i]+7 not in bsquares and bsquares[i]+9 not in bsquares and bsquares[i]-7 not in bsquares and bsquares[i]-9 not in bsquares:
                if bsquares[i]+41 not in bsquares and bsquares[i]+39 not in bsquares and bsquares[i]+33 not in bsquares and bsquares[i]+31 not in bsquares and bsquares[i]+25 not in bsquares and bsquares[i]+23 not in bsquares and bsquares[i]+17 not in bsquares and bsquares[i]+15 not in bsquares:
                    if bsquares[i]-41 not in bsquares and bsquares[i]-39 not in bsquares and bsquares[i]-33 not in bsquares and bsquares[i]-31 not in bsquares and bsquares[i]-25 not in bsquares and bsquares[i]-23 not in bsquares and bsquares[i]-17 not in bsquares and bsquares[i]-15 not in bsquares:
                        black_score += isolated_pawn_punishment

        # Rook on open and semi-open file bonus
        wrsquares = list(board.pieces(chess.ROOK ,chess.WHITE))
        brsquares = list(board.pieces(chess.ROOK ,chess.BLACK))
        for i in wrsquares:
            flag = 0
            j = i + 8
            last_rank = [56, 57, 58, 59, 60, 61, 62, 63]
            while j not in last_rank:
                if j in list(board.pieces(chess.PAWN ,chess.WHITE)):
                    flag = 1
                    break
                j += 8
            if flag == 0:
                white_score += rook_on_semi_open_file_bonus

        for i in brsquares:
            flag = 0
            j = i - 8
            last_rank = [0, 1, 2, 3, 4, 5, 6, 7]
            while j not in last_rank:
                if j in list(board.pieces(chess.PAWN ,chess.BLACK)):
                    flag = 1
                    break
                j -= 8
            if flag == 0:
                black_score += rook_on_semi_open_file_bonus

        for i in wrsquares:
            flag = 0
            j = i + 8
            last_rank = [56, 57, 58, 59, 60, 61, 62, 63]
            while j not in last_rank:
                if j in list(board.pieces(chess.PAWN ,chess.WHITE)) or j in list(board.pieces(chess.PAWN, chess.BLACK)):
                    flag = 1
                    break
                j += 8
            if flag == 0:
                white_score += rook_on_open_file_bonus

        for i in brsquares:
            flag = 0
            j = i - 8
            last_rank = [0, 1, 2, 3, 4, 5, 6, 7]
            while j not in last_rank:
                if j in list(board.pieces(chess.PAWN ,chess.BLACK)) or j in list(board.pieces(chess.PAWN ,chess.WHITE)):
                    flag = 1
                    break
                j -= 8
            if flag == 0:
                black_score += rook_on_open_file_bonus
    
    
    # Bonus for attacking squares around the enemy king (Yet to incorporate)
    #white_score += king_attacks_white * king_attack_bonus_factor
    #black_score += king_attacks_black * king_attack_bonus_factor

# -------------------------------------------------------------------------------------------------
#                              Midgame related functions(Yet to incorporate)
# -------------------------------------------------------------------------------------------------

    #if board.fullmove_number > 20 and board.fullmove_number <= 40:
        # Bonus for attacking squares in the center
        #white_score += center_attacks_white * center_attack_bonus_factor
        #black_score += center_attacks_black * center_attack_bonus_factor

# -------------------------------------------------------------------------------------------------
#                               Endgame related functions
# -------------------------------------------------------------------------------------------------

    if white_score+black_score < 38:

        # Knights are worth slightly less in endgame
        white_score += piecedict['N'] * knight_endgame_punishment
        black_score += piecedict['n'] * knight_endgame_punishment

        # Bishops are worth slightly more in endgame
        white_score += piecedict['B'] * bishop_endgame_bonus
        black_score += piecedict['b'] * bishop_endgame_bonus

        # Knights better with lots of pawns, bishops worse. Rooks better with less pawns.
        white_score += piecedict['N'] * piecedict['P'] * knight_pawn_bonus
        black_score += piecedict['n'] * piecedict['p'] * knight_pawn_bonus

        white_score += piecedict['B'] * piecedict[0]['P'] * bishop_pawn_punishment
        black_score += piecedict['b'] * piecedict[1]['p'] * bishop_pawn_punishment

        white_score += piecedict['R'] * piecedict['P'] * rook_pawn_punishment
        black_score += piecedict['r'] * piecedict['p'] * rook_pawn_punishment

        # Finding mate with no pawns on the board and without syzygy endgame tablebase.
        if piecedict['p'] == piecedict['P'] == 0:
            # Add a small term for piece values, otherwise the algorithm might sacrifice a piece sometimes for no reason.
            white_score = 0.05*piecedict['K']*piece_value_white['K'] + piecedict['Q']*piece_value_white['Q'] + piecedict['B']*piece_value_white['B'] + piecedict['N']*piece_value_white['N'] + piecedict['R']*piece_value_white['R'] + piecedict['P']*piece_value_white['P']
            black_score = 0.05*piecedict['k']*piece_value_black['k'] + piecedict['q']*piece_value_black['q'] + piecedict['b']*piece_value_black['b'] + piecedict['n']*piece_value_black['n'] + piecedict['r']*piece_value_black['r'] + piecedict['p']*piece_value_black['p']
            # White advantage (no rooks or queens on enemy side and a winning advantage)
            if piecedict['r'] == piecedict['q'] == 0 and white_score > black_score:
                # Lone K vs K and (R, Q and/or at least 2xB). Only using mop-up evaluation.
                if piecedict['R'] >= 1 or piecedict['Q'] >= 1 or piecedict['B'] >= 2:
                    black_king_real_pos = real_board_squares.index(board.king(chess.BLACK))
                    white_king_real_pos = real_board_squares.index(board.king(chess.WHITE))
                    white_score += 4.7 *manhattan_distance[black_king_real_pos] + 1.6 * (14 - manhattan_distance[black_king_real_pos] - manhattan_distance[white_king_real_pos])
                # Lone K vs K, N and B
                if piecedict['R'] == piecedict['Q'] == 0 and piecedict['B'] >= 1 and piecedict['N'] >= 1:
                    pass
            # Black advantage (no rooks or queens on enemy side and a winning advantage)
            if piecedict['R'] == piecedict['Q'] == 0 and black_score > white_score:
                # Lone K vs K and (R, Q and/or at least 2xB). Only using mop-up evaluation.
                if piecedict['r'] >= 1 or piecedict['q'] >= 1 or piecedict['b'] >= 2:
                    white_king_real_pos = real_board_squares.index(board.king(chess.WHITE))
                    black_king_real_pos = real_board_squares.index(board.king(chess.BLACK))
                    black_score += 4.7 * manhattan_distance[white_king_real_pos] + 1.6 * (14 - manhattan_distance[white_king_real_pos] - manhattan_distance[black_king_real_pos])
                # Lone K vs K, N and B
                if piecedict['r'] == piecedict['q'] == 0 and piecedict['b'] >= 1 and piecedict['n'] >= 1:
                    pass

    print("White advantage: ", white_score - black_score + 1300)                    
    return black_score - white_score - 1300


class MoveNode:
    def __init__(self, Board):
        self.board = Board
        self.children = []
        self.eval = 0
        self.next = None
        self.nextmove = None
    
    
    
#White player trying to maximize advantage
#Inputs:
#node: Node object of board and evaluation and an array of children nodes
#depth: remaining plys to investigate
#currentdepth: number of plys investigated so far in recursive tree building
#al: alpha, the highest advantage the minimizing player has allowed thus far, given in centipawn advantage for white
#be: beta, the lowest advantage the maximizing player can attain thus far, given in centipawn advantage for white
#tolerance: tolerance for positions that are lower than the beta but will not be pruning by alpha-beta pruning, given in centipawn advantage for white
#Outputs:
#ev: evaluation of the board associated with the input node, given in centipawn advantage for white
def whiteForAdvantage(node, depth, currentdepth, al, be, tolerance):
    #evaluate current board
    #print("white to move, depth = ", currentdepth," remaining = ",depth," ",al," ",be, "\n")
    node.eval = -1*evaluate(node.board, currentdepth)
    print(node.board, '\n\n')
    
    #return if max depth has been reached
    if depth == 0:
        return node.eval
    
    #create an indexable list of legal moves
    lm = list(node.board.legal_moves)
    childeval = []

    
    
    if len(lm) == 0:
        return node.eval
    
    # iterate through each legal move and call blackForDefense to evaluate each child
    for i in range(len(lm)):
        child = MoveNode(node.board.copy())
        child.board.push(lm[i])
        ev = blackForDefense(child, depth-1, currentdepth+1, al, be, tolerance)
        
        if ev>al:
            al = ev
        
        if ev>=be-tolerance or len(childeval) == 0:
            if len(childeval) ==0:
                be = ev
            node.children.append(child)
            childeval.append(ev)
               
    #iterate through list of children nodes to get the node with the max eval
    node.eval = childeval[0]
    node.next = node.children[0]
    node.nextmove = lm[0]
    for i in range(len(childeval)):
        if node.eval < childeval[i]:
            node.eval = childeval[i]
            node.next = node.children[i]
            node.nextmove = lm[i]
    return node.eval



#Black player trying to minimize advantage
#Inputs:
#node: Node object of board and evaluation and an array of children nodes
#depth: remaining plys to investigate
#currentdepth: number of plys investigated so far in recursive tree building
#al: alpha, the highest advantage the minimizing player has allowed thus far, given in centipawn advantage for white
#be: beta, the lowest advantage the maximizing player can attain thus far, given in centipawn advantage for white
#tolerance: tolerance for positions that are higher than alpha but will not be pruning by alpha-beta pruning, given in centipawn advantage for white
#Outputs:
#ev: evaluation of the board associated with the input node, given in centipawn advantage for white
def blackForDefense(node, depth, currentdepth, al, be, tolerance):
    #evaluate current board
    print("Black to move, depth = ", currentdepth," remaining = ",depth," ",al," ",be, "\n")
    node.eval = -1*evaluate(node.board, currentdepth)
    print(node.board, '\n\n')
    
    #return if max depth has been reached
    if depth == 0:
        return node.eval
    
    #create an indexable list of legal moves
    lm = list(node.board.legal_moves)
    childeval = []
    
    if len(lm) == 0:
        return node.eval
    
    # iterate through each legal move and call whiteForAdvantage to evaluate each child
    for i in range(len(lm)):
        child = MoveNode(node.board.copy())
        child.board.push(lm[i])
        
        ev = whiteForAdvantage(child, depth-1, currentdepth+1, al, be, tolerance)
        
        if ev<be:
            be = ev
        
        if ev<=al+tolerance or len(childeval) == 0:
            if len(childeval) ==0:
                al = ev
            node.children.append(child)
            childeval.append(ev)
            
    #iterate through list of children nodes to get the node with the min eval
    node.eval = childeval[0]
    node.next = node.children[0]
    node.nextmove = lm[0]
    for i in range(len(childeval)):
        if node.eval > childeval[i]:
            node.eval = childeval[i]
            node.next = node.children[i]
            node.nextmove = lm[i]
    return node.eval



#Determines whos move it is and starts recursive tree search with the corresponding player
#Inputs:
#node: Node object of board and evaluation and an array of children nodes
#depth: remaining plys to investigate
#tolerance: tolerance for positions that are higher than alpha but will not be pruning by alpha-beta pruning, given in centipawn advantage for white
#Outputs:
#ev: evaluation of the board associated with the input node, given in centipawn advantage for white
def treestart(node, depth, tolerance):
    al = be = -1*evaluate(node.board, 0)
    if node.board.turn == chess.WHITE:
        return whiteForAdvantage(node, depth, 0, al, be, tolerance)
    else:
        return blackForDefense(node, depth, 0, al, be, tolerance)


#Accepts a board and uses tree functions to get evaluation
#Inputs:
#Board: python-chess board object
#depth: remaining plys to investigate
#Outputs:
#ev: evaluation of the board associated with the input node, given in centipawn advantage for white
def evalboard(board, depth):
    root = MoveNode(board)
    ev = treestart(root, depth, 0)
    temp = root
    print("eval: ",ev)
    i = 0
    while (i < depth) and temp.board.is_checkmate()==False:
        print(temp.nextmove, end = ' -> ')
        temp = temp.next
        i=i+1
    print('...')
    return ev
        
        
def evalposfromfen(fen, depth):
    board = chess.Board(fen)
    evalboard(board,depth)
        
        
def evalpostest():
    board = chess.Board()
    evaluate(board,0)   

    
def bookeva(board):
    eva_dic = {}
    with chess.polyglot.open_reader("Perfect2017.bin") as reader:
        for entry in reader.find_all(board,minimum_weight = 1):
            eva_dic[entry.move] = entry.weight
    if len(eva_dic) == 0:
        return 0
    return(eva_dic)

def fen_converter(ip):
    output=' '
    for i in range(len(ip)):
        if ip[i]==' ':
            break
        if ip[i]=='/':
            continue
        if ip[i]=='8':
            output=output+'11111111'
        if ip[i]=='7':
            output=output+'1111111'
        if ip[i]=='6':
            output=output+'111111'
        if ip[i]=='5':
            output=output+'11111'
        if ip[i]=='4':
            output=output+'1111'
        if ip[i]=='3':
            output=output+'111'
        if ip[i]=='2':
            output=output+'11'
        if ip[i]=='1':
            output=output+'1'
        if ip[i]=='r':
            output=output+'r'
        if ip[i]=='n':
            output=output+'n'
        if ip[i]=='b':
            output=output+'b'
        if ip[i]=='q':
            output=output+'q'
        if ip[i]=='k':
            output=output+'k'
        if ip[i]=='R':
            output=output+'R'
        if ip[i]=='N':
            output=output+'N'
        if ip[i]=='B':
            output=output+'B'
        if ip[i]=='Q':
            output=output+'Q'
        if ip[i]=='K':
            output=output+'K'
        if ip[i]=='p':
            output=output+'p'
        if ip[i]=='P':
            output=output+'P'
    return output

def move():
    turn = 1
    board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    boardsvg = chess.svg.board(board, size=1800)
    
    outputfile = open("trial.svg", "w")
    outputfile.write(boardsvg)
    outputfile.close()
    
    drawing = svg2rlg("trial.svg")
    renderPM.drawToFile(drawing, "tfile.png", fmt="PNG")
    
    img = mpimg.imread("tfile.png")
    implot = plt.imshow(img)
    plt.show()
    
    i = " "
    
    while board.legal_moves != 0 or i!="end":# the game will end if there's no legal move for one player
        print('Move number {} '.format(board.fullmove_number))
        #b = board.piece_map()   #where the piece is<a dictionary>
        if turn%2 != 0:
            print('White to move')
        else:
            print('Black to move')
        turn = turn + 1
        a = board.legal_moves

        print(a)
        try:
            i = input("Enter your move: ")
            d = eval(input("Enter depth: "))
            
            if i != "end":
                move = chess.Move.from_uci(str(board.parse_san(i)))
                board.push(move)
    
                boardsvg = chess.svg.board(board, size=1800)
                outputfile = open('trial.svg', "w")
                outputfile.write(boardsvg)
                outputfile.close()
    
                drawing = svg2rlg("trial.svg")
                renderPM.drawToFile(drawing, "tfile.png", fmt="PNG")
                img = mpimg.imread("tfile.png")
                implot = plt.imshow(img)
                plt.show()
                black_adv = evaluate(board, d)
                print("Black advantage: ", black_adv)
        except ValueError:
            print('Enter valid values for move and depth')
            turn = turn-1;
    return (turn)


n = 1
while n:
    turn = move()
    if turn%2 !=0:
        print('Black win')
    else:
        print('White win')
    n = 0
    new = input('Type 1 if you want to start a new game')
    if new == 1:
        n = 1
        